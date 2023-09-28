import datetime
import pytest
from ..models import User, Coords, Level, Pereval, PerevalImages
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///fstr.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    engine.dispose()


def test_user_model(db_session: Session):
    user = User(email='test@example.com', fam='Doe', otc='J', name='John', phone='123456789')
    db_session.add(user)
    db_session.commit()

    assert user.email == 'test@example.com'
    assert user.fam == 'Doe'
    assert user.otc == 'J'
    assert user.name == 'John'
    assert user.phone == '123456789'


def test_coords_model(db_session: Session):
    coords = Coords(latitude=51.5074, longitude=-0.1278, height=100)
    db_session.add(coords)
    db_session.commit()

    assert coords.latitude == 51.5074
    assert coords.longitude == -0.1278
    assert coords.height == 100


def test_level_model(db_session: Session):
    level = Level(winter='high', summer='medium', autumn='low', spring='medium')
    db_session.add(level)
    db_session.commit()

    assert level.winter == 'high'
    assert level.summer == 'medium'
    assert level.autumn == 'low'
    assert level.spring == 'medium'


def test_pereval_model(db_session: Session):
    user = User(email='test@example.com', fam='Doe', otc='J', name='John', phone='123456789')
    coords = Coords(latitude=51.5074, longitude=-0.1278, height=100)
    level = Level(winter='high', summer='medium', autumn='low', spring='medium')
    pereval = Pereval(beautyTitle='Beautiful Pereval', title='Pereval', other_titles='Other',
                      connect='Connection', add_time=datetime.datetime.now(), status='new', user_email=user.email,
                      user=user, coord_id=coords.id, coords=coords, level_id=level.id, level=level)

    db_session.add(pereval)
    db_session.commit()

    assert pereval.beautyTitle == 'Beautiful Pereval'
    assert pereval.title == 'Pereval'
    assert pereval.other_titles == 'Other'
    assert pereval.connect == 'Connection'
    # Add assertions for other fields in Pereval model


def test_pereval_images_model(db_session: Session):
    pereval = db_session.query(Pereval).first()
    pereval_images = PerevalImages(image_name='image.jpg', title='Image', pereval_id=pereval.id)
    db_session.add(pereval_images)
    db_session.commit()

    assert pereval_images.image_name == 'image.jpg'
    assert pereval_images.title == 'Image'
    assert pereval_images.pereval_id == pereval.id
