#!/usr/bin/env python
#-*- coding: utf-8 -*-
from . import  db

class Tasks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    summary=db.Column(db.String(64),nullable=False)
    finished=db.Column(db.Boolean,default=False)
    share=db.Column(db.Boolean,default=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(64))
    user_email=db.Column(db.String(128),unique=True,index=True)
    user_password=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)
    admin=db.Column(db.Boolean,default=False)
    tasks=db.relationship('Tasks',backref='user',lazy='dynamic')

