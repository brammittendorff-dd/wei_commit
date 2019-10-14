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
    weibo = scrapy.Field()
    description = scrapy.Field()
    data = scrapy.Field()
    share_image_url = scrapy.Field()
    create_time = scrapy.Field()
    media_id = scrapy.Field()
    label_id = scrapy.Field()
    dynamicsource = scrapy.Field()
    source = scrapy.Field()
    star_keyword = scrapy.Field()
    dynamicsource_id = scrapy.Field()
    url = scrapy.Field()

