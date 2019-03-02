# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import codecs
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem


class GamedownloadPipeline(object):

    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = codecs.open('changgame.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonLinesWriterPipeline(object):

    def __init__(self):
        self.fp = open('changgame.json', 'wb')
        self.exporter = JsonLinesItemExporter(
            self.fp, ensure_ascii=False, encoding='utf-8')
        self.fp.write(b'{\"game\": [')

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.fp.write(b',')
        return item

    def close_spider(self, spider):
        # remove the last comma
        self.fp.seek(-2, os.SEEK_END)
        self.fp.truncate()
        self.fp.write(b']}')
        self.fp.close()


class GameLogoDownloadPipeLine(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['logoUrl'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
