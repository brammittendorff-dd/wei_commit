# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db import engine
Base = declarative_base()
metadata = Base.metadata

class Source(Base):
    __tablename__ = 'source'
    id = Column(INTEGER(11), primary_key=True)
    source_url = Column(String(128))
    english_name = Column(String(32))
    chinese_name = Column(String(32))
    korea_name = Column(String(32))
    character = Column(String(32))
    company = Column(String(32))
    character_type = Column(INTEGER(11))
    ins_id = Column(String(32))
    twitter_id = Column(String(32))
    weibo_id = Column(String(32))
    youtube_id = Column(String(32))
    last_ins_timestamp = Column(INTEGER(11))
    last_twitter_timestamp = Column(INTEGER(11))
    last_weibo_timestamp = Column(INTEGER(11))
    last_youtube_timestamp = Column(INTEGER(11))
    last_ins_strory_timestamp = Column(INTEGER(11))
    create_time = Column(DateTime)
    container_id=Column(String(255))
    weibo_additional_id=Column(String(32))


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(11), primary_key=True)
    category_name = Column(String(64), nullable=False)
    create_time = Column(DateTime, default=datetime.now)


class DynamicUser(Base):
    __tablename__ = 'dynamic_user'

    id = Column(INTEGER(11), primary_key=True)
    tw_or_ins = Column(INTEGER(11))
    nick_name = Column(String(32))
    avatar_url = Column(String(256))
    create_time = Column(DateTime, default=datetime.now)


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(INTEGER(11), primary_key=True)
    keyword_name = Column(String(64), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    topics = relationship('Topic', secondary='keyword_topics')
# class Keyword_Topics(Base):
#     __tablename__ = 'keyword_topics'
#     keyword_id=Column(INTEGER(11), primary_key=True)
#     topic_id=Column(INTEGER(11), primary_key=True)
#     create_time = Column(DateTime, default=datetime.now)
class Qr(Base):
    __tablename__ = 'qr'

    id = Column(INTEGER(11), primary_key=True)
    qr_url = Column(String(256))
    qr_explain = Column(String(64))
    qr_name = Column(String(64))
    update_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)


class Skill(Base):
    __tablename__ = 'skill'

    id = Column(INTEGER(11), primary_key=True)
    skill_position = Column(String(32))
    skill_data = Column(String(256))
    sub_skill_data = Column(String(256))
    create_time = Column(DateTime, default=datetime.now)


class TempUser(Base):
    __tablename__ = 'temp_user'

    id = Column(INTEGER(11), primary_key=True)
    nick_name = Column(String(32))
    avatar_url = Column(String(256))
    user_category = Column(INTEGER(11))
    create_time = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    nick_name = Column(String(32))
    avatar_url = Column(String(256))
    open_id = Column(String(256))
    gender = Column(INTEGER(11))
    country = Column(String(32), default='')
    province = Column(String(32), default='')
    city = Column(String(32), default='')
    union_id = Column(INTEGER(11))
    create_time = Column(DateTime, default=datetime.now)


class Article(Base):
    __tablename__ = 'article'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(256))
    source_id = Column(ForeignKey('temp_user.id'), index=True)
    create_time = Column(DateTime)
    release_time = Column(DateTime)
    release_state = Column(INTEGER(11))
    read_amount = Column(INTEGER(11))
    article_data = Column(Text)
    qr_id = Column(ForeignKey('qr.id'), index=True)
    coverone = Column(String(256))
    coverthere = Column(String(256))
    covertwo = Column(String(256))
    share_image_url = Column(Text)
    summary = Column(Text)

    source = relationship('TempUser')
    qr = relationship('Qr')


class Dynamic(Base):
    __tablename__ = 'dynamic'

    id = Column(INTEGER(11), primary_key=True)
    author_id = Column(ForeignKey('temp_user.id'), index=True)
    source_id = Column(ForeignKey('source.id'), index=True)
    release_time = Column(DateTime)
    release_state = Column(INTEGER(11), default=1)
    read_amount = Column(INTEGER(11), default=0)
    is_repost = Column(TINYINT(1), default=0)
    tw_or_ins = Column(INTEGER(11))
    correct_state = Column(INTEGER(11))
    data_en = Column(MEDIUMTEXT, default='')
    data_ch = Column(MEDIUMTEXT, default='')
    share_image_url = Column(MEDIUMTEXT, default='')
    create_time = Column(DateTime, default=datetime.now)
    description= Column(String(256))
    weibo_url = Column(String(256))
    source = relationship('TempUser')
    source1 = relationship('Source')


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(INTEGER(11), primary_key=True)
    category_id = Column(ForeignKey('category.id'), index=True)
    create_time = Column(DateTime)
    release_state = Column(INTEGER(11))
    qr_id = Column(ForeignKey('qr.id'), index=True)
    background_url = Column(String(256))
    topic_explain = Column(String(256))
    topic_name_cn = Column(String(256))
    topic_name_en = Column(String(256))
    avater_url = Column(String(256))
    category = relationship('Category')
    qr = relationship('Qr')


class ArticleAtitude(Base):
    __tablename__ = 'article_atitude'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    atitude = Column(String(10))
    article_id = Column(ForeignKey('article.id'), index=True)
    create_time = Column(DateTime, default=datetime.now)

    article = relationship('Article')
    user = relationship('User')


class SourceTopic(Base):
    __tablename__ = 'source_topics'

    source_id = Column(ForeignKey('source.id'), primary_key=True, nullable=False)
    topic_id = Column(ForeignKey('topic.id'), primary_key=True, nullable=False, index=True)
    create_time = Column(DateTime)

    source = relationship('Source')
    topic = relationship('Topic')


class DynamicAtitude(Base):
    __tablename__ = 'dynamic_atitude'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    atitude = Column(String(10))
    dynamic_id = Column(ForeignKey('dynamic.id'), index=True)
    create_time = Column(DateTime, default=datetime.now)

    dynamic = relationship('Dynamic')
    user = relationship('User')


class DynamicTopic(Base):
    __tablename__ = 'dynamic_topics'

    dynamic_id = Column(ForeignKey('dynamic.id'), primary_key=True, nullable=False)
    topic_id = Column(ForeignKey('topic.id'), primary_key=True, nullable=False, index=True)
    create_time = Column(DateTime)

    dynamic = relationship('Dynamic')
    topic = relationship('Topic')

    t_keyword_topics = Table(
        'keyword_topics', metadata,
        Column('keyword_id', ForeignKey('keyword.id'), primary_key=True, nullable=False),
        Column('topic_id', ForeignKey('topic.id'), primary_key=True, nullable=False, index=True)
    )


class Media(Base):
    __tablename__ = 'media'

    id = Column(INTEGER(11), primary_key=True)
    url = Column(Text)
    pic_width = Column(INTEGER(11))
    pic_height = Column(INTEGER(11))
    is_video = Column(TINYINT(1), default=0)
    dynamic_id = Column(ForeignKey('dynamic.id'), index=True)
    create_time = Column(DateTime)

    dynamic = relationship('Dynamic')


class RepostDynamic(Base):
    __tablename__ = 'repost_dynamic'

    id = Column(INTEGER(11), primary_key=True)
    dynamic_user_id = Column(ForeignKey('dynamic_user.id'), index=True)
    data_en = Column(MEDIUMTEXT, default='')
    data_ch = Column(MEDIUMTEXT, default='')
    dynamic_id = Column(ForeignKey('dynamic.id'), index=True)
    create_time = Column(DateTime, default=datetime.now)

    dynamic = relationship('Dynamic')
    dynamic_user = relationship('DynamicUser')


class UserFollow(Base):
    __tablename__ = 'user_follow'

    user_id = Column(ForeignKey('user.id'), primary_key=True, nullable=False)
    topic_id = Column(ForeignKey('topic.id'), primary_key=True, nullable=False, index=True)
    create_time = Column(DateTime)

    topic = relationship('Topic')
    user = relationship('User')


class RepostMedia(Base):
    __tablename__ = 'repost_media'

    id = Column(INTEGER(11), primary_key=True)
    url = Column(Text)
    pic_width = Column(INTEGER(11))
    pic_height = Column(INTEGER(11))
    is_video = Column(TINYINT(1), default=0)
    repost_dynamic_id = Column(ForeignKey('repost_dynamic.id'), index=True)
    create_time = Column(DateTime, default=datetime.now)

    repost_dynamic = relationship('RepostDynamic')


class AccessToken(Base):
    __tablename__ = 'access_token'

    id = Column(INTEGER(11), primary_key=True)
    token = Column(Text)
    update_time = Column(DateTime, onupdate=datetime.now)
    create_time = Column(DateTime, default=datetime.now)