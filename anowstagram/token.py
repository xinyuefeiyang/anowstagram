#!/usr/bin/env/ python
#-*-encoding:utf-8 -*-
#*****************************#
#Add by Jia on 2017/7/27
from itsdangerous import URLSafeTimedSerializer
from anowstagram import app
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email,salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token,expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
	email = serializer.loads(token,salt=app.config['SECURITY_PASSWORD_SALT'],max_age = expiration)
    except:
	return False
    return email







#****************************#