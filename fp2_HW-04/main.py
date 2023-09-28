import os
import uvicorn
import datetime

from fastapi import FastAPI, HTTPException, Depends, APIRouter
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Coords, Level, Pereval, PerevalImages
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Dict
from sqlalchemy.orm import joinedload
from fastapi import Query

app = FastAPI()
router = APIRouter()
app.include_router(router)
load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))
fstr_db_host = os.getenv('FSTR_DB_HOST')
fstr_db_port = os.getenv('FSTR_DB_PORT')
fstr_db_login = os.getenv('FSTR_DB_LOGIN')
fstr_db_pass = os.getenv('FSTR_DB_PASS')

database_url = f'postgresql://{fstr_db_login}:{fstr_db_pass}@{fstr_db_host}:{fstr_db_port}/fstr'

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello():
    return 'Привет'


def create_user(db, user_data):
    user = User(email=user_data['email'], fam=user_data['fam'], otc=user_data['otc'],
                name=user_data['name'], phone=user_data['phone'])
    db.add(user)
    return user


def create_coords(db, coords_data):
    coords = Coords(latitude=coords_data['latitude'], longitude=coords_data['longitude'],
                    height=coords_data['height'])
    db.add(coords)
    return coords


def create_level(db, level_data):
    level = Level(winter=level_data['winter'], summer=level_data['summer'],
                  autumn=level_data['autumn'], spring=level_data['spring'])
    db.add(level)
    return level


def create_perevalImages(db, pereval, images_data):
    images = []
    for image_data in images_data:
        image = PerevalImages(image_name=image_data['data'], title=image_data['title'], pereval=pereval)
        db.add(image)
        images.append(image)
    return images


def create_pereval(db, pereval_data):
    user = create_user(db, pereval_data['user'])
    coords = create_coords(db, pereval_data['coords'])
    level = create_level(db, pereval_data['level'])

    add_time = datetime.datetime.strptime(pereval_data['add_time'], '%Y-%m-%d %H:%M:%S')

    pereval = Pereval(
        beautyTitle=pereval_data['beauty_title'],
        title=pereval_data['title'],
        other_titles=pereval_data['other_titles'],
        connect=pereval_data['connect'],
        add_time=add_time,
        coords=coords,
        user=user,
        level=level
    )

    db.add(pereval)
    db.commit()
    db.refresh(pereval)

    images = create_perevalImages(db, pereval, pereval_data['images'])
    pereval.images = images
    db.commit()

    return pereval


@app.post("/submitData")
def submit_data(data: dict):
    try:
        db = SessionLocal()
        try:
            pereval_data = data.get('pereval')
            pereval = create_pereval(db, pereval_data)
            response_data = {
                "status": 200,
                "message": None,
                "id": pereval.id
            }

            return JSONResponse(content=jsonable_encoder(response_data))

        finally:
            db.close()
    except Exception as e:
        response_data = {
            "status": 500,
            "message": "Ошибка подключения к базе данных",
            "id": None
        }
        raise HTTPException(status_code=500, detail=response_data)


@router.get("/{id}")
def get_pereval_by_id(id: int, db: Session = Depends(get_db)):
    pereval = db.query(Pereval). \
        options(
        joinedload(Pereval.coords),
        joinedload(Pereval.level),
        joinedload(Pereval.images)
    ). \
        filter(Pereval.id == id). \
        first()

    if not pereval:
        raise HTTPException(status_code=404, detail="Перевал не найден")

    return {
        "beauty_title": pereval.beautyTitle,
        "title": pereval.title,
        "other_titles": pereval.other_titles,
        "connect": pereval.connect,
        "add_time": pereval.add_time,
        "status": pereval.status,
        "coords": {
            "latitude": pereval.coords.latitude,
            "longitude": pereval.coords.longitude,
            "height": pereval.coords.height
        },
        "level": {
            "winter": pereval.level.winter,
            "summer": pereval.level.summer,
            "autumn": pereval.level.autumn,
            "spring": pereval.level.spring
        },
        "images": [
            {
                "image_name": image.image_name,
                "title": image.title
            } for image in pereval.images
        ]
    }


app.include_router(router, prefix="/submitData")


@app.patch("/submitData/{id}")
def update_pereval(id: int, data: Dict, db: Session = Depends(get_db)):
    pereval = db.query(Pereval).filter_by(id=id).first()

    if not pereval:
        return {"state": 0, "message": "Перевал не найден"}

    if pereval.status != "new":
        return {"state": 0, "message": "Нельзя редактировать запись с текущим статусом"}

    excluded_fields = ["user_email", "user"]
    for field in excluded_fields:
        if field in data:
            return {"state": 0, "message": f"Поле '{field}' не может быть отредактировано"}

    # Обновляем поля перевала
    if 'beauty_title' in data:
        pereval.beautyTitle = data['beauty_title']
    if 'title' in data:
        pereval.title = data['title']
    if 'other_titles' in data:
        pereval.other_titles = data['other_titles']
    if 'connect' in data:
        pereval.connect = data['connect']
    if 'coords' in data:
        coords = data['coords']
        if 'latitude' in coords:
            pereval.coords.latitude = coords['latitude']
        if 'longitude' in coords:
            pereval.coords.longitude = coords['longitude']
        if 'height' in coords:
            pereval.coords.height = coords['height']
    if 'level' in data:
        level = data['level']
        if 'winter' in level:
            pereval.level.winter = level['winter']
        if 'summer' in level:
            pereval.level.summer = level['summer']
        if 'autumn' in level:
            pereval.level.autumn = level['autumn']
        if 'spring' in level:
            pereval.level.spring = level['spring']

    if 'images' in data:
        images_data = data['images']

        db.query(PerevalImages).filter(PerevalImages.pereval_id == id).delete()

        images = []
        for image_data in images_data:
            image = PerevalImages(image_name=image_data['data'], title=image_data['title'], pereval=pereval)
            db.add(image)
            images.append(image)

        pereval.images = images

    db.commit()

    return {"state": 1, "message": "Запись успешно обновлена"}


@app.get("/submitData/")
def get_user_data(email: str = Query(..., alias="user__email"), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return {"state": 0, "message": "Пользователь не найден"}

    user_data = db.query(Pereval).filter(Pereval.user == user).all()
    data = []
    for item in user_data:
        data.append({
            "beauty_title": item.beautyTitle,
            "title": item.title,
            "other_titles": item.other_titles,
            "connect": item.connect,
            "add_time": item.add_time,
            "status": item.status,
            "coords": {
                "latitude": item.coords.latitude,
                "longitude": item.coords.longitude,
                "height": item.coords.height
            },
            "level": {
                "winter": item.level.winter,
                "summer": item.level.summer,
                "autumn": item.level.autumn,
                "spring": item.level.spring
            },
            "images": [
                {
                    "image_name": image.image_name,
                    "title": image.title
                } for image in item.images
            ]
        })

    return data


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run(app, host="127.0.0.1", port=8000)
