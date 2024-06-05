import json
from urllib.parse import urlencode

import scrapy

from ..items import ShortvideocrawlItem

SEARCH_API = "https://quanmin.baidu.com/wise/growth/api/home/searchmorelist"


class QuanminSpider(scrapy.Spider):
    name = "quanmin"
    allowed_domains = ["quanmin.baidu.com", "bdstatic.com"]

    query = "蔡徐坤"
    count = 20

    def start_requests(self):
        yield self.request(0)

    def request(self, page: int):
        query = {
            "rn": 12,
            "pn": page,
            "q": self.query,
            "type": "search",
            "_format": "json",
        }

        return scrapy.Request(
            SEARCH_API + "?" + urlencode(query),
            meta={"page": page},
        )

    def parse(self, response):
        resp = json.loads(response.body)
        data = resp["data"]
        if "list" in data.keys():
            meta = data["list"]["video_list"]

            for m in meta:
                # print(m["play_url"])
                yield ShortvideocrawlItem(
                    id=m["vid"],
                    file_urls=[m["play_url"]],
                )

            if data["list"]["has_more"] != 0:
                # not enough, theoretically 10 per page
                if (response.meta["page"] + 1) * 10 < int(self.count):
                    yield self.request(response.meta["page"] + 1)
