# _*_ coding: utf-8 _*_

import os
#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/files/images'
#mongodb数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mongodb://localhost:27017/showme"
