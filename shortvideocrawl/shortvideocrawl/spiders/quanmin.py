import scrapy
import json
from urllib.parse import urlencode

from ..items import ShortvideocrawlItem

SEARCH_API = "https://quanmin.baidu.com/wise/growth/api/home/searchmorelist"


class QuanminSpider(scrapy.Spider):
    name = "quanmin"
    allowed_domains = ["quanmin.baidu.com"]

    query = "蔡徐坤"
    count = 10

    def start_requests(self):
        yield self.search_request(0)

    def search_request(self, page: int):
        query = {
            "rn": 12,
            "pn": page,
            "q": self.query,
            "type": "search",
            "_format": "json",
        }

        # https://quanmin.baidu.com/wise/growth/api/home/searchmorelist?rn=12&pn=0&q=蔡徐坤&type=search&_format=json
        print(SEARCH_API + "?" + urlencode(query))
        yield scrapy.Request(
            SEARCH_API + "?" + urlencode(query),
            meta={"page": page},
        )

    def parse(self, response):
        data = json.loads(response.body)
        if "list" in data.keys():
            meta = data["list"]["video_list"]

            for m in meta:
                print(m["play_url"])
                # yield ShortvideocrawlItem(
                #     id=m["vid"],
                #     file_urls=[m["play_url"]],
                # )

            # if data["has_more"] != 0:
            #     # not enough, theoretically 10 per page
            #     if (response.meta["page"] + 1) * 10 < self.count:
            #         yield self.search_request(response.meta["page"] + 1)
