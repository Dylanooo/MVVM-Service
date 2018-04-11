#coding=utf-8

from flask_restful import Resource, reqparse, fields, marshal_with
from showme.Utils.Database import db
from bson import ObjectId

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


html_leading = '''
<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=0" />
            <meta name="apple-mobile-web-app-capable" content="yes" />
            <meta name="apple-mobile-web-app-status-bar-style" content="black" />
            <meta name="format-detection" content="telephone=no" />
            <meta name="format-detection" content="email=no" />
            <style>
            html{
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                text-size-adjust: 100%;
            }
            body, div, dl, dd, ul, ol,  h1, h2, h3, h4, h5, h6, pre, p, blockquote, hr,form, fieldset, legend, input, textarea, optgroup, select,article, aside, details,figcaption,figure,footer,header,hgroup, menu,nav,sectiontable, thead, tbody, tfoot, th, tr, td {
                margin: 0;
                padding: 0;
            }
            article,aside,details,figcaption,figure,footer,header,main,menu,nav,section,summary {
                display: block;
            }
            audio,canvas,video,progress {
                display: inline-block;
            }
            button,input,select,textarea {
                font-family: inherit;
                font-size: 100%;
                margin: 0;
                vertical-align: baseline;
            }
            mark {
                background-color: #ff0;
                color: #000;
            }
            sub,sup {
                font-size: 75%;
                line-height: 0;
                position: relative;
                vertical-align: baseline;
            }
            sub {
                bottom: -0.25em;
            }
            sup {
                top: -0.5em;
            }
            a:active,
            a:hover {
                outline-width: 0;
            }
            ul, ol {
                list-style:none;
            }
            [type="search"] {
                -webkit-appearance: textfield;
                outline-offset: -2px;
            }
            [type="search"]::-webkit-search-cancel-button,
            [type="search"]::-webkit-search-decoration {
                -webkit-appearance: none;
            }
            ::-webkit-file-upload-button {
                -webkit-appearance: button;
                font: inherit;
            }
            
            /*定制部分*/
            html{
                font-size: 18px;
                line-height: 1.6;
                color: #4a4a4a;
                letter-spacing: 0.6px;
                background-color:#f8f8f8;
            }
            body{
                padding: 0 16px 20px;
            }
            a{
                word-break: break-all;
                color: #000;
                text-decoration: none;
            }
            img{
                margin: 6px 0 ;
                border: none !important;
                height: auto !important;
                max-width: 100% !important;
            }
            span{max-width: 100% !important;}
            table{
                margin:15px 0;
                border-collapse: collapse;
                border-spacing: 0;
                width: 100%;
                text-align:center !important;
                max-width:100%;
            }
            th,td{
                max-width: 0;
                border:1px solid #ccc !important;
                white-space:normal !important;
                word-wrap:break-word !important;
            }
            th{
                background-color:#eee !important;
            }
            p{
                text-indent: 0em !important;
            }
            embed{
                width: auto !important;
            }
            section{
                max-width:100% !important;
            }
            iframe{
                max-width:100% !important;
            }
                   
            pre.prettyprint {
                background-color: #272822;
                border: none;
                overflow: hidden;
                padding: 10px 15px;
            }


            </style>
           
        </head>
        <body>
'''

html_trailing = '''
    </body>
</html>
'''
article_fields = {
    'title': fields.String,
    'subTitle': fields.Integer,
    'author': fields.String,
    'pubTime': fields.String,
    'content': fields.String,
    'img': fields.String,
    'url': fields.String,
    'source': fields.String,
    "_id": fields.String
}

articles_fields = {
    'pageNum': fields.Integer,
    'pageSize': fields.Integer
}


request_parser = reqparse.RequestParser()



response_articles = {
    'result': fields.List(fields.Nested(article_fields, default={})),
    'code': fields.Integer,
    'message': fields.String
}

response_article = {
    'result': fields.Nested(article_fields, default={}),
    'code': fields.Integer,
    'message': fields.String
}


class ArticleList(Resource):
    # @marshal_with(response_articles)
    def get(self):
        list_request = request_parser.copy()
        for paramter in articles_fields:
            list_request.add_argument(paramter, type=str, required=True)
        args = list_request.parse_args()

        page_size = int(args['pageSize'])
        page_num = int(args['pageNum'])
        skip = page_size * (page_num - 1)
        diarys = db.diary.find({}, {"title": 1, "subTitle": 1, "img": 1}).limit(page_size).skip(skip)
        diary_list = []
        for diary in diarys:
            diary['_id'] = str(diary['_id'])
            diary_list.append(diary)

        return dict(message="成功", code=0, result=diary_list)

class Article(Resource):
    def get(self):
        item_request = request_parser.copy()
        item_request.add_argument("_id", type=str, required=True)
        args = item_request.parse_args()
        _id = args['_id']
        article = db.diary.find_one({'_id': ObjectId(_id)})
        if article is not None:
            article['_id'] = _id
            article['content'] = html_leading + article['content'] + html_trailing
            return  dict(message="成功", code=0, result=article)
        else:
            return dict(message="找不到对应文章", code=404, result=None)

