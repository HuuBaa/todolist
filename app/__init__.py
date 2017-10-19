#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask,render_template
from config import config
from flask_sqlalchemy import  SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
db=SQLAlchemy()
moment=Moment()
mail=Mail()
def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    from .todo import todo
    app.register_blueprint(todo)

    return app

