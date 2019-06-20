# -*- coding: utf-8 -*-
import scrapy
import logging

logger = logging.getLogger(__name__)  #实例化logger,这样就可以看到是在哪个文件下执行的这个操作。


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://itcast.cn/']

    def parse(self, response):
    	for i in range(10):

	        item = {}
	        item["come_from"] = "itcast"
	        logger.warning(item)
	        # 使用logging的方法就可以把日志的信息保存在一个单独的文件里，但是print的话只能在终端看到，当我们人离开之后就看不到了
	        
	        yield item

