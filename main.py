import sqlalchemy.orm

import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, login_manager
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'some secret code123@#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

manager = LoginManager(app)
manager.init_app(app)

# БД - Таблица - название
# Таблица
# id     title   price   isActive
# 1      Adidas  4490    True
# 2      Nike    5490    True
# 3      Puma    9900    False

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title

class User (db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=False)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route ('/')
def selection():
    return render_template('selection.html')

@app.route ('/index')
def Index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)

@app.route ('/about')
def About():
    return render_template('about.html')

@app.route ('/registration', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not (login and password and password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hashed_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hashed_pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('reg.html')


@app.route ('/login', methods=['POST', 'GET'])
def Login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect('/index')
            flash("Вы вошли как администратор")
        else:
            flash("Неверный пароль")
    else:
        flash("Вы не зарегистрированы")

    return render_template('log.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'вы вышли'

@app.route ('/buy/<int:id>')
@login_required
def Item_buy(id):
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": 3000
    }
    url = checkout.url(data).get('checkout_url')
    return str(id)

@app.route ('/create', methods = ['POST', 'GET'])
def Create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']

        item = Item(title=title, price=price, text=text)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/index')
        except:
            return "Получилась Ошибка"
    else:
        return render_template('create.html')

@app.route ('/<int:id>/update', methods = ['POST', 'GET'])
def Update(id):
    item = Item.query.get(id)
    if request.method == "POST":
        item.title = request.form['title']
        item.price = request.form['price']
        item.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/index')
        except:
            return "Получилась ошибка"
    else:

        return render_template('update.html', item=item)


@app.route ('/detailed/<int:id>')
def Detailed(id):
    return render_template('detail.html')

@app.route ('/<int:id>/delete')
def Del_Item(id):

    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/index')
    except:
        return "При удалении товара произошла ошибка"
@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('/login') + '?next=' + request.url)
    return response


if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)