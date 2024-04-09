from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from main import db
from main import app

#manager = LoginManager(app)
#class User (db.Model, UserMixin):
    #id = db.Column(db.Integer, primary_key=True)
    #login = db.Column(db.String(128), nullable=True, unique=True)
    #password = db.Column(db.String(255), nullable=False)

