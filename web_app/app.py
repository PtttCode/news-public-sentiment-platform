import tornado.ioloop
import tornado.web
import tornado.httpserver
import ptttloggg
import os

from api.save import SaveHandler
from api.show import SearchHandler, TablesHandler
from utils.main_func import MainClass

urls = [(r"/db/save", SaveHandler),
        (r"/normal/search", SearchHandler),
        (r"/normal/tables", TablesHandler)
        ]


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
