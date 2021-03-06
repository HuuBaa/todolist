#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import  render_template,jsonify,request,redirect,url_for,flash
from . import todo
from ..models import User,Tasks
from flask_login import  login_required,current_user
from app import db
@todo.route('/')
def index():
    return render_template('todo/index.html')

#主页ajax获取share task
@todo.route('/todo/shared')
def todo_shared():
    page=request.args.get('page',1,type=int)

    pagnation=Tasks.query.filter_by(share=True).order_by(Tasks.post_time.desc()).paginate(page,8)
    page_items = pagnation.items

    tasks_list=[ task.to_json() for task in page_items]
    iter_pages=list(pagnation.iter_pages(2,2,3,2))

    return jsonify({
        'tasks':tasks_list,
        'page':pagnation.page,
        'prev_num' : pagnation.prev_num,
        'next_num' : pagnation.next_num,
        'has_next':pagnation.has_next,
        'has_prev':pagnation.has_prev,
        'pages':pagnation.pages,
        'iter_pages':iter_pages
    })


@todo.route('/mytasks')
def mytasks():
    return render_template('todo/mytasks.html')

#mytaks页面 ajax 创建task

@todo.route('/todo/createtask',methods=['POST'])
@login_required
def tasks_create():
    if request.method=='POST':
        data=request.get_json()
        if data['create_task'].strip() !='':
            new_task=Tasks(summary=data['create_task'],user=current_user._get_current_object())
            db.session.add(new_task)
            db.session.commit()
            return  jsonify({'status':'ok'})
        else:
            return jsonify({'status': 'empty'})

#ajax获取已完成、未完成事项

@todo.route('/todo/mytask', methods=['GET'])
@login_required
def mytasks_json():
    if request.method=='GET' :
        finished=request.args.get('finished',None,int)
        if finished == 0:
            user_tasks_list = [task.to_json() for task in current_user.tasks.order_by(Tasks.post_time.desc()).filter(Tasks.finished==False).all()]
            finished_count=current_user.tasks.filter(Tasks.finished==True).count()
            unfinished_count=current_user.tasks.filter(Tasks.finished==False).count()
            return jsonify({
                'tasks':user_tasks_list,
                'finished_count':finished_count,
                'unfinished_count':unfinished_count
            })
        elif finished == 1:
            user_tasks_list = [task.to_json() for task in current_user.tasks.order_by(Tasks.post_time.desc()).filter(
                Tasks.finished == True).all()]
            finished_count = current_user.tasks.filter(Tasks.finished == True).count()
            unfinished_count = current_user.tasks.filter(Tasks.finished == False).count()
            return jsonify({
                'tasks': user_tasks_list,
                'finished_count': finished_count,
                'unfinished_count': unfinished_count
            })


@todo.route('/todo/delete/<int:task_id>')
@login_required
def del_task(task_id):

    task=Tasks.query.filter_by(id=task_id).first()
    if task and task.user==current_user:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'status':'del_ok'})
    else:
        return jsonify({'status':'forbidden'})


@todo.route('/todo/share/<int:task_id>')
@login_required
def share_task(task_id):
    task=Tasks.query.filter_by(id=task_id).first()
    if task and task.user==current_user:
        task.share=True
        db.session.add(task)
        db.session.commit()
        return jsonify({'status':'share_ok'})
    else:
        return jsonify({'status':'forbidden'})



@todo.route('/todo/unshare/<int:task_id>')
@login_required
def unshare_task(task_id):
    task=Tasks.query.filter_by(id=task_id).first()
    if task and task.user==current_user:
        task.share=False
        db.session.add(task)
        db.session.commit()
        return jsonify({'status':'unshare_ok'})
    else:
        return jsonify({'status':'forbidden'})


@todo.route('/todo/finished/<int:task_id>')
@login_required
def finished_task(task_id):
    task=Tasks.query.filter_by(id=task_id).first()
    if task and task.user==current_user:
        task.finished=True
        db.session.add(task)
        db.session.commit()
        return jsonify({'status':'finished_ok'})
    else:
        return jsonify({'status':'forbidden'})


@todo.route('/todo/unfinished/<int:task_id>')
@login_required
def unfinished_task(task_id):
    task=Tasks.query.filter_by(id=task_id).first()
    if task and task.user==current_user:
        task.finished=False
        db.session.add(task)
        db.session.commit()
        return jsonify({'status':'unfinished_ok'})
    else:
        return jsonify({'status':'forbidden'})

@todo.route('/user/<int:id>')
def user_pro(id):
    user=User.query.get_or_404(id)
    tasks=user.tasks.filter_by(share=True).all()
    return  render_template('/todo/userpro.html',user=user,tasks=tasks)
