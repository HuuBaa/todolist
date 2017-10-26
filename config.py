#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='HUU IS COOL'
    FLASK_MAIL_SUBJECT_PREFIX = '[任务村]'
    FLASK_MAIL_SENDER = '任务村 <742790905@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    BOOTSTRAP_SERVE_LOCAL=True

class DevelopmentConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-development.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-production.sqlite')

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

config={'default':DevelopmentConfig,
        'development':DevelopmentConfig,
        'production':ProductionConfig,
        'test':TestConfig}