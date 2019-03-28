import json
import requests
import jieba.analyse


class Predict(object):
    def __init__(self, sentiment_url, type_url):
        self.sentiment_url = sentiment_url
        self.type_url = type_url

    @staticmethod
    def get_keywords(news):
        for value in news:
            art = value["title"] + value["content"]
            keywords = jieba.analyse.extract_tags(art, topK=36, withWeight=True, withFlag=True,
                                                  allowPOS=("nr", "ns", "n", "v", "a", "nt", "nz"))

            dic = {
                "nr": [], "ns": [],
                "n": [], "v": [],
                "a": [], "nt": [],
                "nz": [],
            }

            for i in keywords:
                word, pos = str(i[0]).split("/")
                if len(list(set(dic[pos]))) >= 3:
                    continue
                dic[pos].append(word)

            keywords = dic["n"] + dic["ns"] + dic["nr"] + dic["nt"] + dic["nz"] + dic["v"]
            if len(keywords) > 15:
                value["keywords"] = keywords
            else:
                keywords.extend(dic["a"])
                value["keywords"] = keywords

        return news

    def infer(self, news):
        """
        输入新闻列表
        进行情感、类型预测，找出关键词
        """
        sentences = [i["title"]+i["content"] for i in news]
        data = {"news": sentences}
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~", data)

        res_s = requests.post(self.sentiment_url, json=data).json()["data"]
        res_t = requests.post(self.type_url, json=data).json()["data"]

        for idx, value in enumerate(news):
            value["sentiment"] = res_s[idx]
            value["type"] = res_t[idx]

        news = self.get_keywords(news)
        return news

