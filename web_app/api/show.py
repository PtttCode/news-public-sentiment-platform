from api.base import BaseHandler
from settings.settings import ES_INDEX, ES_DOC_TYPE


class SearchHandler(BaseHandler):
    async def get(self):
        question = self.get_argument("question", None)
        limit = int(self.get_argument("limit"))
        page = (int(self.get_argument("page"))-1)*limit
        print(page, limit, question)
        msg = "暂无数据" if question is None else ""

        mc = self.main_class
        li = []

        if msg == "":
            li = mc.es.search_news(index=ES_INDEX, doc_type=ES_DOC_TYPE, question=question)

        return self.response({"code": 0,
                              "message": msg,
                              "count": len(li),
                              "data": li[page:page+limit]})


class TablesHandler(BaseHandler):
    def get(self):
        print(self.request.arguments)
        draw = self.get_argument("draw")
        length = int(self.get_argument("length"))
        start = int(self.get_argument("start"))
        print(start, length)

        mc = self.main_class
        li = mc.mongo.get_news()

        return self.response({"code": 0,
                              "draw": int(draw),
                              "recordsTotal": len(li),
                              "recordsFiltered": len(li),
                              "data": li[start:start + length]})

