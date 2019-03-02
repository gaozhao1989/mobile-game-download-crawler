# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GamedownloadItem(scrapy.Item):
    # define the fields for your item here like:
    gameId = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    screenCapture = scrapy.Field()
    logoUrl = scrapy.Field()
    size = scrapy.Field()
    keyWord = scrapy.Field()
    score = scrapy.Field()
    category = scrapy.Field()
    androidDownloadUrl = scrapy.Field()
    iosDownloadUrl = scrapy.Field()
