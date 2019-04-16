from pymongo import MongoClient


class MongoDB(object):
    def __init__(self, mongo_host, mongo_port, db_name, collection):
        self.client = MongoClient(host=mongo_host, port=mongo_port)
        self.col = self.client[db_name][collection]

    def insert2mongo(self, news):
        self.col.insert_many(news)

    def get_news(self):
        cursor = self.col.find().sort([("newsDate", -1)]).limit(50)

        res = list()
        for i in cursor:
            i["_id"] = str(i["_id"])
            res.append(i)

        return res






