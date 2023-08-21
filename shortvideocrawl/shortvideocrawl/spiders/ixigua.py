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
    "__ac_signature": "_02B4Z6wo00f01Sj4t4gAAIDCBbxbkkVvcDEo2LMAAC5seeqMJOpxBgStyAHJmJnxEMVp8eHfV7hPj7whlIXMDNuERx70NeEFGGAxa7w6i1d875gavAns6E0ND8KsFRJzp298-Lydlw5d4.luf5",
    "ixigua-a-s": 0,
    "support_webp": "true",
    "support_avif": "true",
    "csrf_session_id": "8d66a2705f917f03938dfad1147727d0",
    "ttwid": "1%7CoO6dQdpyel3tVei7nLGeOfGtx6rU-TKXkZkZUpySPzA%7C1692578092%7C7a9fe16f8415cbd571aacc4df6595bc6f82d85c630bd47be662e629199d3cbe5",
    "msToken": "fvt2MXYD38y2e_i7ZNueTNAmm9s0fH_T_089bycvTdLb0ok80COLdhWMIuUIB8iy_jzsVFtoS3uzHWOmJOZ7-1pi0-KdMgI2w8c_wxbkEAVWniN3vSA7t5vCAakbzUg=",
    "tt_scid": "8gdVyLvMGuLLyavEjrTahtoVjTyaotowNPHonF8ZABuZhs9fg-1Jwb-RhDuMbtLKcec2",
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
        # print(json.dumps(data))
        for d in data["data"]:
            # print(d["data"]["group_id"])
            if "group_id" in d["data"].keys():
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
