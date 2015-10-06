# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import PoetItem, PoemItem
import urlparse
import re

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["poets.org"]
    start_urls = [
        "http://www.poets.org/"
    ]

    def parse(self, response):
        item = PoetItem()
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class = "school_movements"]//ul/li/a')
        for s in sites:
            item['movement_name'] = s.xpath('text()').extract()
            link = u''.join(s.xpath('@href').extract())
            item['movement_url'] = urlparse.urljoin("http://www.poets.org",link)
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",link), callback=self.parse_movement, meta = {'item': item}) 

    def parse_movement(self, response):
        item = response.meta['item']
        y = scrapy.Selector(response)
        s = y.xpath('//tbody/tr')
        for i in s:
            if len(i.xpath('td/a/text()').extract())>0:
                # print i.xpath('a/text()').extract()
                item['poet_name'] = i.xpath('td/a/text()').extract()
            if len(i.xpath('td/a/@href').extract())>0:
                link = u''.join(i.xpath('td/a/@href').extract())
                item['poet_url'] = urlparse.urljoin("http://www.poets.org",link)
            if len(i.xpath('td/span/text()').extract()) > 0:
                # print i.xpath('span/text()').extract()
                item['poet_dob2'] = i.xpath('td/span/text()').extract()
            if len(i.xpath('td/text()').extract())>0:
                # print i.xpath('text()').extract()[0]
                item['poet_tags'] = i.xpath('text()').extract()
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
        poet_poems_url = urlparse.urljoin("http://www.poets.org",poetpoemlink)
        item['poet_poems_url'] = poet_poems_url
        yield item
        yield scrapy.Request(url=poet_poems_url, callback=self.parse_poet_poems, meta={'poet_poems_url': poet_poems_url })

    def parse_poet_poems(self, response):
        y = scrapy.Selector(response)
        poem_rows = y.xpath('//tbody/tr')
        regex = re.compile(r'audio')

        for i in poem_rows:
            poemitem = PoemItem()
            poemitem['poet_poems_url'] = response.meta['poet_poems_url']

            if len(i.xpath('td/a/@href').extract()[1]) > 0 :
                poemlink = u''.join(i.xpath('a/@href').extract())
                linktext = str(poemlink)
                if regex.search(linktext) is None:
                    if len(i.xpath('td//text()').extract()[1])>0:
                        poemitem['poem_yrpub'] = i.xpath('td//text()').extract()[1]
                        poemitem['poem_title'] = i.xpath('td/text()').extract()[4]
                        poemitem['poem_link'] = urlparse.urljoin("http://www.poets.org",poemlink)
                        yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",poemlink), callback=self.parse_poet_poem, meta={'poemitem': poemitem})

        nextpagelink = u''.join(y.xpath('//a[@title = "Go to next page"]/@href').extract())
        if len(nextpagelink) > 0:
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",nextpagelink), callback=self.parse_poet_poems, meta= {'poet_poems_url': poet_poems_url})


    def parse_poet_poem(self, response):
        poemitem = response.meta['poemitem']
        y = scrapy.Selector(response)
        poemitem['poem_text'] = y.xpath('//div[@class = "field-items"]//pre/text()').extract()
        poemitem['poem_copyright'] = y.xpath('//div[@class = "field-items"]//p//text()').extract()
        yield poemitem


