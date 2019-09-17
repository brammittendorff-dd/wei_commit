from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import engine
import datetime

Base = declarative_base()
metadata = Base.metadata

class Commit(Base):
    __tablename__ = 'commit'
    id = Column(INTEGER(11), primary_key=True)
    detail_url=Column(String(255))
    mid = Column(String(50))
    bid = Column(String(50))
    like_count = Column(INTEGER(11))
    created_at = Column(DATETIME, nullable=False)
    text = Column(LONGTEXT)
    user_id = Column(String(255))
    screen_name = Column(String(255))
    profile_image_url = Column(String(255))





class Cookies(Base):
    __tablename__ = 'cookie'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    cookies = Column(LONGTEXT, nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


def init_db():
    print('initialize database, drops and creates tables')
    Base.metadata.create_all(engine)


# if not engine.dialect.has_table(engine, 'weibo_status'):
#init_db()
