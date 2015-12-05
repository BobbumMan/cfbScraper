# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GameItem(scrapy.Item):
    home = scrapy.Field()
    away = scrapy.Field()
    date = scrapy.Field()
    _id = scrapy.Field()
    
class BoxItem(scrapy.Item):
    team_name = scrapy.Field()
    date = scrapy.Field()
    position = scrapy.Field()
    carries = scrapy.Field()
    rushing_yards = scrapy.Field()
    rushing_tds = scrapy.Field()
