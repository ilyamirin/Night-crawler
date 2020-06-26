import scrapy
from scrapy_splash import SplashRequest
#%%

class parse_ESSE(scrapy.Spider):
    name = "links"
    def start_requests(self):
        with open('link.txt','r') as file:
            link = file.read.strip()
            link.replace(' ','%20')
        url = 'https://yandex.ru/search/?lr=75&text=' + link + '&p=1'
        urls = [url]
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')
    def parse(self, response):
        #Для яндекса
        import datetime
        import time
        import random
        links = response.xpath('//ul[@id = "search-result"]/li[@class = "serp-item"]/div/h2/a/@href').getall()
        print(links)

        with open('scraped_links/'+'file'+datetime.datetime.now().__str__(),'w') as f:
            links = "\n".join(links)
            f.write(links)
        next_page = response.xpath('//a[@aria-label = "Следующая страница"]/@href').get()
        print('_____________',response.url,'_____________')
        print('NEXT PAGE',next_page)
        time.sleep(random.randint(5,10) + random.random())
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(url=next_page, callback=self.parse, endpoint='render.html')

