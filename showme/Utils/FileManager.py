#coding=utf-8
from flask_restful import Resource
from flask import send_from_directory
from showme import config
import os

class FileManager(Resource):
    def get(self, filename):
        return send_from_directory(config['UPLOAD_FOLDER'],
                                   filename)

    def getRoot(file=None):
        if file is None:
            file = '.'
        me = os.path.abspath(file)
        drive, path = os.path.splitdrive(me)
        while 1:
            path, folder = os.path.split(path)
            if not folder:
                break
        return drive + path



