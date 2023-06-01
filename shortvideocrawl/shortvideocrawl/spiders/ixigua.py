import base64
import json
import re
from urllib.parse import quote, urlencode

import scrapy

from ..items import ShortvideocrawlItem

SEARCH_API = "https://www.ixigua.com/api/searchv2/complex/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "referer": "https://www.ixigua.com/",
}
cookies = {
    "__ac_nonce": "06455b5c0004fea843108",
    "__ac_signature": "_02B4Z6wo00f0140WgWAAAIDAoFJteHoK3s-NNoXAAIcYJlMyCLmPVH4GcpCz6cjabluXCRCqO1bgvhFs8.obVCRg442JRnLl6pDYOAIndQz4Nwpxpzq4zxK5yXkXPNX4Y9CwYy2G0Q67FYIw14",
    "ixigua-a-s": 1,
    "support_webp": "true",
    "support_avif": "true",
    "csrf_session_id": "61b3e21eff2632c4cf9b3721f078ce19",
    "ttwid": "1%7CHBC3sXZ7O4N7hI-FudupBhdzSq7Tcv9kx4rSRlpFpdU%7C1683338709%7Ce37acd71825e60f975e65b66066e7a44b6e73b966c21d3744efd40d2479da98e",
    "msToken": "1cMf4SpS6j4fo1zzyLHk2M7qLOP4Fz6_UE92slF4exP8M3XLG379wJ6-cyEQbMlWFqU28YfIiCLnPwuGbzgp_2_ceO67UgozSIuHsEjFj22SFdimwhjFbtXxfZEx2g==",
    "tt_scid": "XJMrkuXM1Htc6nyCivY.cy8EIeul6-AEycBfnq.6NmgfjKZcm9MnTEDpSI2EY0cQ0b93",
}


class IxiguaSpider(scrapy.Spider):
    name = "ixigua"
    allowed_domains = ["www.ixigua.com"]

    query = "蔡徐坤"
    count = 20

    def start_requests(self):
        yield self.search_request(0)

    def search_request(self, page: int):
        offset = page * 10
        params = {
            "min_duration": 1,
            "max_duration": 300,
        }
        return scrapy.Request(
            SEARCH_API
            + quote(self.query)
            + "/"
            + str(offset)
            + "?"
            + urlencode(params),
            headers=headers,
            cookies=cookies,
            meta={"page": page},
            callback=self.parse_search,
        )

    def detail_request(self, vid):
        return scrapy.Request(
            f"https://www.ixigua.com/{vid}",
            cookies=cookies,
            callback=self.parse_detail,
        )

    def parse_search(self, response):
        resp = json.loads(response.body)
        data = resp["data"]
        # print(data)
        for d in data["data"]:
            # print(d["data"]["group_id"])
            yield self.detail_request(d["data"]["group_id"])

        if data["has_more"] != False:
            # not enough, theoretically 10 per page
            if (response.meta["page"] + 1) * 10 < int(self.count):
                yield self.search_request(response.meta["page"] + 1)

    def parse_detail(self, response):
        # print(response.text)
        pattern = re.compile(
            r"<script id=\"SSR_HYDRATED_DATA\" nonce=.*?>window._SSR_HYDRATED_DATA=(.*?)<\/script>"
        )
        vals = pattern.findall(response.text)
        # print(vals[0])
        if len(vals) > 0:
            data = json.loads(vals[0].replace('":undefined', '":null'))
            meta = data["anyVideo"]["gidInformation"]
            url = self.get_highest_quality(
                meta["packerData"]["video"]["videoResource"]["normal"]["video_list"]
            )
            if url != "":
                yield ShortvideocrawlItem(
                    id=meta["gid"],
                    file_urls=[url],
                    _cookies=cookies,
                    _headers=headers,
                )

    @staticmethod
    def get_highest_quality(data) -> str:
        url = ""
        max_width = 0
        for _, v in data.items():
            if (
                v["vwidth"] > max_width and v["size"] < 16 * 1024 * 1024
            ):  # file size smaller than 16MB
                # url = v["main_url"]
                url = base64.b64decode(v["main_url"].encode("utf-8")).decode("utf-8")
                max_width = v["vwidth"]
        return url
