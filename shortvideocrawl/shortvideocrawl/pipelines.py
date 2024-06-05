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
from scrapy.pipelines.files import FileException, FilesPipeline, logger
from scrapy.utils.request import referer_str


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
        if headers is not None:
            if cookies is not None:
                return [
                    Request(u, callback=NO_CALLBACK, headers=headers, cookies=cookies)
                    for u in urls
                ]
            else:
                return [Request(u, callback=NO_CALLBACK, headers=headers) for u in urls]
        return [Request(u, callback=NO_CALLBACK) for u in urls]

    def media_downloaded(self, response, request, info, *, item=None):
        referer = referer_str(request)

        if response.status not in [200, 206]:
            logger.warning(
                "File (code: %(status)s): Error downloading file from "
                "%(request)s referred in <%(referer)s>",
                {"status": response.status, "request": request, "referer": referer},
                extra={"spider": info.spider},
            )
            raise FileException("download-error")

        if not response.body:
            logger.warning(
                "File (empty-content): Empty file from %(request)s referred "
                "in <%(referer)s>: no-content",
                {"request": request, "referer": referer},
                extra={"spider": info.spider},
            )
            raise FileException("empty-content")

        status = "cached" if "cached" in response.flags else "downloaded"
        logger.debug(
            "File (%(status)s): Downloaded file from %(request)s referred in "
            "<%(referer)s>",
            {"status": status, "request": request, "referer": referer},
            extra={"spider": info.spider},
        )
        self.inc_stats(info.spider, status)

        try:
            path = self.file_path(request, response=response, info=info, item=item)
            checksum = self.file_downloaded(response, request, info, item=item)
        except FileException as exc:
            logger.warning(
                "File (error): Error processing file from %(request)s "
                "referred in <%(referer)s>: %(errormsg)s",
                {"request": request, "referer": referer, "errormsg": str(exc)},
                extra={"spider": info.spider},
                exc_info=True,
            )
            raise
        except Exception as exc:
            logger.error(
                "File (unknown-error): Error processing file from %(request)s "
                "referred in <%(referer)s>",
                {"request": request, "referer": referer},
                exc_info=True,
                extra={"spider": info.spider},
            )
            raise FileException(str(exc))

        return {
            "url": request.url,
            "path": path,
            "checksum": checksum,
            "status": status,
        }
