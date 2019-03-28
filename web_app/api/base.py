import tornado.web
import json


class BaseHandler(tornado.web.RequestHandler):
    @property
    def main_class(self):
        return self.application.mc

    def json_read(self):
        data = self.request.body.decode()
        return json.loads(data, encoding="utf-8")

    def response(self, data):
        return self.write(json.dumps(data, ensure_ascii=False))



