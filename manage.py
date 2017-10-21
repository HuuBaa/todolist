#!/usr/bin/env python
#-*- coding: utf-8 -*-
from app import create_app,db
from app.models import User,Tasks
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app=create_app('default')
manager=Manager(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()