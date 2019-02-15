# -*- coding: utf-8 -*-

'''controller这个模块存放视图函数'''

from __future__ import unicode_literals

from flask import Blueprint

task_bp = Blueprint('task', __name__)

from controller import task
