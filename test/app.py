#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2020/1/3 11:19
# @Author: CHEN MIAOMIAO

from flask import Flask, current_app
from threading import Thread
from flask_mail import Message, Mail


class Email_Settings():
    MAIL_SERVER = 'smtp.163.com'  # 使用的邮箱服务器
    MAIL_PORT = 465  # 端口   支持SSL一般为465，默认为25
    MAIL_USE_SSL = True  # 是否支持SSL
    MAIL_USE_TLS = False  # 是否支持TLS
    MAIL_DEFAULT_SENDER = '15718886295@163.com'  # 默认发件人
    MAIL_USERNAME = '15718886295@163.com'  # 用户名
    MAIL_PASSWORD = '1993515cmm'  # 163邮箱客户端授权码，不是登录密码


app = Flask(__name__)
app.config.from_object(Email_Settings)

mail = Mail()
mail.init_app(app)



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:  # 附件
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:  # 同步
        mail.send(msg)
    else:  # 异步
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email():
    # 调用send_email函数
    send_email(subject='[Microblog] Reset Your Password', sender=Email_Settings.MAIL_USERNAME,
               recipients=['chenmiaomiao199305@163.com'], text_body='这是一封异步发送邮件。', html_body=r'<html><body><h1>内容：HTML-H1</h1></body></html>')

@app.route('/post_email', methods=['GET', 'POST'])
def post_email():
    send_password_reset_email()
    return '发送成功'