import json
from urllib.parse import urlencode

import scrapy

from ..items import ShortvideocrawlItem

GET_SEARCH_ID_API = "https://www.xinpianchang.com/api/xpc/v2/search/getSearchKwIdByKw"
SEARCH_API = "https://www.xinpianchang.com/_next/data/%s/search.json"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}
VIDEO_INFO_API = (
    "https://mod-api.xinpianchang.com/mod/api/v2/media/%s?appKey=61a2f329348b3bf77"
)


class XinpianchangSpider(scrapy.Spider):
    name = "xinpianchang"
    allowed_domains = ["www.xinpianchang.com", "mod-api.xinpianchang.com"]

    query = "蔡徐坤"
    count = 20

    def start_requests(self):
        yield scrapy.Request(
            GET_SEARCH_ID_API + "?" + urlencode({"kw": self.query}),
            callback=self.parse_search_id,
            headers=headers,
        )

    def search_request(self, search_id, build_id):
        params = {
            "from": "inputSearch",
            "kw_id": search_id,
        }
        return scrapy.Request(
            SEARCH_API % build_id + "?" + urlencode(params),
            headers=headers,
            callback=self.parse_search,
        )

    def parse_search_id(self, response):
        resp = json.loads(response.body)
        search_id = resp["data"]["id"]
        yield scrapy.Request(
            "https://www.xinpianchang.com/",
            headers=headers,
            callback=self.parse_build_info,
            meta={"search_id": search_id},
        )

    def parse_build_info(self, response):
        data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        build_id = json.loads(data)["buildId"]
        yield self.search_request(response.meta["search_id"], build_id)

    def parse_search(self, response):
        resp = json.loads(response.body)
        search_data = resp["pageProps"]["searchData"]
        if "list" in search_data.keys():
            for d in search_data["list"]:
                # print(d["web_url"])
                yield scrapy.Request(
                    d["web_url"].split("?")[0],
                    headers=headers,
                    callback=self.parse_detail,
                )

    def parse_detail(self, response):
        # print(response.body)
        data = response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        vid = json.loads(data)["props"]["pageProps"]["detail"]["vid"]
        yield scrapy.Request(
            VIDEO_INFO_API % vid,
            headers=headers,
            callback=self.parse_video_info,
        )

    def parse_video_info(self, response):
        resp = json.loads(response.body)
        video_url = resp["data"]["resource"]["progressive"][0]["url"]
        video_id = resp["data"]["mid"]
        yield ShortvideocrawlItem(
            id=video_id,
            file_urls=[video_url],
        )
