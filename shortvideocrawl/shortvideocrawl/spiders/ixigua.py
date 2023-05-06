import base64
import json
import re
from urllib.parse import quote

import scrapy

SEARCH_API = "https://www.ixigua.com/api/searchv2/complex/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "referer": "https://www.ixigua.com/",
}
cookies = {
    "__ac_nonce": "06455b5c0004fea843108",
    "__ac_signature": "_02B4Z6wo00f0140WgWAAAIDAoFJteHoK3s-NNoXAAIcYJlMyCLmPVH4GcpCz6cjabluXCRCqO1bgvhFs8.obVCRg442JRnLl6pDYOAIndQz4Nwpxpzq4zxK5yXkXPNX4Y9CwYy2G0Q67FYIw14",
    "ixigua-a-s": "1",
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
    count = 10

    def start_requests(self):
        yield self.search_request(0)

    def search_request(self, page: int):
        offset = page * 10
        return scrapy.Request(
            SEARCH_API + quote(self.query) + "/" + str(offset),
            headers=headers,
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
            if (response.meta["page"] + 1) * 10 < self.count:
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

            id = meta["gid"]

            url = self.get_highest_quality(
                meta["packerData"]["video"]["videoResource"]["normal"]["video_list"]
            )

            print(
                id,
                url,
            )
            # print(url)
            # yield ShortvideocrawlItem(
            #     id=meta["id"],
            #     file_urls=[url],
            # )

    @staticmethod
    def get_highest_quality(data) -> str:
        url = ""
        max_width = 0
        for _, v in data.items():
            if v["vwidth"] > max_width:
                # url = v["main_url"]
                url = base64.b64decode(v["main_url"].encode("utf-8")).decode("utf-8")
                max_width = v["vwidth"]
        return url


# wget "https://v9-xg-web-pc.ixigua.com/4827e021895b23fb93751a149c53bd56/6455cb34/video/tos/cn/tos-cn-ve-4c001-alinc2/9c3d5a978ecb42cd8438199a91956d96/?a=1768&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C0%7C0&cv=1&br=2611&bt=2611&cs=0&ds=4&ft=6-IFAjjM9-px8Zq8ZmCTeK_ScoApU5aC6vrKffLLsto0g3&mime_type=video_mp4&qs=0&rc=Ozg5ZTdpaGk0OWk1NTtmaEBpMzxmZjs6ZmhtZTMzNDczM0BfX2M1Yy8zX18xYC1jXl4uYSNicm1ycjRnc2JgLS1kLWFzcw%3D%3D&l=2023050610332469F4E1F80BC2DBA1EA60&btag=e00028000" -O 1.mp4
# import math
# import os
# import sys
# import time
# import traceback
# import urllib
# from concurrent.futures import ThreadPoolExecutor
# from typing import Iterator

# import requests
# from celery import Celery
# from pymongo import MongoClient
# from tqdm import tqdm

# DATASOURCE = "ixigua"
# PRJ_NAME = os.getenv("PRJ_NAME", "")

# MONGO_URI = ""
# # MONGO_URI = "mongodb://root:1111@localhost:27017/admin"
# MONGO_DB = PRJ_NAME
# MONGO_COLLECTION = DATASOURCE

# # CELERY_BROKER = ""
# CELERY_BROKER = ""
# # CELERY_BROKER = "amqp://admin:admin@localhost:5672"


# class MongoCli:
#     def __init__(self, uri, db, collection):
#         self.cli = MongoClient(uri)
#         self.db = self.cli[db]
#         self.collection = self.db[collection]

#     def insert_item(self, item):
#         self.collection.insert_one(vars(item))


# mongo = MongoCli(MONGO_URI, MONGO_DB, MONGO_COLLECTION)

# celery = Celery(broker=CELERY_BROKER)


# class VideoItem:
#     def __init__(self, query, videoId, uploaderId, duration, title):
#         self.query = query
#         self.videoId = videoId
#         self.uploaderId = uploaderId
#         self.duration = float(duration)
#         self.title = title


# def send_save(item, d, pbar):
#     celery.send_task(
#         "celery_worker.download",
#         (
#             f"https://www.ixigua.com/{item.videoId}",
#             os.path.join(DATASOURCE, PRJ_NAME, "_".join([DATASOURCE, d])),
#         ),
#         queue=DATASOURCE,
#     )
#     mongo.insert_item(item)
#     pbar.update(1)

# SEARCH_API = "https://www.ixigua.com/api/searchv2/complex/{}/{}"
# PER_PAGE = 10   #西瓜视频搜索默认每页10个视频，不要改动！

# headers = {
#     # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
#     "referer": "https://www.ixigua.com/",
# }

# def Search(q: str, page: int, min_duration: int = 1, max_duration: int = -1) -> Iterator[VideoItem]:
#     params = {"min_duration":min_duration}
#     if max_duration != -1:
#         params["max_duration"] = max_duration
#     url = SEARCH_API.format(urllib.parse.quote(q),(page-1)*PER_PAGE) + "?" + urllib.parse.urlencode(params)
#     # print(url)
#     resp = requests.get(
#         url, headers=headers
#     )
#     if resp.status_code != 200:
#         raise Exception(f"Code {resp.status_code}!")
#     for data in resp.json()["data"]["data"]:
#         item = data["data"]
#         yield VideoItem(
#             query=q,
#             videoId=item["group_id"],
#             uploaderId=item["anchor_id"],
#             duration=item["video_time"],
#             title=item["title"],
#         )

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: main.py list-file")
#         exit(1)

#     f = sys.argv[1]
#     max_count = 50
#     min_duration = 1
#     max_duration = 180                      #满足 1 <= min_duration < max_duration 即可，均为正整数，单位second

#     with open(f) as fr:
#         lines = fr.read().splitlines()
#         for line in lines:
#             print(f"** search for {line}")
#             videos = []
#             pre_len = 0

#             for page in range(1, math.ceil(max_count / PER_PAGE) + 1):
#                 for _ in range(3):
#                     try:
#                         vs = Search(line, page, min_duration, max_duration)
#                         videos.extend(vs)
#                         break
#                     except Exception as e:
#                         traceback.print_exc()
#                         print("Error, retry in 60 seconds")
#                         time.sleep(60)
#                 if len(videos) == pre_len:
#                     print("no next page")
#                     break
#                 pre_len = len(videos)
#                 print("Added, wait 3 seconds")
#                 time.sleep(3)

#             with tqdm(total=len(videos)) as pbar:
#                 with ThreadPoolExecutor(max_workers=10) as ex:
#                     for v in videos:
#                         # time.sleep(1)
#                         ex.submit(
#                             send_save,
#                             v,
#                             os.path.splitext(os.path.basename(f))[0],
#                             pbar,
#                         )

#             print("Task a 5 minutes break")
#             time.sleep(60 * 5)

#     notify(f"[{DATASOURCE}] finish crawl {PRJ_NAME} {f}")
