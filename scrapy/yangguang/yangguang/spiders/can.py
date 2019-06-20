# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem


class CanSpider(scrapy.Spider):
    name = 'can'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://d.wz.sun0769.com/index.php/question/huiyin']

    def parse(self, response):
        tr_list = response.xpath("//div[@class='newsHead clearfix']/table[2]/tr")
        for tr in tr_list:
        	item = YangguangItem()
        	item['title'] = tr.xpath("./td[3]/a[1]/text()").extract_first()
        	item['href'] = tr.xpath("./td[3]/a[1]/@href").extract_first()
        	item['publish_data'] = tr.xpath("./td[6]/text()").extract_first()


        	yield scrapy.Request(
        			item['href'],
        			callback = self.parse_detail,
        			meta = {'item':item}
        		)
    def parse_detail(self,response):
    	item = response.meta['item']
    	item['content_img'] = response.xpath("//td[@class='txt16_3']//img/@src").extract()
    	item['content_img'] = ['http://wz.sun0769.com'+i for i in item['content_img']]
    	item['content'] = response.xpath("//td[@class='txt16_3']/text()").extract()
    	#print(item)
    	yield item



