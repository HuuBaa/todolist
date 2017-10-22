#!/usr/bin/env python
#-*- coding: utf-8 -*-
from . import auth
from ..models import User
from flask import request,redirect,url_for,render_template,flash
from flask_login import login_user,login_required,logout_user,current_user
from .forms import RegisterForm,CPasswdForm
from app import db
@auth.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(user_email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user,True)
            flash('登录成功!')
            return redirect(url_for('todo.mytasks'))
        else:
            flash('账号、密码错误!')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')



@auth.route('/register',methods=['POST','GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user = User(user_email=form.email.data, user_name=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)
@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('todo.index'))


@auth.route('/cpasswd',methods=['POST','GET'])
@login_required
def cpasswd():
    form=CPasswdForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpasswd.data):
            current_user.password=form.newpasswd.data
            db.session.add(current_user)
            db.session.commit()
            logout_user()
            flash('修改密码成功，请重新登录')
            return redirect(url_for('auth.login'))
        else:
            flash('旧密码错误')
    return render_template('auth/cpasswd.html',form=form)