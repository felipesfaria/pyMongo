__author__ = 'felipesfaria'
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pymongo
from datetime import datetime


def HelloMongo():
    print "Hello Mongo!"


def ImportInstructions():
    uri = "https://raw.githubusercontent.com/mongodb/docs-assets/primer-dataset/dataset.json"
    print "Download sample sets from: {}".format(uri)
    importCommand = "mongoimport --db test --collection restaurants --drop --file dataset.json"
    print "and enter the following line in the terminal:\n{}".format(importCommand)


def Insert():
    client = MongoClient()
    db = client.test
    # Para inserir um documento no bd envie um objeto
    # Se você não incluir um Id o mongo ira gerar um Id automaticamente para você
    result = db.restaurants.insert_one(
        {
            "address": {
                "street": "2 Avenue",
                "zipcode": "10075",
                "building": "1480",
                "coord": [-73.9557413, 40.7720266]
            },
            "borough": "Manhattan",
            "cuisine": "Italian",
            "grades": [
                {
                    "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                    "grade": "A",
                    "score": 11
                },
                {
                    "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                    "grade": "B",
                    "score": 17
                }
            ],
            "name": "Vella",
            "restaurant_id": "41704620"
        }
    )
    # a inserção retorna o id do objeto criado
    print "result.inserted_id: {}".format(result.inserted_id)


def FindNames():
    client = MongoClient()
    db = client.test
    # A chamada find serve para buscar informação, ela retorna um cursor para o
    # primeiro rsultado da busca e pode ser iterado
    cursor = db.restaurants.find({}, ["name"])
    for document in cursor:
        print(document)


def FindAll():
    client = MongoClient()
    db = client.test
    # A chamada find serve para buscar informação, ela retorna um cursor para o
    # primeiro rsultado da busca e pode ser iterado
    cursor = db.restaurants.find()
    for document in cursor:
        print(document)


def FindCount():
    client = MongoClient()
    db = client.test
    # para descobrir a quantdiade de resultados existe a funcao count()
    cursor = db.restaurants.find()
    cursor.count()


def FindeQuery():
    client = MongoClient()
    db = client.test
    # Para filtrar os resultados envie um objeto com os parametros que deseja buscar
    cursor = db.restaurants.find({"address.zipcode": "10075"})
    for document in cursor:
        print(document)
    print len(cursor)


def FindeQueryArray():
    client = MongoClient()
    db = client.test
    # É possivel filtrar por parametros contidos em um vetor interno
    # o resultado vai conter todos os documentos em que algum elemento do vetor
    # satisfizer o filtro
    cursor = db.restaurants.find({"grades.grade": "B"})
    for document in cursor:
        print(document)


def ComplexQuery():
    client = MongoClient()
    db = client.test
    cursor = db.restaurants.find({
        "$or": [{
            "grades.score": {
                "$lt": 100
            },
            "grades.score": {
                "$gt": 90
            },
            "borough": "Manhattan"
        }, {
            "grades.score": {
                "$in": [50, 40]
            },
            "borough": "Staten Island"
        }]
    }).sort([
        ("borough", pymongo.ASCENDING)
    ])
    for document in cursor:
        print(document)
    print "cursor.count()={}".format(cursor.count())

def UpdateUndefinedCategory():
    client = MongoClient()
    db = client.test
    result = db.restaurants.update_many(
        {"address.zipcode": "10016", "cuisine": "Other"},
        {
            "$set": {"cuisine": "Category To Be Determined"}
        })
    print "{} restaurants matched.".format(result.matched_count)
    # print "{} restaurants modified.".format(result.modified_count)


def RestaurantsByBorough():
    client = MongoClient()
    db = client.test
    cursor = db.restaurants.aggregate(
        [
            {"$group": {"_id": "$borough", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ])
    for document in cursor:
        print(document)


def DestroyThoseWhoCannotBeNamed():
    client = MongoClient()
    db = client.test
    result = db.restaurants.delete_many({"name": ""})
    print "{} restaurantes destroyed".format(result.deleted_count)
    print ("Everybody has a name!")
    print db.restaurants.find({"name": ""}).count()


def DestroyManhattan():
    client = MongoClient()
    db = client.test
    result = db.restaurants.delete_many({"borough": "Manhattan"})
    print "{} restaurantes destroyed".format(result.deleted_count)
    print ("No more food in manhattan!")
