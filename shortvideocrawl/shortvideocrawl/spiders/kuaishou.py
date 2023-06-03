import json

import scrapy

from ..items import ShortvideocrawlItem

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "content-type": "application/json",
}

cookies = {
    "kpf": "PC_WEB",
    "kpn": "KUAISHOU_VISION",
    "clientid": 3,
    # "client_key": "65890b29",
    # "didv": "1673605994679",
    "did": "web_e09a1040aa48f4986189eb05785f0d70",
}

# kpf=PC_WEB; clientid=3; did=web_e09a1040aa48f4986189eb05785f0d70; kpn=KUAISHOU_VISION

SEARCH_API = "https://www.kuaishou.com/graphql"


class KuaishouSpider(scrapy.Spider):
    name = "kuaishou"
    allowed_domains = ["www.kuaishou.com"]

    query = "蔡徐坤"
    count = 40

    def start_requests(self):
        yield self.request(0)

    def request(self, page: int):
        body = {
            "operationName": "visionSearchPhoto",
            "variables": {
                "keyword": self.query,
                "pcursor": str(page),
                "page": "search",
                "searchSessionId": "MTRfMF8xNjc1MDY3MDgzNzM2X-iUoeW-kOWdpF8yMDI2",
            },
            "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n",
        }
        return scrapy.Request(
            SEARCH_API,
            method="POST",
            cookies=cookies,
            headers=headers,
            body=json.dumps(body),
        )

    def parse(self, response):
        resp = json.loads(response.body)
        # print(resp)
        data = resp["data"]["visionSearchPhoto"]
        for feed in data["feeds"]:
            yield ShortvideocrawlItem(
                id=feed["photo"]["id"],
                file_urls=[feed["photo"]["photoUrl"]],
            )

        # next
        # print(data)
        if data["pcursor"] != "no_more" and data["pcursor"] is not None:
            next_page = int(data["pcursor"])
            # not enough, theoretically 20 per page
            if next_page * 20 < int(self.count):
                yield self.request(next_page)
