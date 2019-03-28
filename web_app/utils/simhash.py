import jieba
import jieba.analyse
import numpy as np


class SimHash(object):

    def __init__(self, stopwords_path):
        jieba.analyse.set_stop_words(stopwords_path)

    def build_simhash(self, content):
        """
        :params: the body/content of a news
        :return: the simhash fingerprints
        """
        seg = jieba.cut(content)
        # use stop words
        keyWord = jieba.analyse.extract_tags(
            '|'.join(seg), topK=20, withWeight=True, allowPOS=())  # 在这里对jieba的tfidf.py进行了修改
        # 即先按照权重排序，再按照词排序
        keyList = []
        # print(keyWord)
        for feature, weight in keyWord:
            weight = int(weight * 20)
            feature = self.string_hash(feature)
            temp = []
            for i in feature:
                if(i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        # print(list1)
        if(keyList == []):  # 编码读不出来
            return '00'
        simhash = ''
        for i in list1:
            if(i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def string_hash(self, source):
        """
        :params: input of string
        :return: hash code of size 64
        """
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            # print(source,x)
            return str(x)
# def insert_himhash(handler, sh, news_code):
#     """
#     出入一条汉明距离与新闻码
#     """
#     sh_lst = [sh[i * 8: (i + 1) * 8] for i in range(8)]
#     model = Sim()
#     for idx, si in enumerate(sh_lst):
#         setattr(model, "sh{}".format(idx + 1), int(si))
#     if news_code:
#         model.newsDate = news_code
#     handler.add(model)
#     handler.commit()
#
#
# def hanming(handler, simhash):
#     """
#     计算汉明距离，返回满足条件的个数
#     """
#     sh_lst = [simhash[i * 8: (i + 1) * 8] for i in range(8)]
#     sql = """
#         SELECT id
#         FROM simhash
#         WHERE (BIT_COUNT(sh1 ^ {0}) +
#                BIT_COUNT(sh2 ^ {1}) +
#                  BIT_COUNT(sh3 ^ {2}) +
#                  BIT_COUNT(sh4 ^ {3}) +
#                  BIT_COUNT(sh5 ^ {4}) +
#                  BIT_COUNT(sh6 ^ {5}) +
#                  BIT_COUNT(sh7 ^ {6}) +
#                  BIT_COUNT(sh8 ^ {7})
#                 ) < {8}
#         """.format(*sh_lst, 4)
#     try:
#         result = handler.execute(sql)
#     except Exception as e:
#         handler.rollback()
#         print(str(e))
#     return result.rowcount