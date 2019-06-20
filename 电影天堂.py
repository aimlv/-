from lxml import etree
import requests
BASE_DOMIN = 'https://www.dytt8.net'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
	
}
def get_detail_urls(url):
	response = requests.get(url,headers = HEADERS)
	text = response.text
	html = etree.HTML(text)
	detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
	detail_urls = map(lambda url:BASE_DOMIN+url,detail_urls)
	return detail_urls

def parse_detail_page(url):
	movie = {}
	response = requests.get(url,headers = HEADERS)
	text = response.content.decode('gbk')
	html = etree.HTML(text)
	title = html.xpath("//div[@class='title_all']//font/text()")[0]
	movie['title'] = title

	Zoom = html.xpath("//div[@id='Zoom']")[0]
	imgs = Zoom.xpath(".//img/@src")
	cover = imgs[0]
	screenshot = imgs[1]
	movie['cover'] = cover
	movie['screenshot'] =screenshot

	def parse_info(info,rule):
		return info.replace(rule,"").strip()
	infos = Zoom.xpath(".//text()")
	for index,info in enumerate(infos):
		
		if info.startswith("◎年　　代　2018"):
			info = parse_info(info,"◎年　　代")
			movie['year'] = info
		elif info.startswith("◎产　　地"):
			info = parse_info(info,"◎产　　地")
			movie['country'] = info
		elif info.startswith("◎类　　别"):
			info = parse_info(info,"◎类　　别")
			movie['category'] = info
		elif info.startswith("◎豆瓣评分"):
			info = parse_info(info,"◎豆瓣评分")
			movie['douban_rating'] = info
		elif info.startswith("◎片　　长"):
			info = parse_info(info,"◎片　　长")
			movie['duration'] = info
		elif info.startswith("◎导　　演"):
			info = parse_info(info,"◎导　　演")
			movie['director'] = info
		elif info.startswith("◎主　　演"):
			info = parse_info(info,"◎主　　演")
			actors = [info]

			for x in range(index+1,len(infos)):
				actor = infos[x].strip()
				if actor.startswith("◎"):
					break
				actors.append(actor)
				movie['actors'] = actors
		elif info.startswith("◎简　　介"):
			info = parse_info(info,"◎简　　介")
			for x in range(index+1,len(infos)):
				profile = infos[x].strip()
				
				movie['profile'] = profile

				if profile.startswith("【下载地址】"):
					break

	download_url = Zoom.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
	movie['download_url'] = download_url
	return movie




	
def spider():
	base_url='https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
	movies = []
	for x in range(1,8):
		url = base_url.format(x)
		detail_urls = get_detail_urls(url)
		for detail_url in detail_urls:
			movie = parse_detail_page(detail_url)
			movies.append(movie)
			print(movies)



if __name__ == '__main__':
	spider()
