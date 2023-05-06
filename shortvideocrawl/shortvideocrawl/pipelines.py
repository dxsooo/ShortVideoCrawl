# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mimetypes
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK
from scrapy.pipelines.files import FilesPipeline


class ShortvideocrawlPipeline:
    def process_item(self, item, spider):
        return item


class VideosPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        media_guid = ItemAdapter(item).get("id")
        media_ext = os.path.splitext(request.url)[1]
        if media_ext not in mimetypes.types_map:
            # default mp4
            media_ext = ".mp4"
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return f"{media_guid}{media_ext}"

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        cookies = ItemAdapter(item).get("_cookies")
        headers = ItemAdapter(item).get("_headers")
        if headers is not None and cookies is not None:
            return [
                Request(u, callback=NO_CALLBACK, headers=headers, cookies=cookies)
                for u in urls
            ]
        return [Request(u, callback=NO_CALLBACK) for u in urls]
