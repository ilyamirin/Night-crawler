import scrapy
import json
import datetime
from urllib.parse import urlparse
import os
import re
#%%
import first_filter
import second_filter

#%%
def links_filter(links):
    f_links = []
    for i in links:
        if i.find('.pdf') != -1:
            continue
        if i.find('wikipedia') != -1:
            continue
        elif i.find('youtube') != -1:
            continue
        elif i.find('facebook') != -1:
            continue
        elif i.find('google') != -1:
            continue
        elif i.find('contact') != -1:
            continue
        elif i.find('seo') != -1:
            continue
        elif i.find('wordpress.com') != -1:
            continue
        elif i.find('privacy') != -1:
            continue
        elif i.find('twitter') != -1:
            continue
        elif not i.startswith('http'):
            continue
        else:
            f_links.append(i)
    f_links = list(set(f_links))
    return f_links

def get_domains(links):
    domains = []
    for i in links:
        domains.append(urlparse(i).netloc)
    return domains
#%%
path_links = 'links/'
MAX_PAGES = 6000
class parse_ESSE(scrapy.Spider):
    name = "ESSE"
    pages_num = 0
    
    t_name = str(datetime.datetime.now())[:-7]
    file_ind = 1
    
    #Считываются начальные ссылки из файлов в папке links
    file_names = [f for f in os.listdir(path_links) if os.path.isfile( os.path.join(path_links, f))]
    links = [path_links + f for f in file_names]
    urls = []
    for i in links:
        f = open(i,'r')
        f_url = [u.strip() for u in f.read().split('\n') if u.strip() != '']
        urls += f_url
        f.close()
    urls = links_filter(urls)
    
    #Старые ссылки при переходе на которые считываются только ссылки для перехода
    #без эссе
    with open('data/old_links.txt','r') as file:
        old_links = file.read().strip().split('\n')
    #Переход на сторонние домены
    allowed_domains = get_domains(urls)
    print(allowed_domains)
    start_urls = urls
    print(start_urls)
    
    def parse(self, response):
        self.pages_num += 1
        #Ограничение по просмортенным страницам
        if self.pages_num > MAX_PAGES:
            print('END')
            raise scrapy.exceptions.CloseSpider('bandwidth_exceeded')
        #Проверка на то, что по этой ссылке не отбирались тексты
        if response.url not in self.old_links:
            texts = response.xpath("//body//*").xpath('string(.)').re(r'[A-Z]+[a-zA-Z0-9\s.,!?:°;\’`"\'-]+[.!?]')
            text = first_filter.check_text(texts)
            texts = second_filter.filter_one(text)
            if texts != None:
                self.old_links.append(response.url)
                with open('data/old_links.txt','a') as file:
                    file.write(response.url)
                    file.write('\n')
                texts = list(set(texts))
                for text in texts:
                    with open('scraped_data/' + self.t_name + '_' + str(self.file_ind) + '.json','w+') as f:
                        data = [{response.url:text}]
                        json.dump(data,f)
                        self.file_ind += 1
        links = response.xpath("//a/@href").getall()
        links = [response.urljoin(i) for i in links]
        links = links_filter(links)
        for i in range(len(links)):
            yield scrapy.Request(url=links[i], callback=self.parse, meta={'dont_redirect': True})

