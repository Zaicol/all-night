from models import *
from datetime import datetime
from werkzeug.security import generate_password_hash


def makeDefUsers():
    user = UsersModel(
        user_name='admin',
        password_hash=generate_password_hash('admin'),
        regdate=datetime.now())
    user2 = UsersModel(
        user_name='user',
        password_hash=generate_password_hash('user'),
        regdate=datetime.now())
    user3 = UsersModel(
        user_name='org',
        password_hash=generate_password_hash('org'),
        regdate=datetime.now(),
        isOrg=True)
    db.session.add(user)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()


def makeDefPlaces():
    im = "https://burobiz-a.akamaihd.net/uploads/images/76400/large_1.jpg"
    place1 = PlaceModel(
        title='Место 1',
        content='vk.com',
        lat='55.7742129',
        lon='37.5981785',
        date=datetime.now(),
        author=1,
        pic=im)
    place2 = PlaceModel(
        title='Место 2',
        content='yandex.ru',
        lat='55.780626',
        lon='37.595001',
        date=datetime.now(),
        author=2,
        pic=im)
    place3 = PlaceModel(
        title='Место 3',
        content='bing.com',
        lat='55.779190',
        lon='37.599994',
        date=datetime.now(),
        author=1,
        pic=im)
    db.session.add(place1)
    db.session.add(place2)
    db.session.add(place3)
    db.session.commit()


def dbinit(i=0):
    if i:
        db.drop_all()
        db.create_all()
        makeDefUsers()
        makeDefPlaces()


if __name__ == '__main__':
    dbinit(1)
