from flask import redirect, render_template, \
    request, send_file, jsonify
from werkzeug.security import generate_password_hash
from db_default import dbinit
from models import app, db, PlaceModel
from os.path import join, exists, abspath, dirname
from datetime import datetime
from forms import *
import logging


logging.basicConfig(level=logging.DEBUG)
apath = dirname(abspath(__file__))


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html', title='All-night')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect('/index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UsersModel(
            user_name=form.username.data,
            password_hash=generate_password_hash(form.password.data),
            regdate=datetime.now())
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect('/index')
    form = LoginForm()
    session["apath"] = apath
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(
            user_name=form.username.data).first()
        session['username'] = user.user_name
        session['user_id'] = user.id
        return redirect('/index')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    ses_p = ['username', 'user_id', 'news_sort_type', 'reverse', 'pic']
    for item in ses_p:
        try:
            session.pop(item)
        except Exception as e:
            print(e)
    return redirect('/login')


@app.route('/avatar/<int:user_id>', methods=['GET'])
def avatar(user_id):
    user = UsersModel.query.filter_by(id=user_id).first()
    avat = getAvat(user, user.av_type)
    return send_file(avat)


@app.route('/id<int:user_id>', methods=['GET'])
def userpage(user_id):

    if user_id == 0 and "user_id" in session:
        user_s = UsersModel.query.filter_by(id=session["user_id"]).first()
    else:
        user_s = UsersModel.query.filter_by(id=user_id).first()
        if not user_s:
            return redirect('/index')

    if user_s.user_name == "admin":
        user_type = "Администратор"
    elif user_s.isOrg:
        user_type = "Организатор"
    else:
        user_type = "Посетитель"
    regdate = str(user_s.regdate).split('.')[0]
    pic = getAvat(user_s, user_s.av_type)
    return render_template(
        "userpage.html",
        title="Страница пользователя " + user_s.user_name,
        pic=pic, user=user_s, regdate=regdate, user_type=user_type)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect('/login')
    av_form = AvatarForm()
    us_form = ChangeUsernameForm()
    pass_form = ChangePasswordForm()
    user = UsersModel.query.filter_by(id=session["user_id"]).first()
    pic = getAvat(user, user.av_type)
    if av_form.submit_av.data and av_form.validate_on_submit():
        f = av_form.avatar.data
        user = UsersModel.query.filter_by(id=session["user_id"]).first()
        if f.filename.split('.')[-1] == 'gif':
            fnm = 'static/img/' + str(session["user_id"]) + "_av.gif"
            user.av_type = 'gif'
        else:
            fnm = 'static/img/' + str(session["user_id"]) + "_av.png"
            user.av_type = 'png'
        f.save(join(apath, fnm))
        db.session.commit()
        session["pic"] = getAvat(user, user.av_type)
        return redirect('/settings')
    if us_form.submit_us.data and us_form.validate_on_submit():
        user.user_name = us_form.new_name.data
        session["username"] = us_form.new_name.data
        db.session.commit()
        return redirect('/settings')
    if pass_form.submit_pass.data and pass_form.validate_on_submit():
        user.password_hash = generate_password_hash(pass_form.password.data)
        db.session.commit()
        return redirect('/settings')
    return render_template('settings.html', title='Настройки', av_form=av_form,
                           us_form=us_form, pass_form=pass_form, pic=pic)


@app.route('/sitemap', methods=['GET'])
def sitemap():
    return render_template('sitemap.html', title='Карта сайта')


@app.route('/terms')
def terms():
    return render_template(
        'terms.html', title='Пользователькое соглашение')


@app.route('/user/list')
def user_list():
    if 'username' not in session:
        return redirect('/login')
    data = list(map(lambda x: [x.user_name, x.id, booltorus(x.isOrg)],
                    UsersModel.query.all()))
    return render_template(
        'user_list.html', title='Информация о пользователях', data=data)


@app.route('/user/makeorg/<int:user_id>')
def make_org(user_id):
    if session["username"] == "admin":
        user = UsersModel.query.filter_by(id=user_id).first()
        user.isOrg = not user.isOrg
        db.session.commit()
        return redirect('/user/list')
    return redirect('/login')


def dts(x):
    return x.date.strftime("%d.%m.%Y %H:%M:%S")



@app.route('/place/list')
def places_list():
    if 'username' not in session or session["username"] != 'admin':
        return redirect('/index')
    data = list(map(lambda x: [x.id, x.title, x.content, x.lat, x.lon, dts(x),
                               getusername(x.author)],
                    PlaceModel.query.all()))
    return render_template(
        'places_list.html', title='Информация о вечеринках', data=data)


def getusername(uid):
    us = UsersModel.query.filter_by(id=uid).first()
    return us.user_name


@app.route('/place/add', methods=['GET', 'POST'])
def addplace():
    if "username" not in session or session["username"] != 'admin':
        return redirect('/login')
    form = PlaceAddForm()
    form.author.choices = usernamesToJson()
    if form.validate_on_submit():
        link = form.content.data
        if "https://" not in link:
            link = "https://" + link
        place = PlaceModel(
            title=form.title.data,
            content=link,
            lat=form.lat.data,
            lon=form.lon.data,
            date=form.dt.data,
            author=form.author.data)
        db.session.add(place)
        db.session.commit()
        return redirect('/place/list')
    pft = 'Добавление нового места'
    pg = 'placeform.html'
    tit = 'Добавить место'
    return render_template(pg, title=tit, form=form, placeformtitle=pft)


@app.route('/place/edit/<int:place_id>', methods=['GET', 'POST'])
def editplace(place_id):
    if "username" not in session or session["username"] != 'admin':
        return redirect('/login')
    ed_place = PlaceModel.query.filter_by(id=place_id).first()
    form = PlaceAddForm()
    form.author.choices = usernamesToJson()
    if form.validate_on_submit():
        ed_place.title = form.title.data
        ed_place.content = form.content.data
        ed_place.lat = form.lat.data
        ed_place.lon = form.lon.data
        ed_place.date = form.dt.data
        ed_place.author = form.author.data
        db.session.commit()
        return redirect('/index')
    pft = 'Изменить информацию о месте'
    pg = 'placeform.html'
    tit = 'Добавить место'
    return render_template(pg, title=tit, form=form, pid=place_id,
                           placeformtitle=pft)


@app.route('/place/delete/<int:place_id>', methods=['GET', 'POST'])
def deleteplace(place_id):
    if "username" not in session or session["username"] != 'admin':
        return redirect('/login')
    p = PlaceModel.query.filter_by(id=place_id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect('/place/list')


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')


@app.route('/api/places/all', methods=['GET', 'POST'])
def getplaces():
    data = request.args
    date = data.get('date', 0)
    try:
        if date:
            date = datetime.strptime(date, "%Y,%m,%d").date()
            return jsonify(placestojson(date))
    except Exception as e:
        print(e)
    return jsonify(placestojson())


@app.route('/api/pid<int:place_id>', methods=['GET'])
def getplace(place_id):
    return jsonify(placetojson(place_id))


@app.route('/api/user/all', methods=['GET'])
def user_all():
    pw = request.args.get("pw")
    if pw and pw == "1048596":
        return jsonify(usernamesToJson())
    return jsonify([session["username"]])


@app.errorhandler(404)
def e404(e):
    print(e)
    return render_template('404.html'), 404


def usernamesToJson():
    users = UsersModel.query.filter_by(isOrg=True).all()
    ls = []
    for u in users:
        ls.append((u.id, u.user_name))
    return ls


def booltorus(b):
    if b:
        return 'Да'
    return 'Нет'


def placestojson(date=False):
    places = PlaceModel.query.all()
    if places:
        col = places[0].__table__.columns
        d = []
        for p in places:
            if (not date) or (date and p.date.date() == date):
                d.append(compilejson(p, col))
        return d
    return []


def placetojson(place_id):
    place = PlaceModel.query.filter_by(id=place_id).first()
    if place:
        col = place.__table__.columns
        return [compilejson(place, col)]
    return []


def compilejson(place, col):
    s = {}
    for column in col:
        s[column.name] = str(getattr(place, column.name))
    s['shortlink'] = str(getattr(place, 'content')).split('/')
    s['shortlink'] = s['shortlink'][0].replace('www.', '')
    s['dt'] = dts(place)
    return s


def getAvat(user, avtype='png', username=False):
    if username:
        user_id = user
    else:
        user_id = str(user.id)
    if exists(join(apath, 'static', 'img', user_id + '_av.' + avtype)) or \
       exists(join('static', 'img', user_id + '_av.' + avtype)):
        return join('static', 'img', user_id + '_av.' + avtype)
    else:
        return join('static', 'img', 'default_av.png')


def addZero(x, nlen=2):
    x = str(x)
    while len(x) < nlen:
        x = '0' + x
    return x


if __name__ == '__main__':
    dbinit()
    app.run(host='0.0.0.0')
