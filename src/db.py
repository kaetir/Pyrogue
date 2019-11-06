import json
from pymongo import MongoClient

class PyrogueDB:

    def __init__(self) -> None:
        client = MongoClient('trustme.ovh', 27017)
        db = client['pyrogue']
        c = db['users'].find({})
        print(c[0])

