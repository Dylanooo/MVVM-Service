# _*_ coding: utf-8 _*_
from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api
from FileManager import FileManager


utils = Blueprint('utils', __name__)

CORS(utils)

api = Api()
api.init_app(utils)

@utils.route('/')
def show():
    return "hello views"

# 文件管理工具
api.add_resource(FileManager, '/user/avatar/<filename>')