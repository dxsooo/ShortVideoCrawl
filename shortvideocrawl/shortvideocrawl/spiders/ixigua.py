import scrapy


class IxiguaSpider(scrapy.Spider):
    name = "ixigua"
    allowed_domains = ["www.ixigua.com"]
    start_urls = ["http://www.ixigua.com/"]

    def parse(self, response):
        pass


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
