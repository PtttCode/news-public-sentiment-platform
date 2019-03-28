# -!- coding: utf-8 -!-
import scrapy
import re
import sys
import os
import time
import datetime
import json
import requests

sys.path.append("..")

from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy import cmdline
from multiprocessing import Process

from items import TutorialItem


class WY_Spider(scrapy.Spider):
    name = "wy"
    allowed_domains = ["new.163.com"]
    start_urls = [
        "https://news.163.com",
        "http://news.163.com/domestic/",
        "http://news.163.com/world/",
        "http://tech.163.com/",
        "http://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback",
        "https://temp.163.com/special/00804KVA/cm_yaowen.js?callback=data_callback",
        "https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback",
        "http://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback"
    ]
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               }

    def parse(self, response):
        # print(response.text)
        keyword = "".join(re.findall("//(.*)\.163", response.url))
        keyword = keyword if keyword != "temp" else "news"

        pattern = "(http.*://{}.163.com/\d+/\d+/\d+/.*.html)".format(keyword)
        # html = response.css("a::attr(href)").extract()
        html = list(set(re.findall(pattern, response.text)))
        # print(html, response.url)
        # print(pattern)

        for i in html.copy():
            if re.search(pattern, i) is None:
                html.remove(i)
                continue
        # print("=============", len(html))
        for i in html:
            i = re.split("\"", i)[0]
            yield scrapy.Request(i, callback=self.get_content,
                                 headers=self.headers, dont_filter=True)

    def get_content(self, response):
        title = self.rm_html_tag("".join(response.css("h1::text").extract()))
        content = response.css("div.endText p::text").extract() \
            if response.css("div.endText p::text").extract() \
            else response.css("div.post_text p::text").extract()

        content = [i for i in content if i != "" and i != "\n"]
        content = self.rm_html_tag("".join(content))
        # print("=========", content)
        # print("---------", title)
        item = TutorialItem()
        item['newsDate'] = str(datetime.datetime.now())
        item['title'] = title
        item['content'] = content
        item['source'] = response.url

        yield item

    @staticmethod
    def rm_html_tag(content):
        content = re.sub("（原标题.*）", "", content)
        return re.sub(r"</?\w+[^>]*>", "", content)


def run_spider(spider, filename):
    # date = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # filename = "news-"+date+".json"
    cmdline.execute("scrapy crawl {} -o {}".format(spider, filename).split())



def run():
    spider_name = ["wy", "sina"]
    for spider in spider_name:
        date = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        filename = "news_saver/news-{}-{}.json".format(spider, date)
        p = Process(target=run_spider, args=(spider, filename,))
        p.start()
        p.join()

        print(filename)
        with open(filename, "r", encoding="utf-8") as f:
            news = json.loads(f.read())
        r = requests.post(url="http://localhost:8888/db/save", json={"news": news})
        print(r.json())


if __name__ == "__main__":

    bs = BlockingScheduler()
    bs.add_job(run, "interval", hours=1, max_instances=5)
    print("start")
    run()
    bs.start()
    # run()


    # import json
    # from elasticsearch import Elasticsearch
    #
    # es = Elasticsearch(hosts="localhost", port=9200)
    # date = str(datetime.datetime.now().strftime("%Y-%m-%d-H"))
    # with open("news-2019-03-14-22-30-00.json", "r", encoding="utf-8") as f:
    #     data = json.loads(f.read())

    # li = []
    # for idx, v in enumerate(data):
    #     v1 = {}
    #     v1["_index"] = "test1"
    #     v1["_type"] = "test1"
    #     v1["_id"] = idx
    #     dic = {}
    #     dic["index"] = v1
    #     li.append(dic)
    #     li.append(v)
    #
    # a = es.bulk(index="test1", doc_type="test1", body=li)
    # print(a)




