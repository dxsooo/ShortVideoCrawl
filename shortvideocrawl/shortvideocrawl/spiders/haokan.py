import json

import scrapy
from urllib.parse import urlencode
from ..items import ShortvideocrawlItem

SEARCH_API = "https://haokan.baidu.com/haokan/ui-search/pc/search/video"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "cors",
    "Cache-Control": "no-cache",
    "Host": "haokan.baidu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4.1 Safari/605.1.15",
    "Referer": "https://haokan.baidu.com/web/search/page?query=%E8%94%A1%E5%BE%90%E5%9D%A4",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
}

cookies = {
    "RT": '"z=1&dm=baidu.com&si=b1e3eebf-bc17-4ba8-80c4-981450a88da7&ss=lgupdtuj&sl=3&tt=1pb&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1rak&ul=cind&hd=cipz"',
    "ariaDefaultTheme": "undefined",
    "Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5": "1682332626",
    "Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5": "1682332585",
    "hkpcSearch": "%u8521%u5F90%u5764",
    "ab_sr": "1.0.1_NGJmMjMyNzg2YWZjMDQ2YzhmZGM4MGI3YjMxZDgzNWIyNzU1NTFjNWY3NTM4MDkzNTdiNDkyZWQ2MzJmNDJmYzFiM2M0NDQ1MGExNmZjZTMyZTg5MmE3MGJkNDVjZDc5NGQ4ZjBmNzMxYTIxMzlkZTVkOGJmZWQ2YjJmNDIyNzc3OWNjNjQ0ODIzM2M0NWNmMjBjODMzOTE0OGMyZDI5Mg==",
    "reptileData": "%7B%22data%22%3A%2207365175041eb5a237beae3fe59b0a8611b6c16a31f5fbb2caa721fa9bc1f08467a1330751f52ccd88684810a3e551c34507d070bdd750eeea2ffc0c70d4d9a718f2fcd92e58052565c79aa7ef94a71a29bce541848099f2c48d26e361d97e12%22%2C%22key_id%22%3A%2230%22%2C%22sign%22%3A%22253b5d4c%22%7D",
    "ZFY": "OH1XubtMO4gg4WiLnLXhu2DDldqY6bdQGEFwTst4XLw:C",
    "BAIDUID": "47480F23FB5D94E35D7D21F63797455F:FG=1",
    "BIDUPSID": "AE72DD69FA755190B5172FD5C667F888",
    "PSTM": "1638979955",
}


class HaokanSpider(scrapy.Spider):
    name = "haokan"
    allowed_domains = ["haokan.baidu.com"]

    query = "蔡徐坤"
    count = 30

    def start_requests(self):
        yield self.request(1)

    def request(self, page: int):
        query = {
            "pn": page,
            "rn": 10,
            "type": "video",
            "query": self.query,
            "sign": "9cb60910441a1e1afde1e4d73de14a45",
            "version": 1,
            "timestamp": 1682333168570,
        }
        return scrapy.Request(
            SEARCH_API + "?" + urlencode(query),
            meta={"page": 1},
            headers=headers,
            cookies=cookies,
        )

    def parse(self, response):
        resp = json.loads(response.body)
        data = resp["data"]

        if "list" in data:
            for l in data["list"]:
                print(l["vid"])

            if data["has_more"] != 0:
                # not enough, theoretically 10 per page
                if response.meta["page"] * 10 < self.count:
                    yield self.request(response.meta["page"] + 1)
        else:
            print(data)
