#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask,render_template
from config import config
from flask_sqlalchemy import  SQLAlchemy
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='auth.login'
db=SQLAlchemy()
moment=Moment()
mail=Mail()
bootstrap=Bootstrap()
def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from .todo import todo
    app.register_blueprint(todo)
    from .auth import auth
    app.register_blueprint(auth)

    return app

