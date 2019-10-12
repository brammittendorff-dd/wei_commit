# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/commit/wei_commit/weibo_jiexi')
import scrapy
import redis
import re
import json
import requests
import datetime
import time
import os
from urllib import parse
from scrapy_redis.spiders import RedisSpider
from weibo_jiexi.items import WeiboJiexiItem

class JiexiSpider(RedisSpider):
    name = 'jiexi'
    allowed_domains = ['*']
    redis_key = 'weibo:items'
    #CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=100103type%3D1%26q%3D{}&type=uid&value={}&containerid={}&page={}'
    # CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid=' + str(
    #     model.weibo_additional_id) + '&luicode=10000011&lfid=100103type%3D1%26q%3D' + weiboid + '&type=uid&value=' + str(
    #     model.weibo_additional_id) + '&containerid=' + model.container_id
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 1,
    #     'DEFAULT_REQUEST_HEADERS': {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    #     },
    #     #'COOKIES_ENABLED': False,
    #
    #     "ITEM_PIPELINES": {
    #         'weibo_jiexi.pipelines.WeiboJiexiPipeline': 1,
    #         'scrapy_redis.pipelines.RedisPipeline': 100,
    #     },
    #     "LOG_LEVEL": "DEBUG",
    #     "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderPriorityQueue",
    #     "SCHEDULER_PERSIST": True,
    #     "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
    #     # #     # 先进先出队列
    #     # "SCHEDULER_QUEUE_CLASS" : "scrapy_redis.queue.SpiderQueue",
    #     # #
    #     #     # 先进后出栈
    #     # "SCHEDULER_QUEUE_CLASS" : "scrapy_redis.queue.SpiderStack",
    #     "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "REDIS_HOST": '47.110.95.150',
        "REDIS_PORT": 6379,
        # "REDIS_URL":"redis://root:123456789@39.106.214.65",
        "REDIS_PARAMS" :{
        'password': 'Bitgraph818'
    }
    }
    # def __init__(self):
    #     self.r = redis.Redis(host="47.110.95.150", port=6379,password="Bitgraph818")

    def make_request_from_data(self, data):
        data=json.loads(data.decode())
        url="https://www.baidu.com/"
        meta={}
        meta["item"]=data
        return scrapy.Request(url=url,callback=self.parse,meta=meta,dont_filter=True)
    def parse(self, response):

        data=response.meta["item"]
        print(data)
        item=self.to_item(data)
        yield item
    def to_item(self,data):
        item=WeiboJiexiItem()
        item["release_time"] = data.get("release_time")
        item["release_state"] = data.get("release_state")
        item["is_repost"] = data.get("is_repost")
        item["weibo"] = data.get("weibo")
        item["weibo"] = data.get("weibo")
        item["data"] = data.get("data")
        item["share_image_url"] = data.get("share_image_url")
        item["create_time"] = data.get("create_time")
        item["media_id"] = data.get("media_id")
        item["label_id"] = data.get("label_id")
        item["other_keyword"] = data.get("other_keyword")
        item["source"] = data.get("source")
        item["star_keyword"] = data.get("star_keyword")
        item["dynamicsource_id"] = data.get("dynamicsource_id")
        item["description"] = data.get("description")
        item["url"] = data.get("url")
        return item