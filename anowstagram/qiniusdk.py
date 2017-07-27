#!/usr/bin/env/python
#-*- encoding:utf-8 -*-
from anowstagram import app
from qiniu import Auth,put_stream,put_data,put_file
import os

#需要填写你的Access Key 和 Secret Key
access_key=app.config['QINIU_ACCESS_KEY']
secret_key=app.config['QINIU_SECRET_KEY']

#构建鉴权对象
q=Auth(access_key,secret_key)


#需要上传的空间
bucket_name = app.config['QINIU_BUCKET_NAME']
domain_prefix = app.config['QINIU_DOMAIN']

def qiniu_upload_file(source_file,save_file_name):
    token = q.upload_token(bucket_name,save_file_name)
    #ret,info = put_stream(token,save_file_name,source_file.stream,"qiniu",source_file.stream.tell())
    #os.fstat(source_file.stream.fileno()).st_size)
    #save_dir=app.config['UPLOAD_DIR']
    #file_path = os.path.join(save_dir,save_file_name)
    #print file_path
    #source_file.save(file_path)
    ret,info = put_data(token,save_file_name,source_file.stream)
    print type(info.status_code),info
    if info.status_code == 200:
	return domain_prefix+save_file_name
    return None

	
