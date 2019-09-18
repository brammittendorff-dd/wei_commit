#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
#sys.path.append('/home/xiangmu/bitexiangmu/hanyu')
from database.db import session
from database.models import Keyword, Topic, Dynamic, TempUser, DynamicUser, RepostDynamic,\
    Media, RepostMedia, Source, DynamicTopic, SourceTopic, AccessToken
import random
import time
#from youdao_translator import translate
#from token_manager import get_token
import re
#from hanyu import image
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
from aliyunsdkgreen.request.extension import HttpContentHelper
import json
import uuid
import datetime


class JsonParser:

    def __init__(self, json_string):
        if not json_string:

            return

        # 获取所有话题
        topics = session.query(Topic.id).all()
        self.topic_ids = [obj[0] for obj in topics]
        self.keywords = self.get_keywords()
        self.json_string = json_string

    def get_keywords(self,):
        # 获取每个话题下的所有关键字
        kws = []
        for tid in self.topic_ids:
            # print(tid)
            #model=session.query(Keyword_Topics).filter(Keyword_Topics.topic_id==tid).all()
            models = session.query(Keyword).filter(Keyword.topics.any(Topic.id == tid))
            # print(models)
            # #格式为 {'topic_id': 'kw1|kw2|kw3'}
            kw = {str(tid): '|'.join([model.keyword_name for model in models.all()])}
            kws.append(kw)
        return kws

    @staticmethod
    def get_random_temp_user():
        rand = random.randrange(0, session.query(TempUser).filter(TempUser.user_category == 1).count())
        temp_user = session.query(TempUser).filter(TempUser.user_category == 1)[rand]
        return temp_user

    @staticmethod
    def get_media_models(media_list: list, tw_or_ins, dynamic_id, retweeted=False):
        media_models = list()
        for media in media_list:
            if retweeted:
                model = RepostMedia()
            else:
                model = Media()
            model.tw_or_ins = tw_or_ins
            model.is_video = media.get('is_video')
            model.pic_width = media.get('pic_width')
            model.pic_height = media.get('pic_height')
            model.url = media.get('url')
            if retweeted:
                model.repost_dynamic_id = dynamic_id
            else:
                model.dynamic_id = dynamic_id
            media_models.append(model)
        return media_models

    def get_topics(self, data_en):
        keyword_topic = []
        #print(self.keywords)
        for topic_and_keyword_dict in self.keywords:
            for topic_id, keyword in topic_and_keyword_dict.items():
                topic_id = int(topic_id)
                pattern = re.compile(keyword)
                res = pattern.findall(data_en)
                if res:
                    keyword_topic.append(topic_id)
        #print(keyword_topic)
        return keyword_topic

    def get_retweeted_model(self, retweeted_tweet, topics, model: Dynamic):
        repost_topics = topics
        # 被转发twitter的作者
        #print(retweeted_tweet.get('nick_name'),retweeted_tweet.get('tw_or_ins'))
        # repost_user = session.query(DynamicUser).filter(
        #     DynamicUser.nick_name == "AppleMusicJapan",
        #     DynamicUser.tw_or_ins == 1)

        repost_user = session.query(DynamicUser).filter(
            DynamicUser.nick_name == retweeted_tweet.get('nick_name'),
            DynamicUser.tw_or_ins == retweeted_tweet.get('tw_or_ins')).first()

        if not repost_user:

            repost_user = DynamicUser()
            repost_user.tw_or_ins = retweeted_tweet.get('tw_or_ins')
            repost_user.nick_name = retweeted_tweet.get('nick_name')
            repost_user.avatar_url = retweeted_tweet.get('avatar_url')
            session.add(repost_user)
            self.__flush()

        # 被转发twitter的内容
        repost_model = RepostDynamic()
        repost_model.dynamic_id = model.id
        repost_model.data_en = retweeted_tweet['data_en']
        if repost_model.data_en:
            try:
                #repost_model.data_ch = translate(repost_model.data_en)
                repost_model.data_ch = ''
            except:
                repost_model.data_ch = ''
            # if repost_model.data_ch:
            #     try:
            #         #model.release_state = 1
            #         model.release_state = self.green_text_scan(repost_model.data_ch)
            #     except:
            #         model.release_state = 1
            # else:
            #     repost_model.data_ch = ''
            # 被转发tweet的关键字，归属至转发tweet的话题
            repost_topics.extend(self.get_topics(repost_model.data_en))
        repost_model.dynamic_user_id = repost_user.id
        session.add(repost_model)
        self.__flush()
        #print(repost_model.id)

        # 被转发tweet的视频/图片
        if retweeted_tweet.get('media_id'):
            media_models = self.get_media_models(retweeted_tweet.get('media_id'),
                                                 model.tw_or_ins,
                                                 repost_model.id,
                                                 retweeted=True)
            session.add_all(media_models)
        return repost_topics

    def get_dynamic(self):
        author_id = self.json_string[0].get('author_id_rl')
        author = session.query(Source).filter(Source.id == author_id).first()
        author_topic = session.query(SourceTopic).filter(SourceTopic.source == author).first()

        for dynamic in self.json_string:
            # 获取动态
            #try:

            weibo_url=dynamic.get("weibo_url")
            url_model=session.query(Dynamic).filter(Dynamic.weibo_url==weibo_url).all()
            if url_model:
                return
            model = Dynamic()
            topics = []
            model.weibo_url =weibo_url
            model.author_id = self.get_random_temp_user().id
            # TODO 增加兜底，解决authod_id为空的问题 原因未知
            if not model.author_id:
                model.author_id = 1
            model.source_id = dynamic.get('author_id_rl')
            model.release_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dynamic['release_time']))
            model.is_repost = dynamic.get('is_repost')
            model.weibo_url=dynamic.get("weibo_url")
            model.tw_or_ins = dynamic.get('tw_or_ins')
            model.data_en = dynamic.get('data_en')
            model.description=dynamic.get("description")
            model.release_state = dynamic.get("release_state")
            if not model.release_state:
                model.release_state=0
            if model.is_repost==1:
                model.release_state=1
            model.read_amount = 0
            model.correct_state = 0

            # 如果该动态有文本内容
            if model.data_en:
                # 翻译为中文
                try:
                    #model.data_ch = translate(model.data_en)
                    model.data_ch =''
                except:
                    model.data_ch = ''
                # 违禁词敏感词检测
                if model.data_ch and model.release_state==0:

                    try:
                        model.release_state = self.green_text_scan(model.data_ch)
                    except:
                        model.data_ch = ''
                else:

                    model.data_ch = ''

                # 根据匹配到的关键字获取对应的话题
                topics = self.get_topics(model.data_en)
            session.add(model)
            self.__flush()
            # try:
            #     cover_url = None
            #     if dynamic.get('media_id'):
            #         media = dynamic.get('media_id')[0]
            #         if media.get('is_video') == 0:
            #             cover_url = media.get('url')
            #     model.share_image_url = image.get_share_img(nick_name="",
            #                                                 avatar_url="",
            #                                                 summary=author.chinese_name+"发动态啦!",
            #                                                 content_id=model.id,
            #                                                 is_dynamic=True,
            #                                                 release_time=model.release_time,
            #                                                 token_data=get_token(),
            #                                                 cover_url=cover_url)
            # except:
            #     model.share_image_url = ''
            # session.add(model)

            # 将图片/视频关联到动态
            if dynamic.get('media_id'):
                media_models = self.get_media_models(dynamic.get('media_id'), model.tw_or_ins, model.id)
                session.add_all(media_models)

            # 如果是转发
            if dynamic.get('is_repost') and dynamic.get('retweeted_status'):
                topics = self.get_retweeted_model(dynamic.get('retweeted_status'), topics, model)

            # 将动态与话题关联起来
            if author.character_type == 1 and author_topic:
                topic_list = list()
                topic_list.append(author_topic.topic_id)
            else:
                topic_list = sorted(list(set(topics)), key=topics.index)
            dynamic_topics = []

            for topic_id in topic_list:
                try:
                    if model.id:
                        dynamic_topic_model = DynamicTopic()
                        dynamic_topic_model.dynamic_id = model.id
                        dynamic_topic_model.topic_id = topic_id
                        dynamic_topics.append(dynamic_topic_model)
                except:
                    pass
            session.add_all(dynamic_topics)

        try:
            session.commit()
        except:
            session.rollback()

    @staticmethod
    def __flush():
        try:
            session.flush()
        except:
            session.rollback()

    @staticmethod
    def green_text_scan(text):
        # 请替换成您自己的accessKeyId、accessKeySecret。您可以修改配置文件，也可以直接明文替换
        clt = client.AcsClient("LTAIXqD8j3omkRbg", "2gZCYf4RCurAf1EXSKG3sKoX4eQCyc",'cn-shanghai')
        region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
        request = TextScanRequest.TextScanRequest()
        request.set_accept_format('JSON')
        task1 = {"dataId": str(uuid.uuid1()),
                 "content": text,
                 "time": datetime.datetime.now().microsecond
                }
        # 文本垃圾检测： antispam
        request.set_content(HttpContentHelper.toValue({"tasks": [task1], "scenes": ["keyword"]}))
        response = clt.do_action_with_exception(request)
        print(response.decode('utf-8'))
        result = json.loads(response)
        if 200 == result["code"]:
            task_results = result["data"]
            for task_result in task_results:
                if 200 == task_result["code"]:
                    scene_results = task_result["results"]
                    for scene_result in scene_results:
                        suggestion = scene_result["suggestion"]
                        if suggestion != 'pass':
                            return 1
                    return 0
# a=[{'avatar_url': 'https://entertain-kr.oss-cn-hangzhou.aliyuncs.com/15688009044800618.jpg', 'release_time': 1564979953, 'weibo_id': 5038104889, 'tw_or_ins': 3, 'nick_name': '崔秀英_snsd', 'author_id_rl': 36, 'data_en': '这12年我们一起经历了无数快乐的时光 💕 我们一起走下去吧💝 ', 'media_id': [{'url': 'https://entertain-kr.oss-cn-hangzhou.aliyuncs.com/1568800904779428.jpg', 'pic_width': 403, 'pic_height': 270, 'is_video': False}], 'retweeted_status': None, 'weibo_url': 'https://m.weibo.cn/detail/4401907328472754'}]
# JsonParser(a).get_dynamic()