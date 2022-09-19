
import numpy as np
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import Flask, url_for, render_template, request, redirect
import os 
from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    mail = Mail()
    app = Flask(__name__)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'newpythontestapp@gmail.com'
    app.config['MAIL_PASSWORD'] = 'yhvgoogijajxqfsi'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    mail.init_app(app)

    from views import views
    from auth import auth 
    from main import main 

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from models import User, Match

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run()
