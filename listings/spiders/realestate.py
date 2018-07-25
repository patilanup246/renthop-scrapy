# -*- coding: utf-8 -*-
import scrapy
from listings.items import ListingsItem
import re

class RealestateSpider(scrapy.Spider):
    name = 'realestate'
    allowed_domains = ['renthop.com']
    start_urls = ['https://www.renthop.com/search/nyc?min_price=1500&max_price=4500&q=&neighborhoods_str=1%2C10%2C14%2C11%2C18&sort=hopscore&search=0&page=1/']

    def parse(self, response):
        for listing_url in response.xpath('//a[@class="font-size-11 listing-title-link b"]/@href').extract():
            yield response.follow(listing_url, callback=self.parse_listing)
        next_page = response.xpath('//a[contains(text(), "Next")]/@href').extract()[0]
        if next_page is not 'https://www.renthop.com/search/nyc?min_price=1500&max_price=4500&q=&neighborhoods_str=1%2C10%2C14%2C11%2C18&sort=hopscore&page=2435&search=0':
            yield response.follow(next_page, callback=self.parse)
        
    def parse_listing(self, response):
        for agent_url in response.xpath('//div[@class="b overflow-ellipsis"]/a/@href').extract():
            yield response.follow(agent_url, callback=self.parse_agent_listing)
        
    def parse_agent_listing(self, response):
        item = ListingsItem()
        trans_table = {ord(c): None for c in u'\r\n\t'}
        item['name'] =  response.xpath('//h1[@class="b font-size-15"]/text()').extract()
        item['phone'] = response.xpath('//span[@class="b"]/text()').extract()[0]
        item['email'] =  response.xpath('//a[@class="font-blue font-size-10"]/text()').extract()
        item['firm'] = ' '.join(s.translate(trans_table) for s in response.xpath('//div[@style="padding-top: 2px;"]/text()').extract())
        listings = response.xpath("//html//div[@class='font-size-10 mt-3']//span[2]/text()").extract()[1]
        item['listings'] = re.search('\((.+?)Rentals', listings).group(1)
        item['agent_page'] = response.xpath("//meta[@property='og:url']/@content").extract()
    
        yield item
    