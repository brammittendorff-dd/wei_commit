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
    name = 'jiexi_new'
    allowed_domains = ['*']
    redis_key = 'weibo_new:items'
    #CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=100103type%3D1%26q%3D{}&type=uid&value={}&containerid={}&page={}'
    # CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid=' + str(
    #     model.weibo_additional_id) + '&luicode=10000011&lfid=100103type%3D1%26q%3D' + weiboid + '&type=uid&value=' + str(
    #     model.weibo_additional_id) + '&containerid=' + model.container_id
    custom_settings = {
        "CONCURRENT_REQUESTS": 3,
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
        item=self.to_item(data)
        yield item
    def to_item(self,data):
        item=WeiboJiexiItem()
        item["release_time"] = data.get("release_time")
        item["release_state"] = data.get("release_state")
        item["is_repost"] = data.get("is_repost")
        #item["weibo"] = data.get("weibo")
        #item["weibo"] = data.get("weibo")
        item["data"] = data.get("data")
        item["share_image_url"] = data.get("share_image_url")
        item["create_time"] = data.get("create_time")
        item["media_id"] = data.get("media_id")
        #item["label_id"] = data.get("label_id")
        #item["other_keyword"] = data.get("other_keyword")
        #item["source"] = data.get("source")
        item["dynamicsource"] = data["dynamicsource"]
        item["star_keyword"] = data.get("star_keyword")
        item["dynamicsource_id"] = data.get("dynamicsource_id")
        item["description"] = data.get("description")
        item["url"] = data.get("url")
        return item
#「 #杨幂FashionNotes#小贴士-科普 」#杨幂##BOBOSNAP#是这两年常常看到的，每次出片总能拍出明星艺人的不同时尚感。这则纪录片带你了解创始人@伦思博 从创始BOBOSNAP一路走来的各种不容易，怀抱着一颗坚持的心，以及那份追求自由梦想的勇气～想要更多了解bobo伦思博尽在BOBOSNAP纪录片中哟～ ...全文
#text=<a  href="https://m.weibo.cn/p/index?containerid=100808e8d586dd7436fe56dd79b9b4f6c69350&extparam=%E6%9D%A8%E5%B9%82&luicode=10000011&lfid=1076036155202942" data-hide=""><span class='url-icon'><img style='width: 1rem;height: 1rem' src='http://n.sinaimg.cn/photo/5213b46e/20181127/timeline_card_small_super_default.png'></span><span class="surl-text">杨幂超话</span></a>｜<a  href="https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E6%9D%A8%E5%B9%82FashionNotes%23&luicode=10000011&lfid=1076036155202942" data-hide=""><span class="surl-text">#杨幂FashionNotes#</span></a> <br />2018-FashionNotes年终总结 <a href='/n/杨幂'>@杨幂</a> <br /><br />冬至之后，白天会慢慢变长。如果你愿意的话，每天都能和南回归线，一起回到原来的位置。我们和你一起，会在亮堂下，站得越来越久。<br />——————————————————————<br />•影视/综艺<br />2018年上映了一部电影，播出了两部 ...<a href="/status/4328755177048273">全文</a>
#longTextContent=<a  href="https://m.weibo.cn/p/index?extparam=%E6%9D%A8%E5%B9%82&containerid=100808e8d586dd7436fe56dd79b9b4f6c69350&luicode=20000061&lfid=4426598184785191" data-hide=""><span class='url-icon'><img style='width: 1rem;height: 1rem' src='https://n.sinaimg.cn/photo/5213b46e/20180926/timeline_card_small_super_default.png'></span><span class="surl-text">杨幂</span></a>｜<a  href="https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E6%9D%A8%E5%B9%82FashionNotes%23&luicode=20000061&lfid=4426598184785191" data-hide=""><span class="surl-text">#杨幂FashionNotes#</span></a>｜<a  href="https://m.weibo.cn/search?containerid=231522type%3D1%26t%3D10%26q%3D%23%E6%9D%A8%E5%B9%82%E4%B8%AD%E5%9B%BD%E8%BE%BE%E4%BA%BA%E7%A7%80%23&extparam=%23%E6%9D%A8%E5%B9%82%E4%B8%AD%E5%9B%BD%E8%BE%BE%E4%BA%BA%E7%A7%80%23&luicode=20000061&lfid=4426598184785191" data-hide=""><span class="surl-text">#杨幂中国达人秀#</span></a> <br /><a href='/n/中国达人秀'>@中国达人秀</a> 梦想观察员<a href='/n/杨幂'>@杨幂</a> 录制LOOK<br /><br />针织衫 in <a href='/n/GUCCI'>@GUCCI</a> RESORT 2020早春系列<br />耳饰 in <a href='/n/GUCCI'>@GUCCI</a> RESORT 2020早春系列<br />高跟鞋 in <a href='/n/Stuart_Weitzman'>@Stuart_Weitzman</a> NUDIST<br /><br />姐对卡通人物的服饰还蛮感兴趣的，看到这件米老鼠针织毛衣真的就写着杨幂的名字；GUCCI的耳饰也一直都是很夸张的，这个兽首宝石网面耳饰真是美丽闪耀，在ELLE11月刊内页上也佩戴过；以及杨幂很迅速的穿上了第四套GUCCI 2020早春系列(三套成衣+一套配饰)