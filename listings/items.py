# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ListingsItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    firm = scrapy.Field()
    listings = scrapy.Field()
    agent_page = scrapy.Field()