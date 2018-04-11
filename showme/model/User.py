#coding=utf-8
from bson import ObjectId
import os
import uuid
from flask_restful import Resource, reqparse, request, fields, marshal_with
from showme.Utils.Database import db
from flask import send_from_directory, abort
import hashlib
import showme.config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




user_fields = {
    'name': fields.String(default=""),
    'gender': fields.Integer(default=0),
    'address': fields.String(default=""),
    'mobile': fields.String,
    'nickname': fields.String(default=""),
    'age': fields.Integer(default=0),
    'avatar': fields.String(default=""),
    '_id': fields.String
}

request_parser = reqparse.RequestParser()

for paramter in user_fields:
    request_parser.add_argument(paramter, type=str, required=(paramter == "mobile" or paramter == "password"))


response_fields = {
    'result': fields.Nested(user_fields, default={}),
    'code': fields.Integer,
    'message': fields.String
}


class UserList(Resource):
    def get(self):
        users = db.user.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return dict(result='success', userlist=user_list)

class User(Resource):
    # 获取用户信息
    @marshal_with(response_fields)
    def get(self):
        info_parser = request_parser.copy()
        info_parser.remove_argument('mobile')
        args = info_parser.parse_args()
        id = args['_id']
        user = db.user.find_one({'_id': ObjectId(id)})
        if user is not None:
            user['_id'] = str(user['_id'])
            return dict(message='success', code=0, result=user)
        return dict(message='failed', code=3, result=None)



    @marshal_with(response_fields)
    def post(self, todo_id):
        # 注册
        if todo_id == "register":
           return self.register()
        # 头像
        elif todo_id == "avatar":
           return self.update_avatar()
        # 登录
        elif todo_id == "login":
            return self.login()
        # 错误处理
        else:
            return dict(message="路径错误", code = 404, result = None)

    # 登录
    def login(self):
        # 获取入参
        login_parse = request_parser.copy()
        login_parse.add_argument('password', required=True)
        args = login_parse.parse_args()
        mobile = args['mobile']
        password = args['password']
        # 判断是否缺少必要参数
        if mobile is None or password is None:
            return dict(message="缺少必要参数", code=999, result=None)
        user = db.user.find_one({'mobile': mobile})
        # 判断用户是否注册
        if user is None:
            return dict(message="该手机号未注册", code=888, result=None)
        # 判断密码是否正确
        if user['password'] == hashlib.md5(password).hexdigest():
            user['_id'] = str(user['_id'])
            return dict(message="登陆成功", code=0, result=user)
        else:
            return dict(message="密码错误", code=777, result=None)

    # 更新头像
    def update_avatar(self):
        file = request.files['file']
        parser = request_parser.copy()
        parser.add_argument('_id', type=str, required=True)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        if file is None:
            return dict(message="上传失败，缺少文件", code=100, result=None)
        else:
            id = args['_id']
            extension = os.path.splitext(file.filename)[1]
            f_name = str(uuid.uuid4()) + extension
            path = os.path.join(showme.config.UPLOAD_FOLDER, f_name)
            file.save(path)
            file_url = request.host_url + "api/file/" + f_name
            db.user.update({'_id': ObjectId(id)}, {"$set": {'avatar': file_url}})
            user = db.user.find_one({'_id': ObjectId(id)})
            if user is not None:
                user["_id"] = id
            return dict(message='上传成功', code=0, result=user)
        abort(400)

    # 下载头像
    def download_avatar(self):
        args = self.reqparse.parse_args()
        filePath = args['avatar']
        if os.path.isfile(os.path.join('upload', filePath)):
            return send_from_directory('upload', filePath, as_attachment=True)
        abort(404)

    # 用户注册
    def register(self):
        register_parse = request_parser.copy()
        register_parse.add_argument('password',required=True)
        register_parse.remove_argument('_id')
        args = register_parse.parse_args()
        user = db.user.find_one({'mobile': args['mobile']})
        if user is not None:
            return dict(message="该手机号码已注册", code=3, result=None)

        password = args["password"]
        if password is not None:
            args["password"] = hashlib.md5(password).hexdigest()
        user_data = dict(args)
        user_id = db.user.insert_one(user_data).inserted_id
        user = db.user.find_one({'_id': user_id})
        if user is not None:
            user['_id'] = str(user['_id'])
            return dict(message='success', code=0, result=user)
        return dict(message='failed', code=3, result=None)



class UserFile(Resource):
    def get(self, avatarname):
        if os.path.isfile(os.path.join(showme.config.UPLOAD_FOLDER, avatarname)):
            return send_from_directory(showme.config.UPLOAD_FOLDER, avatarname, as_attachment=True)
        abort(404)










