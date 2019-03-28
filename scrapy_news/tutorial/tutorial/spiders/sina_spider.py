# coding: utf-8
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


class Sina_spider(scrapy.Spider):
    name = "sina"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = [
        "https://news.sina.com.cn/",
        "https://news.sina.com.cn/china/",
        "https://news.sina.com.cn/world/",
    ]
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               }

    def parse(self, response):
        # print(response.text)
        htmls = re.findall("(https://.{1,100}?.shtml)", response.text)
        # print(htmls, len(htmls))
        for i in htmls:
            yield scrapy.Request(i, callback=self.get_content,
                                 headers=self.headers, dont_filter=False)

    def get_content(self, response):
        title = "".join(response.css("h1::text").extract())

        content = response.css("div.article p::text").extract()
        if "原标题" in content[0]:
            content.pop(0)
        content = "".join([i for i in content if i != "" and i != "\n"])

        title = self.rm_html_tag(title)
        content = self.rm_html_tag(content)

        item = TutorialItem()
        item['newsDate'] = str(datetime.datetime.now())
        item['title'] = title
        item['content'] = content
        item['source'] = response.url

        yield item

        # print(title, "\n", content)

    @staticmethod
    def rm_html_tag(content):
        content = re.sub("(责任编辑.*)", "", content)
        return re.sub(r"</?\w+[^>]*>", "", content)


def sina():
    cmdline.execute("scrapy crawl sina".split())


def wy():
    cmdline.execute("scrapy crawl wy".split())


if __name__ == "__main__":
    # p = Process(target=wy)
    p1 = Process(target=sina)
    # p.start()
    p1.start()
    # sen = "原标题：被调查环保志愿者已获自由 自称涉“寻衅滋事”被传唤　　出所。　　新京报此前报道，在响水调查环境污染问题的民间环保志愿者张文斌失联。张文斌居住酒店的工作人员证实，有身着制式服装的人到店将其带走。响水县城东派出所民警称，张文斌正在接受警方调查。　　今日14时，新京报记者与张文斌取得联系。他称，今早被响水警方传唤，据传唤证的内容，他因涉嫌“寻衅滋事”接受警方询问。张文斌介绍，民警主要就他在网络发布关于响水爆炸核心现场的内容进行询问。但该说法未得到警方证实。此前报道中提及他持有的两个身份证，系其本人户籍地变更前、后所办理。　　响水县公安局城东派出所民警14时证实，张文斌此前接受警方传唤、询问，目前已离开派出所。　　新京报记者 康佳  责任编辑：赵明"
    # print(u'　　中国非凡的技术实力让美国的自由市场信徒们乱了阵脚——不论在公共部门还是私营部门都是如此。随着中国增加军费、经略南海，成为美国头号地缘政治对手，那种不受束')

