import scrapy


class HaokanSpider(scrapy.Spider):
    name = "haokan"
    allowed_domains = ["haokan.baidu.com"]
    # start_urls = ["http://haokan.baidu.com/"]

    def parse(self, response):
        pass
