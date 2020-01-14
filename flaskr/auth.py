#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/1/8 16:09
# @Author: CHEN MIAOMIAO

'''
认证(验证)蓝图： 包括注册新用户、登录和注销视图
'''

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db



# 注册到蓝图
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册视图
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 直接默认先清除用户session； 防止登录成功以后，再手动打开注册页，头部还带用户信息。
    if g.user is not None:
        session.clear()
        g.user = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.login'))    # 注册成功， 重定向到登录视图
        flash(error)

    return render_template('auth/register.html')




# 登录视图
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 先判断是否是已经登录的状态，如果是，直接跳转到首页
    if g.user is not None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)

    return render_template('auth/login.html')




# 注册一个在视图函数之前运行的函数，不论其URL是什么
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



# 注销视图
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



# 在其他视图中使用认证（验证）蓝图， 比如只有用户登录以后才能创建、编辑和删除博客帖子
# 使用装饰器
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(*args, **kwargs)
    return wrapped_view




