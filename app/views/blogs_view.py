#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   view.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/26 下午6:29   wangshuai      1.0         None
'''

# import lib
import os
import oss2
from flask import request, jsonify
from app import app, db
from app.libs.ustils import sysTime_ymdhm
from app.models.blogs import Notes
from datetime import datetime


@app.route('/publish', methods=['POST'])
def publish():
    resData = request.json
    notestype_id = resData.get('notestype')
    title = resData.get('title')
    seo_link = resData.get('seo_link')
    body_html = resData.get('body_html')
    notesState = resData.get('notesState')
    blogs_type = resData.get('blogs_type')
    user_id = resData.get('user_id')
    notesID = resData.get('notesID')  # 当前笔记id
    blogs_type = True if blogs_type != 'false' else False
    try:
        if notesID:  # 存在
            notes = db.session.query(Notes).filter(Notes.userId == int(user_id), Notes.id == int(notesID)).first()
            notes.title = title
            notes.seo_link = seo_link
            notes.body_html = body_html
            notes.alter_time = sysTime_ymdhm()
            notes.notesState = notesState
            notes.notestype_id = notestype_id
            notes.notes_private = blogs_type
            db.session.commit()
        else:
            notesT = Notes(notestype_id=notestype_id, title=title, seo_link=seo_link, body_html=body_html,
                           notesState=notesState, userId=int(user_id), create_time=sysTime_ymdhm(),
                           alter_time=sysTime_ymdhm(), notes_private=blogs_type)
            db.session.add(notesT)
            db.session.commit()
    except BaseException as e:
        print('异常', e)
        db.session.rollback()
    return jsonify({'status': 0})


@app.route('/uploads', methods=['POST'])
def uploads():
    auth = oss2.Auth(app.config['OSS_KEY'], app.config['OSS_SECRET'])
    bucket = oss2.Bucket(auth, app.config['OSS_URL'], app.config['OSS_NAME'])
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        sys_path = (app.config['OSS_IMGSNAME'] if ex != '.mp4' else app.config['OSS_VIDEO'])
        imgpath = os.getcwd() + app.config['STATIC_UPLOAD_PATH']
        file.save(imgpath + "{}".format(filename))
        copy_imgUrl = imgpath + filename
        response = bucket.put_object_from_file(sys_path + filename,
                                               os.path.join(imgpath, filename))
        public_imgUrl = app.config['USER_IP'] + sys_path + filename
        if ex != '.gif' and ex != '.mp4':
            public_imgUrl += app.config['IMGS_TYPE']
    if response.status != 200:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        res = {
            'success': 1,
            'message': '上传成功',
            'url': public_imgUrl,
        }
    os.remove(copy_imgUrl)
    return jsonify(res)
