#!/usr/bin/env/ python
# -*- encoding:utf-8 -*-

#*************************************#
#Adde by Jia on 2017/7/29


from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
	if current_user.confirmed is False:
	    flash('Please confirmed your account!','warning')
	    return redirect('/unconfirmed')
	return func(*args,**kwargs)
    return decorated_function

#************************************#
