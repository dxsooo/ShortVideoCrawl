import scrapy


class KuaishouSpider(scrapy.Spider):
    name = "kuaishou"
    allowed_domains = ["www.kuaishou.com"]
    start_urls = ["http://www.kuaishou.com/"]

    def parse(self, response):
        pass
