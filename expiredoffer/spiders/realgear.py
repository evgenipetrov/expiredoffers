# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from expiredoffer.items import ExpiredofferItem
from urllib.parse import urlparse



class RealgearSpider(scrapy.Spider):
    name = 'realgear'
    allowed_domains = [
        'realgear.net',
        'amazon.com',
        'amazon.co.uk',
        'amazon.ca',
        'amazon.de',
        'amzn.to'
    ]
    start_urls = [
        'https://www.realgear.net/'
    ]

    def parse(self, response):

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        if links is not None:
            for item in links:
                parsed = urlparse(item.url)
                if parsed.netloc == 'www.realgear.net':
                    yield response.follow(item, callback=self.parse)
                else:
                    yield scrapy.Request(item.url, self.parse_offer)
        pass

    def parse_offer(self, response):
        loader = ItemLoader(item=ExpiredofferItem(), response=response)
        loader.add_xpath('name', 'normalize-space(//h1[@id="title"]/span/descendant-or-self::text())')
        loader.add_xpath('availability', 'normalize-space(//div[@id="availability"]/span/descendant-or-self::text())')
        loader.add_xpath('asin', 'normalize-space(//form/input[@id="ASIN"]/@value)')
        loader.add_value('url', response.url)
        item = loader.load_item()
        print(item)
        return item

# scrapy crawl realgear -o items.csv -t csv
