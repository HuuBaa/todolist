#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import  render_template
from . import todo

@todo.route('/todo')
def todo():
    return render_template('todo/todolist.html')