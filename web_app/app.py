import tornado.ioloop
import tornado.web
import tornado.httpserver
import json
import ptttloggg
import os


from settings.settings import MYSQL_DB_NAME, \
    STOPWORDS_PATH, ES_HOST, ES_PORT, \
    MONGO_COL, MONGO_DB, MONGO_HOST, MONGO_PORT, \
    SENTIMENT_URL, TYPE_URL
from utils.es import ES
from utils.mongo import MongoDB
from utils.mysql import Mysql
from utils.simhash import SimHash
from utils.predict import Predict
from api.save import SaveHandler
from api.show import SearchHandler, TablesHandler

urls = [(r"/db/save", SaveHandler),
        (r"/normal/search", SearchHandler),
        (r"/normal/tables", TablesHandler)
        ]


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


class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls
        settings = dict(static_path=os.path.join(os.path.dirname(__file__), 'static'))
        super(Application, self).__init__(handlers, **settings)
        ptttloggg.initLogConf()
        self.mc = self.init_main()

    @staticmethod
    def init_main():
        return MainClass()


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.bind(8888)
    http_server.start()
    print("-------------server start-----------------")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
    # mc = MainClass()
    # body ={
  # "settings": {
  #   "index.analysis.analyzer.default.type": "ik_max_word"
  #   }
# }

    # mc.es.es.index(index="test3", doc_type="test3", body=body)
    # data = mc.es.es.search(index="test2", doc_type="test2", body={"query":{"match_all":{}}, "size":1000})
    # data = [i["_source"] for i in data["hits"]["hits"]]
    # print(len(data))
    # mc.es.insert2es(index="test4", doc_type="test4", data=data)

    # res = mc.es.search_news("test4", "test4", "暴雨")
