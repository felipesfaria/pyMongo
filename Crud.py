__author__ = 'felipesfaria'

from pymongo import MongoClient
client = MongoClient()
db = client.teste
db.contato.drop()
contato = db.contato

#Fiz um amigo o antonio
contato.insert_one({"nome":"Antonio","sobrenome":"Antunes","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199998888"},{"nome":"casa","numero":"2122223333"}]})

#Fiz mais dois amigos, Bruno e Carlos
Bruno = {"nome":"Bruno","sobrenome":"Bastos","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199997777"},{"nome":"casa","numero":"2122224444"}]}
Carlos = {"nome":"Carlos","sobrenome":"Carvalho","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199996666"},{"nome":"casa","numero":"2122225555"}]}
contato.insert_many([Bruno,Carlos])

#Quem sao meus amigos?
cursor = contato.find({},{"_id":0,"nome":1})
print "Nomes:"
for document in cursor:
    print(document)

#Como demorou para achar meus amigos, vou criar um indice
contato.create_index([("nome",1)])

#Antonio se mudou para sao paulo
contato.update({"nome":"Antonio"},{"$set":{"estado":"SP","telefone":[{"nome":"casa","numero":"1122223333"}]}})

#Quantos amigos eu tenho por estado?
cursor = contato.aggregate(
        [
            {"$group": {"_id": "$estado", "count": {"$sum": 1}}}
        ])
print "Amigos por estado:"
for document in cursor:
    print(document)

#Fiz uma amiga, Daniela
contato.insert_one({"nome":"Daniela","sobrenome":"Duarte","sexo":"f","estado":"RJ", "telefone":[{"nome":"celular","numero":"2199996666"},{"nome":"casa","numero":"2122225555"}]})

#Agora preciso mudar meus outros contatos para incluir o sexo de cada um
contato.update_many({"nome":{"$ne":"Daniela"}},{"$set":{"sexo":"m"}})

#Nao sou mais amigo do Carlos
contato.delete_one({"nome":"Carlos"})

#Vou dar uma festa, quem eu posso convidar do rio?
cursor = contato.find({"estado":"RJ","telefone.nome":"celular"},{"_id":0,"nome":1,"telefone.numero":1}).sort("nome",1)
print "Moram no rio e tem celular:"
for document in cursor:
    print(document)

#Quero ver minha agenda completa
cursor = contato.find()
print "Contatos:"
for document in cursor:
    print(document)