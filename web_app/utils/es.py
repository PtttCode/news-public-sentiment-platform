from elasticsearch import Elasticsearch


class ES(object):
    def __init__(self, host, port):
        self.es = Elasticsearch("{}:{}".format(host, port))

    def insert2es(self, index, doc_type, data):
        li = []
        for idx, v in enumerate(data):
            v1 = dict()
            dic = dict()

            v1["_index"] = index
            v1["_type"] = doc_type
            v1["_id"] = idx
            dic["index"] = v1

            li.append(dic)
            li.append(v)
        self.es.bulk(index=index, doc_type=doc_type, body=li)

    def search_news(self, index, doc_type, question):
        body = {
            "query": {
                "bool": {
                    "should": [
                            {"match": {"title": question}},
                            {"match": {"content": question}},
                            {"match": {"keywords": question}}
                        ]
                }
            },
            "size": 80,

        }
        result = self.es.search(index=index, doc_type=doc_type, body=body)
        result = result["hits"]["hits"]

        res = [i["_source"] for i in result]
        return res




