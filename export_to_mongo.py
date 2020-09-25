import pymongo as mg
import json


class Export:
    mongo = ''

    def __init__(self):
        self.mongo = mg.MongoClient("localhost", 27017)

    def many_to_mongo(self, reviews):
        mydb = self.mongo["Crawl_data"]
        mycol = mydb["tiki"]
        for review in reviews:
            try:
                x = mycol.insert(review, check_keys=False)
            except:
                print("err at export to mongo, message: " + str(err))
                pass

    def one_to_mongo(self, review):
        mydb = self.mongo["Crawl_data"]
        mycol = mydb["tiki"]
        try:
            x = mycol.insert(review, check_keys=False)
        except Exception as err:
            print("err at export to mongo, message: " + str(err))
            pass
