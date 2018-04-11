# _*_ coding: utf-8 _*_
from pymongo import MongoClient
from showme import config

mongoClient = MongoClient(config.SQLALCHEMY_DATABASE_URI)
db = mongoClient.showme