# -!- coding: utf-8 -!-
import os
import sys
import datetime
import json
import requests

sys.path.append("..")

from apscheduler.schedulers.blocking import BlockingScheduler
from scrapy import cmdline
from multiprocessing import Process


web_url = os.environ.get("WEB_URL", "http://localhost:8888/db/save")


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
        r = requests.post(url=web_url, json={"news": news})
        print(r.json())


if __name__ == "__main__":

    bs = BlockingScheduler()
    bs.add_job(run, "interval", hours=1, max_instances=5)
    print("start")
    run()
    bs.start()
    # run()




