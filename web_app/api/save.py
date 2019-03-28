import time
import logging

from api.base import BaseHandler
from settings.settings import ES_INDEX, ES_DOC_TYPE

logger = logging.getLogger("tornado.access")


class SaveHandler(BaseHandler):
    async def post(self):
        start = time.time()
        body = self.json_read()
        logger.info(msg="读取数据: {}s".format(str(time.time()-start)))

        mc = self.main_class
        news = body["news"]
        res_str = "成功存入"

        start = time.time()
        n_news = mc.check_repeat(news)
        logger.info("滤重: {}s".format(str(time.time() - start)))
        logger.info("过滤前数量: {}\n过滤后数量: {}".format(len(news), len(n_news)))

        if len(n_news) > 0:
            start = time.time()
            mc.save2db(news=n_news, index=ES_INDEX, doc_type=ES_DOC_TYPE)
            logger.info("存入数据: {}s".format(str(time.time() - start)))

        return self.response({"code": 200, "msg": res_str+" {}篇".format(str(len(n_news)))})

