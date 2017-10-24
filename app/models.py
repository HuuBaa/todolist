#!/usr/bin/env python
#-*- coding: utf-8 -*-
from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import  request
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.Text, nullable=False)
    finished = db.Column(db.Boolean, default=False)
    share = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_time = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        import forgery_py
        from random import seed, randint
        seed()
        user_count = User.query.count()
        for i in range(count):
            user = User.query.offset(randint(0, user_count - 1)).first()
            t = Tasks(summary=forgery_py.lorem_ipsum.sentence(),
                      finished=True,
                      share=True,
                      user=user,
                      post_time=forgery_py.date.date(True)
                      )
            db.session.add(t)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def to_json(self):
        json_task={
            'id':self.id,
            'summary':self.summary,
            'post_time':self.post_time,
            'share':self.share,
            'finished':self.finished,
            'user_id':self.user_id,
            'user_name':self.user.user_name,
            'user_gravatar':self.user.gravatar(size=40)
        }
        return json_task


class User(UserMixin,db.Model):

    def __init__(self,**kw):
        super(User, self).__init__(**kw)

        if self.user_email is not None and self.avatar_hash is None:
            self.avatar_hash=hashlib.md5(self.user_email.encode('utf-8')).hexdigest()

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    user_email = db.Column(db.String(128), unique=True, index=True)
    user_password = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Tasks', backref='user', lazy='dynamic')
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_hash=db.Column(db.String(32))
    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        import forgery_py
        from random import seed
        seed()
        for i in range(count):
            u = User(user_name=forgery_py.internet.user_name(),
                     user_email=forgery_py.internet.email_address(),
                     user_password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     member_since=forgery_py.date.date(True)
                     )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def gravatar(self, size=100, default='retro', rating='g'):
        if request.is_secure:
            url = 'https://www.gravatar.com/avatar/'
        else:
            url = 'http://www.gravatar.com/avatar/'
        hash = self.avatar_hash or hashlib.md5(self.user_email.encode('utf-8')).hexdigest()
        return '{url}{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default,
                                                      rating=rating)

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self,password):
        self.user_password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.user_password,password)

    def to_json(self):
        json_user={
            'user_id':self.user_id,
            'user_name':self.user.user_name,
            'user_gravatar':self.user.gravatar(size=100),
            'member_since':self.member_since
        }
        return json_task
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))