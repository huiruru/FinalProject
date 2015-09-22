# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["poets.org"]
    start_urls = [
    		"http://www.poets.org/poetsorg/poets"
	    ]

    def parse(self, response):
    	for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
    		url = response.urljoin(href.extract())
    		yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse(self, response):
    	for sel in response.xpath('//ul/li'):
    		item = DmozItem()
    		item['title'] = sel.xpath('a/text()').extract()
    		item['link'] = sel.xpath('a/@href').extract()
    		item['desc'] = sel.xpath('text()').extract()
    		yield item