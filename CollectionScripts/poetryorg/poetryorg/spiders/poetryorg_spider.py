# -*- coding: utf-8 -*-
import scrapy
from poetryorg.items import PoetItem, PoemItem
import urlparse
import re


class poetryspider(scrapy.Spider):
    name = "poetryspider"
    allowed_domains = ["poets.org"]
    start_urls = [
        "http://www.poets.org/"
    ]

    def parse(self, response):
        movements_to_scrape = ["Beat","Black Arts","Black Mountain","Conceptual Poetry","Concrete Poetry",
                               "Confessional Poetry","Contemporary","Dark Room Collective","Formalism","Futurism",
                               "Harlem Renaissance","Jazz Poetry","Language Poetry","Modernism","New Formalism",
                               "New York School","Objectivists","San Francisco Renaissance","Slam/Spoken Word",
                               "Surrealism","Symbolists"]
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//div[@class = "school_movements"]//ul/li/a')
        for s in sites:
            if ''.join(s.xpath('text()').extract()) in movements_to_scrape:
                movement_name = s.xpath('text()').extract()
                link = u''.join(s.xpath('@href').extract())
                movement_url = urlparse.urljoin("http://www.poets.org",link)
                yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",link), callback=self.parse_movement, meta = {'movement_name': movement_name, 'movement_url':movement_url})

    def parse_movement(self, response):
        movement_name = response.meta['movement_name']
        movement_url = response.meta['movement_url']
        y = scrapy.Selector(response)
        poetnextpagelink = u''.join(y.xpath('//a[@title = "Go to next page"]/@href').extract())
        s = y.xpath('//tbody/tr')
        for i in s:
            item = PoetItem()
            item['movement_name'] = movement_name
            item['movement_url'] = movement_url
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

        if len(poetnextpagelink) > 0:
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",poetnextpagelink), callback=self.parse_movement, meta = {'movement_name': movement_name, 'movement_url':movement_url})


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
        poet_poems_url = response.meta['poet_poems_url']
        y = scrapy.Selector(response)
        nextpagelink = u''.join(y.xpath('//a[@title = "Go to next page"]/@href').extract())
        poem_rows = y.xpath('//tbody/tr')
        regex = re.compile(r'audio')

        for i in poem_rows:
            if len(i.xpath('td/a/@href').extract()[0]) > 0 :
                poemlink = u''.join(i.xpath('td/a/@href').extract()[0])
                linktext = str(poemlink)
                if regex.search(linktext) is None:
                    if len(i.xpath('td//text()').extract())>0:
                        poemitem = PoemItem()
                        poemitem['poet_poems_url'] = poet_poems_url
                        poemitem['poem_yrpub'] = i.xpath('td//text()').extract()[1]
                        poemitem['poem_title'] = i.xpath('td//text()').extract()[4]
                        poemitem['poem_link'] = urlparse.urljoin("http://www.poets.org",poemlink)
                        yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",poemlink), callback=self.parse_poet_poem, meta={'poemitem': poemitem})

        if len(nextpagelink) > 0:
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",nextpagelink), callback=self.parse_poet_poems, meta= {'poet_poems_url': poet_poems_url})

    def parse_poet_poem(self, response):
        poemitem = response.meta['poemitem']
        y = scrapy.Selector(response)
        poemitem['poem_text'] = y.xpath('//div[@property = "content:encoded"]//text()').extract()
        poemitem['poem_copyright'] = y.xpath('//div[@class = "poem-credit"]//p//text()').extract()
        yield poemitem


