# -*- coding: utf-8 -*-
import scrapy


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/?labelWords=label']


    def parse(self, response):
        li_list = response.xpath("//ul[@class='item_con_list']//li")
        for li in li_list:
        	item = {}
        	item['title'] = li.xpath(".//h3/text()").extract_first()
        	yield item



