#Загрузка библиотек для работы с базой данных
import re
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey
import datetime #Загрузка библиотеки для работы с датой и временем
import os #Загрузка библиотеки для работы с файлами
#Загрузка библиотеки Flask и расширений этой бибилотеки
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask import Flask,render_template, request, flash, redirect, url_for, send_from_directory
#Загрузка библиотек для защиты файлов
from werkzeug.security import generate_password_hash, check_password_hash

db_string = "postgresql://postgres:123@localhost/CinemaSite" #адрес подключения к БД
dbEngine = create_engine(db_string) #создание класса базы данных

app = Flask( __name__ )
app.secret_key = 'veryveryveryHardSecretKey' #создание ключа для шифрования данных
app.config['SQLALCHEMY_DATABASE_URI'] = db_string #опредления встроенного в Flask базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app) #Создание экземпляра базы данных
manager = LoginManager(app) #Создание менеджера логинов
Session = sessionmaker(db) #Создание сессии сайта
session = Session()

db.create_all() #создание элементов базы даных
db.session.commit()

#Функции для работы с базой данных
def get_filmList():
    request = dbEngine.execute(f'SELECT * FROM "Films"') #запрос к базе данных для получения списка фильмов
    filmList = request.fetchall()
    return filmList

def filter_filmList_Genre(genreID): #функция для фильтрации списка фильмов по жанру
    request = dbEngine.execute(f'SELECT * FROM "Films" WHERE genre_id = {genreID}') #запрос к базе данных для вывода фильмов определенного жанра
    filmList = request.fetchall()
    return filmList

def get_filmInfo(filmID): #функция для информации о фильме
    request = dbEngine.execute(f'SELECT * FROM "Films" WHERE id = {filmID}') #запрос к базе данных для получения данных фильма
    filmData = request.fetchall()
    return filmData

def get_filmSessions(filmID): #функция для получения сеансов фильма
    request = dbEngine.execute(f'SELECT * FROM "Sessions" WHERE film_id = {filmID}')  # запрос к базе данных на получение сеансов фильма
    filmSessions = request.fetchall()
    return filmSessions

def get_placesForSession(sesionID):
    session = dbEngine.execute(f'SELECT * FROM "Sessions" WHERE id = {sesionID}').fetchone() #получение данных сеанса в зале
    rowsList = dbEngine.execute(f'SELECT * FROM "Rows" WHERE hall_id = {session.hall_id}').fetchall() #получение рядов в зале
    for
    request = dbEngine.execute(f'SELECT * FROM "Shedule" WHERE film_id = {id}')  #получение мест
    places = request.fetchall()
    return places

#блок функций для обработки адресных путей
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def mainPage():
    return render_template("index.html")

@app.route('/about') #вывод страницы cо справочной информацией
def aboutPage():
    return render_template("about.html")

@app.route('/filmList', methods=['GET', 'POST']) #вывод страницы c афишей кинотеатра
def filmListPage():
    return render_template("filmList.html")

@app.route('/filmList/<filmID>', methods=['GET', 'POST']) #вывод страницы c информацией о выбранном фильме
def filmInfo(filmID):
    return render_template("filmInfo.html")

@app.route('/sessions/<filmID>', methods=['GET', 'POST']) #вывод страницы с сеансами выбранного фильма
def filmSessions(filmID):
    return render_template("filmSessions.html")

@app.route('/placesForSession/<sessionID>', methods=['GET', 'POST']) #вывод страницы c местами в кинозале
def sessionPlaces(sessionID):
    return render_template("places.html")

@app.route('/buyTicket/<placeID>', methods=['GET', 'POST']) #вывод страницы покупки билета
def buyTicket():
    return render_template("buy.html")

@app.route('/uploads/<name>') #загрузка файла на сервер
def download_file(name):
    print(send_from_directory(app.config["UPLOAD_FOLDER"], name)) #вывод информации о файле в консоль
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/registration', methods=['GET', 'POST'])
def registrationPage():
    #получение данных из формы на сайте
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    telephone = request.form.get('telephone')
    fio = request.form.get('fio')
    biography = request.form.get('biography')
    email = request.form.get('email')
    discipline = request.form.get('discipline')
    birth_date = request.form.get('birth_date')
    if request.method == 'POST':

        else:
            hash_pwd = generate_password_hash(password)  # Хеширование пароля
            new_user = Repetitors(login=login, password=hash_pwd, email=email,biography=biography,fio=fio,discipline_id=discipline.id,birth_date=birth_date) #Добавление нового пользователя
            db.session.add(new_user)
            db.session.commit() #сохранение изменений
            return redirect(url_for('mainPage'))
    return render_template("registration.html")




