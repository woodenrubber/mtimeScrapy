# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtimescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 电影名称
    movie = scrapy.Field()

    # 电影评论
    comment = scrapy.Field()

    # 电影评分
    score = scrapy.Field()

    # 评论的时间
    time = scrapy.Field()

    # 正向的情感
    positive = scrapy.Field()

    # 负向的情感
    negative = scrapy.Field()

    pass
