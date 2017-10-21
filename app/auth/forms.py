#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,Regexp
from wtforms import ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    email=StringField('邮箱',validators=[Email(),DataRequired(),Length(1,64)])
    username=StringField('用户名',validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须以字母开头，只能包含字母、数字、点、下划线')])
    password=PasswordField('密码',validators=[DataRequired(),EqualTo('password2',message='两次输入密码不一致')])
    password2=PasswordField('确认密码',validators=[DataRequired()])
    submit=SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError('邮箱已经注册')

    def validate_username(self,field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('用户名已经被使用')


class CPasswdForm(FlaskForm):
    oldpasswd=PasswordField('旧密码',validators=[DataRequired()])
    newpasswd=PasswordField('新密码',validators=[DataRequired(),EqualTo('newpasswd2',message='两次输入密码不一致')])
    newpasswd2=PasswordField('重新输入新密码',validators=[DataRequired()])
    submit=SubmitField('修改密码')