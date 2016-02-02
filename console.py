__author__ = 'felipesfaria'

from pymongo import MongoClient
client = MongoClient()
db = client.test
restaurants = db.restaurants

def printCursor(cursor):
    for doc in cursor:
        print doc
