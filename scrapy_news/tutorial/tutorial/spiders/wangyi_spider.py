# -!- coding: utf-8 -!-
import scrapy
import re
import sys
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



