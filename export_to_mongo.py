import pymongo as mg
import json


class Export:
    mongo = ''

    def __init__(self):
        self.mongo = mg.MongoClient("localhost", 27017)

    def to_mongo(self, reviews):
        mydb = self.mongo["Crawl_data"]
        mycol = mydb["tiki"]
        for review in reviews:
            try:
                x = mycol.insert(review, check_keys=False)
            except:
                pass


