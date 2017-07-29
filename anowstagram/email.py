#!/usr/bin/env/ python
#-*- encoding:utf-8 -*-

#*******************************#
#Added by Jia on 2017/7/29
from flask_mail import  Mail,Message
from anowstagram import app

mail = Mail(app)

def send_mail(to,subject,template):
    msg = Message(subject,[to],html=template,sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)


#******************************#
