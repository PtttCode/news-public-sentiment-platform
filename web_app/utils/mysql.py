from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import BigInteger
from settings.settings import SIMHASH_NAME, NEWS_NAME, MYSQL_URL

Base = declarative_base()


class Sim(Base):
    __tablename__ = SIMHASH_NAME
    id = Column(Integer, primary_key=True)
    sh1 = Column(BigInteger, nullable=False)
    sh2 = Column(BigInteger, nullable=False)
    sh3 = Column(BigInteger, nullable=False)
    sh4 = Column(BigInteger, nullable=False)
    sh5 = Column(BigInteger, nullable=False)
    sh6 = Column(BigInteger, nullable=False)
    sh7 = Column(BigInteger, nullable=False)
    sh8 = Column(BigInteger, nullable=False)
    newsDate = Column(String, nullable=True)
    title = Column(String, nullable=True)
    source = Column(String, nullable=True)


class News(Base):
    __tablename__ = NEWS_NAME
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    newsDate = Column(String, nullable=False)
    source = Column(String, nullable=False)


class Mysql(object):
    def __init__(self, db):
        mysql_str = MYSQL_URL.format(db)
        pool = create_engine(mysql_str, encoding='utf-8', echo=False,
                             pool_size=100, pool_recycle=10)
        self.conn = scoped_session(sessionmaker(bind=pool))

    def hanming(self, simhash):
        """
        计算汉明距离，返回满足条件的个数
        """
        sh_lst = [simhash[i * 8: (i + 1) * 8] for i in range(8)]
        sql = """
            SELECT id
            FROM simhash 
            WHERE (BIT_COUNT(sh1 ^ {0}) + 
                   BIT_COUNT(sh2 ^ {1}) + 
                     BIT_COUNT(sh3 ^ {2}) + 
                     BIT_COUNT(sh4 ^ {3}) + 
                     BIT_COUNT(sh5 ^ {4}) + 
                     BIT_COUNT(sh6 ^ {5}) +
                     BIT_COUNT(sh7 ^ {6}) +
                     BIT_COUNT(sh8 ^ {7})
                    ) < {8}
            """.format(*sh_lst, 4)
        try:
            result = self.conn.execute(sql)
        except Exception as e:
            self.conn.rollback()
            print(str(e))
        return result.rowcount

    def insert_himhash(self, sh, value):
        """
        出入一条汉明距离与新闻码
        """
        sh_lst = [sh[i * 8: (i + 1) * 8] for i in range(8)]
        model = Sim()
        for idx, si in enumerate(sh_lst):
            setattr(model, "sh{}".format(idx + 1), int(si))

        model.newsDate = value["newsDate"]
        model.title = value["title"]
        model.source = value["source"]

        self.conn.add(model)
        self.conn.commit()

    def insert2mysql(self, news):
        # insert_template= "insert into news(title, content, newsDate, source) " \
        #              "values ({}, {}, {}, {})"
        for i in news:
            n = News()
            n.__tablename__ = "news"
            n.content = i["content"]
            n.title = i["title"]
            n.newsDate = i["newsDate"]
            n.source = i["source"]

            self.conn.add(n)
            self.conn.commit()

