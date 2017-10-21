#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import  render_template,jsonify,request
from . import todo
from ..models import User,Tasks

@todo.route('/')
def index():
    return render_template('todo/index.html')

@todo.route('/todo/shared')
def todo_shared():
    page=request.args.get('page',1,type=int)

    pagnation=Tasks.query.filter_by(share=True).order_by(Tasks.post_time.desc()).paginate(page,15)
    page_items = pagnation.items

    tasks_list=[ task.to_json() for task in page_items]
    iter_pages=list(pagnation.iter_pages(2,1,2,2))

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


