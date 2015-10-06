# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoetItem(scrapy.Item):
    movement_name = scrapy.Field()
    movement_url = scrapy.Field()
    poet_name = scrapy.Field()
    poet_url = scrapy.Field()
    #poet_dob is the dob scraped from poet page
    poet_dob = scrapy.Field()
    #poet_from is the yrs scraped from movement
    #some times no dob is available on poet page, 
    #this is secondary source
    poet_dob2 = scrapy.Field()
    #a poet may be tagged with multiple movements
    poet_tags = scrapy.Field()

    #from poembio page
    poet_basicbio = scrapy.Field()
    poet_bio = scrapy.Field()

    poet_positions = scrapy.Field()
    poet_posyears = scrapy.Field()
    poet_poems_url = scrapy.Field()

class PoemItem(scrapy.Item):
    poet_poems_url = scrapy.Field()
    poem_link = scrapy.Field()
    poem_yrpub = scrapy.Field()
    poem_title = scrapy.Field()
    poem_text = scrapy.Field()
    poem_copyright = scrapy.Field




# class PoemItem(scrapy.Item):