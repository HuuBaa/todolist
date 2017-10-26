# -*- coding: utf-8 -*-
import os, re
from datetime import datetime
from fabric.api import *



env.user = 'root'
env.password = 'hubang1994.'
env.hosts = ['139.224.235.140']


_TAR_FILE='todolist.tar.gz'

def build():
    includes=['app','config.py','manage.py','requirements.txt','data-development.sqlite','migrations']
    excludes=['__pycache__','*.pyc','*.pyo']
    local('rm -f dist/%s'%_TAR_FILE)
    with lcd(os.path.abspath('.')):
        cmd=['tar','--dereference','-czvf','./dist/%s'%_TAR_FILE]
        cmd.extend(includes)
        cmd.extend(['--exclude=\'%s\''% ex for ex in excludes])
        local(' '.join(cmd))

_REMOTE_TMP_TAR='/tmp/%s'%_TAR_FILE
_REMOTE_BASE_DIR='/srv/todolist'
def deploy():
    newdir='todolist-%s'%datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    run('rm -f %s'%_REMOTE_TMP_TAR)
    put('dist/%s'%_TAR_FILE,_REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        run('mkdir %s'%newdir)
    with cd('%s/%s'%(_REMOTE_BASE_DIR,newdir)):
        run('tar -xzvf %s'%_REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        run('rm -rf todolist')
        run('ln -s %s todolist'%newdir)

def host_type():
    run('uname -s')