import json
from pymongo import MongoClient

client = MongoClient('trustme.ovh',27017)
db = client['pyrogue']
c = db['users'].find({})
print(c[0])
