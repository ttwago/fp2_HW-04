from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    fam = Column(String)
    otc = Column(String)
    name = Column(String)
    phone = Column(String)


class Coords(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True, autoincrement=True)
    winter = Column(String)
    summer = Column(String)
    autumn = Column(String)
    spring = Column(String)


class Pereval(Base):
    __tablename__ = 'pereval'

    STATUS_CHOICES = [
        'new',
        'pending',
        'accepted',
        'rejected',
    ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    beautyTitle = Column(String)
    title = Column(String)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(DateTime)
    status = Column(Enum(*STATUS_CHOICES, name='status_enum'), default='new')
    user_email = Column(String, ForeignKey('users.email', onupdate='CASCADE'))
    user = relationship('User')
    coord_id = Column(Integer, ForeignKey('coords.id', onupdate='CASCADE'))
    coords = relationship('Coords')
    level_id = Column(Integer, ForeignKey('level.id', onupdate='CASCADE'))
    level = relationship('Level')
    images = relationship('PerevalImages', backref='pereval')


class PerevalImages(Base):
    __tablename__ = 'perevalimages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_name = Column(String)
    title = Column(String)
    pereval_id = Column(Integer, ForeignKey('pereval.id'))