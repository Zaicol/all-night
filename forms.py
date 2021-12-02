from flask import session
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     SelectField, DateTimeField)
from wtforms.validators import (DataRequired, ValidationError, EqualTo,
                                StopValidation)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models import UsersModel


forbidden_names = ['admin', 'default', 'Zaicol']
MAX_FILE_SIZE = 1024 * 1024 * 8 * 4 + 1


def user_check(form, field):
    if form.username.data:
        check = UsersModel.query.filter_by(
            user_name=form.username.data).first()
        if check:
            if not check_password_hash(check.password_hash, field.data):
                raise ValidationError(
                    'Неверный пароль')
        else:
            raise ValidationError('Такого пользователя не существует')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[
                           DataRequired('Заполните это поле')])
    password = PasswordField(
        'Пароль', validators=[
            DataRequired('Заполните это поле'), user_check])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


def name_check(form, field):
    if UsersModel.query.filter_by(user_name=field.data).first():
        raise ValidationError('Пользователь с таким логином уже существует')
    return form


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[
                           DataRequired('Заполните это поле'), name_check])
    password = PasswordField(
        'Пароль', validators=[
            DataRequired('Заполните это поле')])
    password_rep = PasswordField('Подтверждение пароля',
                                 validators=[
                                     DataRequired('Заполните это поле'),
                                     EqualTo('password', 'Пароли не совпадают')
                                 ])
    submit = SubmitField('Зарегистрироваться')


def size_check(form, field):
    file = field.data
    file_bytes = file.read(MAX_FILE_SIZE)
    if len(file_bytes) == MAX_FILE_SIZE:
        raise StopValidation('Превышен максиммальный размер файла')
    return form


class AvatarForm(FlaskForm):
    avatar = FileField('Новый аватар', validators=[
                       FileRequired('Необходимо выбрать файл'),
                       FileAllowed(['jpg', 'png', 'gif'],
                                   'Расширение файла не является допустимым'),
                       size_check])
    submit_av = SubmitField('Сохранить')


def exist_check(form, field):
    if UsersModel.query.filter_by(user_name=field.data).first():
        raise ValidationError('Пользователь с таким логином уже существует')
    elif field.data in forbidden_names and session['user_id'] != 1:
        raise ValidationError('Использование данного имени запрещено')
    return form


class ChangeUsernameForm(FlaskForm):
    new_name = StringField('Новый логин', validators=[
                           DataRequired('Введите новый логин'),
                           exist_check])
    submit_us = SubmitField('Сохранить')


def oldpass_check(form, field):
    user = UsersModel.query.filter_by(id=session["user_id"]).first()
    if not check_password_hash(user.password_hash, field.data):
        raise ValidationError('Неверный пароль')
    return form


class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Старый пароль', validators=[
        DataRequired('Введите старый пароль'),
        oldpass_check])
    password = PasswordField('Новый пароль', validators=[
        DataRequired('Введите новый пароль')])
    password_rep = PasswordField('Подтверждение пароля', validators=[
        DataRequired('Повторно введите новый пароль'),
        EqualTo('password', 'Пароли не совпадают')])
    submit_pass = SubmitField('Сохранить')


class PlaceAddForm(FlaskForm):
    title = StringField('Название места*', validators=[
        DataRequired('Заполните это поле')])
    content = StringField('Ссылка*', validators=[
        DataRequired('Заполните это поле')])
    dt = DateTimeField('Время проведения*', format='%d.%m.%Y %H:%M:%S',
                       validators=[
                           DataRequired('Заполните это поле')])
    author = SelectField('Организатор*', validators=[
        DataRequired('Заполните это поле')])
    search = StringField('Адрес', validators=[])
    lat = StringField('Широта*', validators=[
        DataRequired('Заполните это поле')])
    lon = StringField('Долгота*', validators=[
        DataRequired('Заполните это поле')])
    submit = SubmitField('Добавить место')
