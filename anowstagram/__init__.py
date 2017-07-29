#!/usr/bin/env/python
# -*- encoding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


#*************************************#
#Added by Jia on 2017/7/29
from flask_mail import Mail
#*************************************#



app = Flask(__name__)

app.config.from_pyfile('app.conf')
app.secret_key = 'nowcoder'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = '/regloginpage/'

from anowstagram import views, models



