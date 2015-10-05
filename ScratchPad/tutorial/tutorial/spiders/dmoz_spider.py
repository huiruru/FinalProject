# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import PoItem
import urlparse
import re

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["poets.org"]
    start_urls = [
    		"http://www.poets.org/"
	    ]

    def parse(self, response):
        item = PoItem()
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class = "school_movements"]//ul/li/a')
        for s in sites:
            item['movement_name'] = s.xpath('text()').extract()
            link = u''. join(s.xpath('@href').extract())
            item['movement_url'] = urlparse.urljoin("http://www.poets.org",link)
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",link), callback=self.parse_movement, meta = {'item': item}) 

    def parse_movement(self, response):
        item = response.meta['item']
        y = scrapy.Selector(response)
        s = y.xpath('//tbody/tr/td')
        for i in s:
            if len(i.xpath('a/text()').extract())>0:
                # print i.xpath('a/text()').extract()
                item['poet_name'] = i.xpath('a/text()').extract()
            if len(i.xpath('a/@href').extract())>0:
                link = u''.join(i.xpath('a/@href').extract())
                item['poet_url'] = urlparse.urljoin("http://www.poets.org",link)
            if len(i.xpath('span/text()').extract()) > 0:
                # print i.xpath('span/text()').extract()
                item['poet_dob2'] = i.xpath('span/text()').extract()
            if len(i.xpath('text()').extract()[0])>0:
                # print i.xpath('text()').extract()[0]
                item['poet_tags'] = i.xpath('text()').extract()[0]
            yield scrapy.Request(url =urlparse.urljoin("http://www.poets.org",link), callback=self.parse_poet, meta = {'item': item})

    def parse_poet(self, response):
        item = response.meta['item']
        y = scrapy.Selector(response)
        x = y.xpath('//div[@class="view-content"]')
        item['poet_basicbio'] = x[0].xpath('div/span//text()').extract()
        item['poet_positions'] = x[0].xpath('div//div/text()').extract()
        item['poet_posyears'] = x[0].xpath('div//div/span/text()').extract()
        item['poet_bio'] = y.xpath('//div[@class="field-items"]//p//text()').extract()
        poetpoemlink = u''.join(y.xpath('//div[@class="view-footer"]/a/@href').extract())
        item['poet_poems_url'] = urlparse.urljoin("http://www.poets.org",poetpoemlink)
        yield item
        # yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",poetpoemlink), callback=self.parse_poems)

    def parse_poems(self, response):
        pass
        # y = scrapy.Selector(response)
        # s = y.xpath('//tbody/tr/td')
        # regex = re.compile(r'audio')
        # for i in s:
        #     poemlink = u''.join(i.xpath('a/@href').extract())
        #     linktext = str(poemlink)
        #     if len(i.xpath('span/text()').extract())>0:
        #         item['poem_yrpub'] = i.xpath('span/text()').extract()
        #     if regex.search(linktext) is None:
        #         item['poem_title'] = i.xpath('a/text()').extract()
        #         item['poem_link'] = urlparse.urljoin("http://www.poets.org",poemlink)




    	# for sel in response.xpath('//div[@class = "school_movements"]'):
     #        item = DmozItem()
     #        item['title'] = sel.xpath('a/text()').extract()
     #        item['link'] = sel.xpath('a/@href').extract()
     #        item['desc'] = sel.xpath('text()').extract()
     #        yield item