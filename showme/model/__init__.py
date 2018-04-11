# _*_ coding: utf-8 _*_
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api

## 业务层代码
from User import UserList, User, UserFile
from Article import ArticleList, Article

views = Blueprint('views', __name__)

CORS(views)

api = Api()
api.init_app(views)

@views.route('/')
def show():
    return "hello views"


# UserList
api.add_resource(UserList, '/users')

# User
api.add_resource(User, '/user/<string:todo_id>', '/user')

# UserFile
api.add_resource(UserFile, '/file/<avatarname>')

api.add_resource(ArticleList, '/articles')

api.add_resource(Article, '/article/info')