from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem

class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["poets.org"]
    start_urls = [
            "http://www.poets.org/poetsorg/poems"
        ]

    def parse(self, response):
        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = StackItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
    # name = "stack"
    # allowed_domains = ["stackoverflow.com"]
    # start_urls = [
    #     "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    # ]

    # def parse(self, response):
    #     questions = Selector(response).xpath('//div[@class="summary"]/h3')

    #     for question in questions:
    #         item = StackItem()
    #         item['title'] = question.xpath(
    #             'a[@class="question-hyperlink"]/text()').extract()[0]
    #         item['url'] = question.xpath(
    #             'a[@class="question-hyperlink"]/@href').extract()[0]
    #         yield item