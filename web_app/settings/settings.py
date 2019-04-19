import os

# Mysql settings
SIMHASH_NAME = "simhash"
NEWS_NAME = "news"
MYSQL_DB_NAME = "news_simhash"

# Simhash settings
STOPWORDS_PATH = './data/stopwords.txt'

# ES settings
ES_HOST = os.environ.get("ES_HOST", "localhost")
ES_PORT = os.environ.get("ES_PORT", 9200)
ES_INDEX = os.environ.get("ES_INDEX", "test4")
ES_DOC_TYPE = os.environ.get("ES_DOC_TYPE", "test4")

# Mongo settings
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_DB = os.environ.get("MONGO_DB", "final_design")
MONGO_COL = os.environ.get("MONGO_COL", "news")

# NLP settings
SENTIMENT_URL = os.environ.get("SENTIMENT_URL", "http://localhost:8585/nlp/sentiment")
TYPE_URL = os.environ.get("TYPE_URL", "http://localhost:8585/nlp/news_type")
