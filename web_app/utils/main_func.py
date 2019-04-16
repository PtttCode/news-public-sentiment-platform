import json

from settings.settings import MYSQL_DB_NAME, \
    STOPWORDS_PATH, ES_HOST, ES_PORT, \
    MONGO_COL, MONGO_DB, MONGO_HOST, MONGO_PORT, \
    SENTIMENT_URL, TYPE_URL
from utils.es import ES
from utils.mongo import MongoDB
from utils.mysql import Mysql
from utils.simhash import SimHash
from utils.predict import Predict


class MainClass(object):
    def __init__(self):
        self.es = ES(host=ES_HOST, port=ES_PORT)
        self.mongo = MongoDB(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT,
                             db_name=MONGO_DB, collection=MONGO_COL)
        self.mysql = Mysql(db=MYSQL_DB_NAME)
        self.simhash = SimHash(stopwords_path=STOPWORDS_PATH)
        self.nlp = Predict(sentiment_url=SENTIMENT_URL, type_url=TYPE_URL)

    @staticmethod
    def get_news(filename):
        with open(filename, "r", encoding="utf-8") as f:
            news = json.loads(f.read())
        return news

    def check_repeat(self, news):
        news_save = list()
        for idx, value in enumerate(news):
            try:
                simhash_code = self.simhash.build_simhash(value["title"] + value["content"])
                repeat_code = self.mysql.hanming(simhash_code)
            except Exception as e:
                print(e.args)
                print(simhash_code, value)
                repeat_code = 1

            if repeat_code == 0:
                try:
                    self.mysql.insert_himhash(simhash_code, value)
                    news_save.append(value)
                except Exception as e:
                    print(e.args)
            else:
                continue

        self.mysql.insert2mysql(news_save)

        return news_save

    def predict(self, news):
        return self.nlp.infer(news)

    def save2db(self, news, index, doc_type):
        final_news = self.predict(news)
        #TODO 验证是否存入成功
        self.es.insert2es(data=final_news, index=index, doc_type=doc_type)
        self.mongo.insert2mongo(final_news.copy())

        print("finish")





