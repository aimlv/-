# -*- coding: utf-8 -*-
import scrapy
import re


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/971121542/profile']
    def start_requests(self):
    	cookies = "anonymid=jwpnsua4-nq0cu6; depovince=HEN; _r01_=1; JSESSIONID=abclorWdle92j4Rmm3_Sw; ick_login=c6392173-f320-4cba-b320-038635327022; _de=C8716255095AA2EED1133785475A9C156DEBB8C2103DE356; ick=bb81772a-c518-4b00-80fc-22106b4c66a4; t=2efdc7d4a14570dfda71c6112d0bc9222; societyguester=2efdc7d4a14570dfda71c6112d0bc9222; id=971121542; xnsid=c1222b19; XNESSESSIONID=621d9d566195; ver=7.0; loginfrom=null; jebe_key=8b9941f5-4173-4f93-afc2-ac63a8f730b7%7C29fea3226f08ae4a7276e95f230da8be%7C1560128039766%7C1%7C1560128041186; wp_fold=0; jebecookies=63ac552f-b70c-4b18-b04c-fb7ceaf2c5b0|||||"
    	cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; " )}
    	yield scrapy.Request(
    		self.start_urls[0],
    		callback=self.parse,
    		cookies=cookies
    		)
    def parse(self, response):
        print(re.findall("吕晓亮",response.body.decode()))
        yield scrapy.Request(
        		"http://www.renren.com/971121542/profile?v=info_timeline",
        		callback=self.parse_detail,
        		        	)
    def parse_detail(self,response):
    	print(re.findall("信息科学技术学院",response.body.decode()))
