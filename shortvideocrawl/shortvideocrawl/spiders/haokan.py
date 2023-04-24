import json

import scrapy

from ..items import ShortvideocrawlItem


class HaokanSpider(scrapy.Spider):
    name = "haokan"
    allowed_domains = ["haokan.baidu.com"]

    query = "蔡徐坤"
    count = 20

    def parse(self, response):
        pass
