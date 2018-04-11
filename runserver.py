# _*_ coding: utf-8 _*_
from flask import Flask, make_response, jsonify
from showme.model import views
from showme.Utils import utils
#创建项目对象
app = Flask(__name__)
app.register_blueprint(views, url_prefix='/api')
app.register_blueprint(utils, url_prefix='/api')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"message": "没有找到资源", "result": {}, "code": 404}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"message": "请求无效", "result": {}, "code": 400}), 400)

if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', port=5000, debug=True)