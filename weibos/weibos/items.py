# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    release_time = scrapy.Field()
    release_state = scrapy.Field()
    # twr_item["read_amount"] = scrapy.Field()
    is_repost = scrapy.Field()
    twitter_id = scrapy.Field()
    tw_or_ins = scrapy.Field()
    nick_name = scrapy.Field()
    author_id_rl = scrapy.Field()
    weibo_id = scrapy.Field()
    # twr_item["correct_state"] = scrapy.Field()
    data_en = scrapy.Field()
    avatar_url = scrapy.Field()
    media_id = scrapy.Field()
    retweeted_status = scrapy.Field()
    type = scrapy.Field()
    weibo_url = scrapy.Field()
