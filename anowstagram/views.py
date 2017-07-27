#!/usr/bin/env/ python
# -*- encoding:utf-8 -*-

from anowstagram import app,db
from models import Image,User,Comment
from flask import render_template,redirect,request,flash,get_flashed_messages
import random,hashlib,json
from flask_login import login_user,logout_user,current_user,login_required
from qiniusdk import qiniu_upload_file


import sys,uuid,os
reload(sys)
sys.setdefaultencoding('utf-8')





@app.route('/')
def index():
    #return 'Hello'
    images=Image.query.order_by(Image.id.desc()).limit(10).all()
    return render_template('index.html',images=images)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user==None:
	return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1,per_page=3,error_out=False)
    
    return render_template('profile.html',user=user,images=paginate.items,has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id,page,per_page):
    paginate = Image.query.filter_by(user_id = user_id).paginate(page=page,per_page = per_page)
    map = {'has_next':paginate.has_next}
    images =[]
    for image in paginate.items:
        imavo={'id':image.id,'url':image.url,'comment_count':len(image.comments)
}
	images.append(imavo)
    map['image']=images
    return json.dumps(map)






@app.route('/image/<int:image_id>/')
def image(image_id):
    image=Image.query.get(image_id)
    if image==None:
	return redirect('/')
    return render_template('pageDetail.html',image=image)

@app.route('/regloginpage/',methods={'post','get'})
def regloginpage(msg=''):
    
    for m in get_flashed_messages(with_categories=False,category_filter=['reglogin']):
	msg = msg+m
    return render_template('login.html',msg=msg,next=request.values.get('next'))



def redirect_message(target,msg,category):
    if msg!=None:
	flash(msg,category=category)
    return redirect(target)

@app.route('/login/',methods={'post','get'})
def login():
    
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username=='' or password=='':	
	return redirect_message('/regloginpage','用户名和密码不能为空','reglogin')
    user = User.query.filter_by(username = username).first()
    if user==None:
	return redirect_message('/regloginpage','用户名不存在','reglogin')

    m=hashlib.md5()
    m.update(password+user.salt)
    if (user.password != m.hexdigest()):
	return redirect_message('/regloginpage','密码错误','reglogin')

    login_user(user)

    #current_user#
    print current_user.id,current_user.username
    #current_user#

    next=request.values.get('next')
    if next!=None and next.startswith('/'):
	return redirect(next)


    return redirect('/')



@app.route('/reg/',methods={'post','get'})
def reg():
    #request.args
    #request.form
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username=='' or password=='':	
	return redirect_message('/regloginpage','用户名和密码不能为空','reglogin')
    user = User.query.filter_by(username = username).first()
    if user!=None:
	return redirect_message('/regloginpage','用户名已经存在','reglogin')
	
    #更多判断
    
    salt='.'.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()
    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)


    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()

    #current_user#
    print current_user.is_authenticated
    #current_user#

    return redirect('/')


def save_to_local(file,file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir,file_name))
    return '/image/'+file_name


@app.route('/image/<image_name>')
def view_image():
    return send_from_directory(app.config['UPLOAD_DIR'],image_name)



@app.route('/upload/',methods={"post"})
def upload():
    #print type(request.files)
    #print request.files
    file = request.files['file']
    #print dir(file)
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.')[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
	file_name = str(uuid.uuid1()).replace('-','')+'.'+file_ext
        
	
	#current_user#
        if not current_user.is_authenticated:
	    return 'None'#current_user.is_authenticated # ,current_user.name
	#current_user#


	#url = save_to_local(file,file_name)
	url = qiniu_upload_file(file,file_name)
	

        if url != None:
	    db.session.add(Image(url,current_user.id))
	    db.session.commit()
        
    return redirect('/profile/%d' % current_user.id)
    return 'OK'


@app.route('/addcomment/',methods={'post'})
def add_comment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content,image_id,current_user.id)
    db.session.add(comment)
    db.session.commit()
    return json.dumps({"code":0,"id":comment.id,
		       "content":content,
		       "username":comment.user.username,
		       "user_id":comment.user.id})

