# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    allowed_domains = ["craigslist.hk"]
    start_urls = ['http://hongkong.craigslist.hk/search/apa?sort=date&availabilityMode=0&max_bedrooms=1']

    def parse(self, response):
        apas=response.xpath("//p[@class='result-info']")
        for apa in apas:
        	name = apa.xpath("a/text()").extract_first()
        	price = apa.xpath("span[@class='result-meta']/span[@class='result-price']/text()").extract_first()
        	address = apa.xpath("span[@class='result-meta']/span[@class='result-hood']/text()").extract_first("")[2:-1]
        	url_detail = apa.xpath("a/@href").extract_first()
        	yield Request(url_detail, callback=self.parse_detail,meta={"Url":url_detail,"Name":name, "Price":price, "Address":address})
        next_rel = response.xpath("//a[@class='button next']/@href").extract_first()
        next_abs = response.urljoin(next_rel)
        yield Request(next_abs, callback=self.parse)

    def parse_detail(self, response):
    	name = response.meta['Name']
    	price = response.meta['Price']
    	address = response.meta['Address']
    	desc=response.xpath("//*[@id='postingbody']/text()").extract()
    	phones = list(filter(None, [re.findall(r'[0-9]{4} [0-9]{4}',d) for d in desc]))
    	phone = ",".join(p[0] for p in phones if p)
    	response.meta['phone']=phone
    	yield {"Name":name, "Price":price, "Address":address, "Phone":phone}


# scrapy shell "https://hongkong.craigslist.hk/apa/d/sfurnished-studio-in-shek/6434935695.html"
# desc=response.xpath("//*[@id='postingbody']/text()").extract()
# phones = list(filter(None, [re.findall(r'[0-9]{4} [0-9]{4}',d) for d in desc]))
# phone = ",".join(p[0] for p in phones if p)