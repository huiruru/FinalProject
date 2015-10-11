# -*- coding: utf-8 -*-
import scrapy
from poetryorg.items import PoetItem, PoemItem
import urlparse
import re


class poetryspider(scrapy.Spider):
    """
        This spider crawls poets.org site and pipes poets, and their poems to poets & poems collection in mongodb poetry
        database
    """
    name = "poetryspider"
    allowed_domains = ["poets.org"]
    start_urls = ["http://www.poets.org/"]

    #rules =

    def parse(self, response):
        """
            This method parses poetic movements as specified in the movements_to_scrape list, follows each movement link
            and yields a request using parse_movement method
        """
        movements_to_scrape = ["Beat","Black Arts","Black Mountain","Conceptual Poetry","Concrete Poetry",
                               "Confessional Poetry","Contemporary","Dark Room Collective","Formalism","Futurism",
                               "Harlem Renaissance","Jazz Poetry","Language Poetry","Modernism","New Formalism",
                               "New York School","Objectivists","San Francisco Renaissance","Slam/Spoken Word",
                               "Surrealism","Symbolists"]

        sresponse = scrapy.Selector(response)

        #sites are selectors found in the school movements table
        sites = sresponse.xpath('//div[@class = "school_movements"]//ul/li/a')
        for site in sites:
            if ''.join(site.xpath('text()').extract()) in movements_to_scrape:
                movement_name = site.xpath('text()').extract()
                link = u''.join(site.xpath('@href').extract())
                movement_url = urlparse.urljoin("http://www.poets.org",link)
                yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",link), callback=self.parse_movement,
                                     meta = {'movement_name': movement_name, 'movement_url':movement_url})

    def parse_movement(self, response):
        """
            This method looks at each movement page and creates a new PoetItem for each poet found in page's table
        """
        movement_name = response.meta['movement_name']
        movement_url = response.meta['movement_url']

        sresponse = scrapy.Selector(response)

        #Because each movement page contains a table that has maximum of ten rows, we need to go to the next page
        #in order to extract all of the poets associated for each movement
        poetnextpagelink = u''.join(sresponse.xpath('//a[@title = "Go to next page"]/@href').extract())

        table = sresponse.xpath('//tbody/tr')
        for row in table:
            item = PoetItem()
            item['movement_name'] = movement_name
            item['movement_url'] = movement_url
            if len(row.xpath('td/a/text()').extract())>0:
                item['poet_name'] = row.xpath('td/a/text()').extract()
            if len(row.xpath('td/a/@href').extract())>0:
                #the link is for the poet bio page on poetry.org website
                link = u''.join(row.xpath('td/a/@href').extract())
                item['poet_url'] = urlparse.urljoin("http://www.poets.org",link)
            if len(row.xpath('td/span/text()').extract()) > 0:
                item['poet_dob2'] = row.xpath('td/span/text()').extract()
            if len(row.xpath('td/text()').extract())>0:
                #a poet may be tagged/associated with multiple movements
                item['poet_tags'] = row.xpath('td/text()').extract()
            yield scrapy.Request(url =urlparse.urljoin("http://www.poets.org",link), callback=self.parse_poet,
                                 meta = {'item': item})

        #if more poets on next page, use this method again
        if len(poetnextpagelink) > 0:
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",poetnextpagelink),
                                 callback=self.parse_movement, meta = {'movement_name': movement_name,
                                                                       'movement_url':movement_url})


    def parse_poet(self, response):
        """
            This method scrapes data (bio, url of all poems) from each poet page to continue creating the poet item
        """
        item = response.meta['item']

        sresponse = scrapy.Selector(response)
        poetdata = sresponse.xpath('//div[@class="view-content"]')

        #TODO: Clear empty strings from poet item fields

        item['poet_basicbio'] = poetdata[0].xpath('div/span//text()').extract()
        item['poet_positions'] = poetdata[0].xpath('div//div/text()').extract()
        item['poet_posyears'] = poetdata[0].xpath('div//div/span/text()').extract()
        item['poet_bio'] = sresponse.xpath('//div[@class="field-items"]//p//text()').extract()

        #this important link goes to the page of poems for each poet
        poetpoemlink = u''.join(sresponse.xpath('//div[@class="view-footer"]/a/@href').extract())
        poet_poems_url = urlparse.urljoin("http://www.poets.org",poetpoemlink)

        item['poet_poems_url'] = poet_poems_url

        #PoetItem finishes here
        yield item

        #goes to method that parses poems found in the poet_poems_url
        yield scrapy.Request(url=poet_poems_url, callback=self.parse_poet_poems, meta={'poet_poems_url': poet_poems_url })

    def parse_poet_poems(self, response):
        """
            This method parses the poems found in the page of all poems available for a specific poet
            The poet poems url is the foreign key to poets collection
        """
        poet_poems_url = response.meta['poet_poems_url']

        sresponse = scrapy.Selector(response)

        #like the movement pages, this page contains a table that has maximum of ten rows, we need to go to the next
        # page in order to extract all of the poems associated with each poet
        nextpagelink = u''.join(sresponse.xpath('//a[@title = "Go to next page"]/@href').extract())

        table_poems = sresponse.xpath('//tbody/tr')

        #poetry.org does not provide text for all of the poems available, some links are for audio versions only,
        #therefore need to avoid storing poemitems that are not text
        regex = re.compile(r'audio')

        for row in table_poems:
            if len(row.xpath('td/a/@href').extract()[0]) > 0 :
                poemlink = u''.join(row.xpath('td/a/@href').extract()[0])
                linktext = str(poemlink)
                if regex.search(linktext) is None:
                    if len(row.xpath('td//text()').extract())>0:
                        poemitem = PoemItem()
                        poemitem['poet_poems_url'] = poet_poems_url
                        poemitem['poem_yrpub'] = row.xpath('td//text()').extract()[1]
                        poemitem['poem_title'] = row.xpath('td//text()').extract()[4]
                        poemitem['poem_link'] = urlparse.urljoin("http://www.poets.org",poemlink)
                        yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",poemlink),
                                             callback=self.parse_poet_poem, meta={'poemitem': poemitem})

        #if more poems on next page, use this method again
        if len(nextpagelink) > 0:
            yield scrapy.Request(url = urlparse.urljoin("http://www.poets.org",nextpagelink),
                                 callback=self.parse_poet_poems, meta= {'poet_poems_url': poet_poems_url})

    def parse_poet_poem(self, response):
        """
            This method parses each poem on poem pages and finally yields the poemitems
        """
        poemitem = response.meta['poemitem']
        sresponse = scrapy.Selector(response)
        poemitem['poem_text'] = sresponse.xpath('//div[@property = "content:encoded"]//text()').extract()
        poemitem['poem_copyright'] = sresponse.xpath('//div[@class = "poem-credit"]//p//text()').extract()

        yield poemitem


