from pymongo import MongoClient

conn = MongoClient("host.docker.internal:27017") #modificar en base a la base de datos, ahora esta asi para que el docker acceda al mongo de mi maquina