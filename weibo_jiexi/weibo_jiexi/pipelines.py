# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/commit/wei_commit/weibo_jiexi')
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from weibo_jiexi import weibo_json_parse
import requests
import time
from weibo_jiexi.oss import upload
class WeiboJiexiPipeline(object):
    def __init__(self):
        self.s=requests.session()
        self.s.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
    def process_item(self, item, spider):
        data=dict(item)
        item=self.oss_up(data)
        print(item)
        #lists=[]
        #lists.append(item)
        weibo_json_parse.JsonParser(item).get_dynamic()
        return item
    def oss_up(self,data):
        # avatar_url=data.get("avatar_url")
        # if avatar_url:
        #     data["avatar_url"]=self.get_oss_img_url(avatar_url)
        media_id=data.get("media_id")
        if media_id:
            for index,i in enumerate(media_id):
                if i["is_video"]:
                    data["media_id"][index]["url"]=self.get_oss_video_url(i["url"])
                else:
                    data["media_id"][index]["url"]=self.get_oss_img_url(i["url"])
        # retweeted_status=data.get("retweeted_status")
        # if retweeted_status:
        #     avatar_url = retweeted_status.get("avatar_url")
        #     if avatar_url:
        #         data["retweeted_status"]["avatar_url"] = self.get_oss_img_url(avatar_url)
        #     media_id = retweeted_status.get("media_id")
        #     if media_id:
        #         for index,i in enumerate(media_id):
        #             if i["is_video"]:
        #                 data["retweeted_status"]["media_id"][index]["url"]=self.get_oss_video_url(i["url"])
        #             else:
        #                 data["retweeted_status"]["media_id"][index]["url"]=self.get_oss_img_url(i["url"])
        return data
    def get_oss_img_url(self, url):
        filename = str(time.time()).replace('.', '') + '.jpg'
        # path = re.sub('[?=&%]', '', filename)
        res = requests.get(url=url).content  # 设置代理
        return upload(res, filename)


    def get_oss_video_url(self, video_url):
        # if '&' in detail_url:
        #     detail_url = detail_url.split('&')[0]
        filename = str(time.time()).replace('.', '') + '.mp4'
        res = requests.get(video_url, verify=False).content  # 设置代理
        return upload(res, filename)
