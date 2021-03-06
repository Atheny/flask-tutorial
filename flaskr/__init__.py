#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/12/31 16:54
# @Author: CHEN MIAOMIAO

import os
from flask import Flask
from flask.views import View

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # # @app.route('/index')
    # def index():
    #     return '登录成功。'

    from . import db, auth, blog
    db.init_app(app)   # 将数据库注册到应用
    app.register_blueprint(auth.bp)  # 将登录蓝图注册到应用
    app.register_blueprint(blog.bp)  # 将博客蓝图注册到应用
    app.add_url_rule('/', endpoint='index')

    return app