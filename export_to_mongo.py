import pymongo as mg
import json


class Export:
    mongo = ''

    def __init__(self):
        self.mongo = mg.MongoClient("localhost", 27017)

    def to_mongo(self, product):
        mydb = self.mongo["Crawl_data"]
        mycol = mydb["tiki"]
        x = mycol.insert(product, check_keys=False)
