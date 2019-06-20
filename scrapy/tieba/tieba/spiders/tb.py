# -*- coding: utf-8 -*-
import scrapy


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tib.com']
    start_urls = ['http://tib.com/']

    def parse(self, response):
        pass
