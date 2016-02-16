__author__ = 'felipesfaria'

from pymongo import MongoClient
client = MongoClient()
db = client.teste
db.contato.drop()
contato = db.contato

contato.insert_one({"nome":"Antonio","sobrenome":"Antunes","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199998888"},{"nome":"casa","numero":"2122223333"}]})

Bruno = {"nome":"Bruno","sobrenome":"Bastos","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199997777"},{"nome":"casa","numero":"2122224444"}]}
Carlos = {"nome":"Carlos","sobrenome":"Carvalho","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199996666"},{"nome":"casa","numero":"2122225555"}]}


contato.insert_many([Bruno,Carlos])

print "Contatos iniciais:"
cursor = contato.find()
for document in cursor:
    print(document)

contato.update({"nome":"Antonio"},{"$set":{"estado":"SP","telefone":[{"nome":"casa","numero":"1122223333"}]}})

contato.insert_one({"nome":"Daniela","sobrenome":"Duarte","sexo":"f","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199996666"},{"nome":"casa","numero":"2122225555"}]})

contato.update_many({"nome":{"$ne":"Daniela"}},{"$set":{"sexo":"m"}})

contato.delete_one({"nome":"Carlos"})

print "Contatos finais:"
cursor = contato.find({},{"_id":0,"nome":1}).sort("nome",1)
for document in cursor:
    print(document)

