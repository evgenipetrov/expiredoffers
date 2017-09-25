# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from expiredoffer.items import ExpiredofferItem


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

        loader = ItemLoader(item=ExpiredofferItem(), response=response)
        loader.add_xpath('name', '//div[@class="product_name"]')
        loader.add_xpath('availability', '//div[@class="product_title"]')
        loader.add_xpath('url', '//p[@id="price"]')
        yield loader.load_item()

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        if links is not None:
            for url in links:
                yield response.follow(url, callback=self.parse)

        pass
