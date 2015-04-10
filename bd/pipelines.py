# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os
import shutil
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline, DropItem
from bd.settings import IMAGES_STORE


class ImagePipeline(ImagesPipeline):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': '',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        _headers =  self.headers
        _headers['Host'] = re.search(r'http://(.*?)/', item['url']).groups()[0]
        _headers['Referer'] = item['origin_url']
        return scrapy.Request(item['url'], headers=_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths or len(image_paths) != 1:
            raise DropItem("Item contains no images")
        path = image_paths[0]
        file_name = os.path.split(path)[-1]
        dir_name = item['name']
        dir_path = os.path.join(IMAGES_STORE, dir_name)
        # 目录不存在
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        src = os.path.join(IMAGES_STORE, path)
        dst = os.path.join(IMAGES_STORE, os.path.join(dir_name, file_name))
        shutil.copyfile(src, dst)
        return item

