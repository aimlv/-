# -*- coding: utf-8 -*-
import scrapy
import re

from copy import deepcopy   
#第1个问题. 在没有引用deepcopy的时候  是赋值   这时候因为整个过程都使用同一个item  这时候所有的def函数同时运行  这时候其中的item相互影响 导致结果出现
# 重复值。  但是使用deepcopy的时候  是引用  这时候引用之后的值不会对其他的值造成影响，所以结果不会出现重复值。
# 第2个问题：就是为什么在前两个项目中（腾旭招聘、和阳光政府平台）就没有出现这种情况（出现结果值重复）这是因为在这个项目中有两个分类 第一个是
# 大分类 然后大分类下还有一个小分类  这两个分类用了一个item，而在另外两个项目中  则分别有自己的item，而且只有一个分类 所以不会相互影响。

class SnSpider(scrapy.Spider):
    name = 'sn'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/?safp=d488778a.13705.0.8cca61ce53']

    def parse(self, response):
    	#大标签
        div_list = response.xpath("//div[@class='menu-list']/div")
        for div in div_list:
        	item = {}
        	item['h_cate'] = div.xpath("./dl/dt/h3/a/text()").extract_first()
        	#小标签
        	a_list = div.xpath(".//dd/a")
        	for a in a_list:

        		item['a_href'] = a.xpath("./@href").extract_first()
        		item['a_cate'] = a.xpath("./text()").extract_first()

        		yield scrapy.Request(
        				item["a_href"],
        				callback=self.parse_book_list,
        				meta={"item":deepcopy(item)}
        			)
    def parse_book_list(self,response):
    	item = response.meta["item"]
    	li_list = response.xpath("//div[@class='filter-results productMain clearfix  temporary']/ul/li")
    	for li in li_list:
    		item['book_text'] = li.xpath(".//div[@class='img-block']/a/img/@alt").extract_first()
    		item['book_href'] = li.xpath(".//div[@class='img-block']/a/@href").extract_first()
    		if item['book_href'] is not None:
    			item['book_href'] = 'https:'+ item['book_href']
    		item['book_img'] = li.xpath(".//div[@class='img-block']/a/img/@src2").extract_first()
    		if item['book_img'] is not None:
    			r = 'https:' + item['book_img']
    			item['boo_img'] = re.sub(r"_220w_220h_4e","",r)
    		

    			yield scrapy.Request(
    					item['book_href'],
    					callback = self.parse_detail_book,
    					meta={"item":deepcopy(item)}
				)
				#翻页
				# （翻页的方法还要多看一下，这个方法很有用  明天接着看这个方法）
				# 1.第一种方法：使用标签的方式自己构造：(eeee  好像不对 ，反正没有成功 尝试下一个方式)
				# i = 0
				# next_url = 'https://list.suning.com//1-502320-{i}-0-0-0-0-14-0-4.html'
				# for i in range(1,100):
				#
				#2.第二个方法：正则表达式
				page_count = re.findall("param.pageNumbers = \"(.*?)\";",response.body.decode())[0]
				page_current = re.findall("param.currentPage = \"(.*?)\";",response.body.decode())[0]
				if page_current<page_count:
					next_url = "https://list.suning.com/emall/showProductList.do?ci=502320&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=372".format(page_current+1),
					
					yield scrapy.Request(
							next_url,
							callback = self.parse_book_list,
							meta = {"item":deepcopy(item)}
						)
    	
    def parse_detail_book(self,response):
    	item = response.meta['item']
    	# li_list = response.xpath("//ul[ul[class='bk-publish clearfix']/li")
    	# for li in li_list():
    	# 	item['author'] = li.xpath("./span/text()").extract_first()

    	item['author'] = response.xpath("//ul[@class='bk-publish clearfix']/li[1]/text()").extract_first()
    	# item['author'] = [re.sub(r"\r\t\n|\s|\'","",i)for i in item['author']]  这个替换没有做好  ，还有字符的问题，需要解决
    	item['author'] = [i for i in item['author'] if len(i)>0]
    	item['publish'] = response.xpath("//ul[@class='bk-publish clearfix']/li[2]/text()").extract_first()
    	item['time'] = response.xpath("//ul[@class='bk-publish clearfix']/li[3]/span/span/text()").extract_first()
    	
    	print(item)


    	# content = [re.sub(r"\xa0|\s|\r\n","",i) for i in content]   #使用正则表达式，替换特殊字符串和空字符串  而strip函数只能去掉字符符旁边的空格。
    	# content = [i for i in content if len(i)>0]  #去除列表中的空字符串
    	
    	# ajkx 的请求方式：
    	# url:https://list.suning.com/emall/showProductList.do?ci=502320&pg=03&cp=0&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=372&paging=1&sub=0
    	# url:https://list.suning.com/emall/showProductList.do?ci=502320&pg=03&cp=1&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=372
    	# url:https://list.suning.com/emall/showProductList.do?ci=502320&pg=03&cp=2&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=372
    	# url:https://list.suning.com/emall/showProductList.do?ci=502320&pg=03&cp=3&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=372

