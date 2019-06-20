#encoding = "utf-8"
import requests
from lxml import etree
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
	'Referer':'https://movie.douban.com/cinema/nowplaying/anyang/'
}
url = 'https://movie.douban.com/cinema/nowplaying/anyang/'
response = requests.get(url,headers = headers)
text = response.text
movies=[]

html = etree.HTML(text)
ul = html.xpath("//ul[@class='lists']")[0]
lis = ul.xpath("./li")
for i in lis:
	title = i.xpath('@data-title')[0]
	release = i.xpath('@data-release')[0]
	region = i.xpath('@data-region')[0]
	director = i.xpath('@data-director')[0]
	actors = i.xpath('@data-actors')[0]
	img = i.xpath(".//img/@src")[0]
	movie = {
	'title':title,
	'release':release,
	'region':region,
	'director':director,
	'actors':actors,
	'img':img,
	}
	movies.append(movie)
print(movies)


	






