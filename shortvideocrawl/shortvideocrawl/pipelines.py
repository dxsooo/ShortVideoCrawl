# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import mimetypes
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
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
