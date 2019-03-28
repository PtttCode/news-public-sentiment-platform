import tornado.ioloop
import tornado.web
import tornado.httpserver
import json
import ptttloggg

from sentiment_model import SentimentModel
from type_model import TypeModel


def main():
    ptttloggg.initLogConf()
    application = tornado.web.Application([(r"/nlp/sentiment", SentimentHandler),
                                           (r"/nlp/news_type", TypeHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(8585)
    http_server.start()
    print("-------------server start-----------------")
    tornado.ioloop.IOLoop.current().start()


class BaseHandler(tornado.web.RequestHandler):
    #  解决跨域问题
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'authorization, Authorization, Content-Type, Access-Control-Allow-Origin,'
                        ' Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')


class SentimentHandler(BaseHandler):
    async def post(self):
        body = json.loads(self.request.body.decode(), encoding="utf-8")
        news = body.get("news")
        result = list()

        for i in news:
            res = sentiment_cla.predict(i)
            result.append(res)
        return self.write(json.dumps({"code": 200, "data": result}, ensure_ascii=False))


class TypeHandler(BaseHandler):

    async def post(self):
        body = json.loads(self.request.body.decode(), encoding="utf-8")
        # print(body)
        news = body.get("news")
        result = list()

        for i in news:
            res = type_cla.predict(i)
            result.append(res)
        return self.write(json.dumps({"code": 200, "data": result}, ensure_ascii=False))


if __name__ == "__main__":
    type_cla = TypeModel()
    print("==============================1=============================")
    sentiment_cla = SentimentModel()
    print("==============================2=============================")
    main()
