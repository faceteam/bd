# -*- coding: utf-8 -*-
import re
import os
import json
import urllib
import hashlib
import scrapy
from scrapy.http import Request
from bd.items import ImageItem
from bd.settings import PeopleNames, IMAGES_STORE
from bd.settings import Pages

class Spider(scrapy.Spider):
    """
        360 pictures for face project
    """
    name = 'Haosou'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
    }
    url_pattern = "http://image.haosou.com/j?q={2}&src=srp&sn={1}&pn={0}"

    def start_requests(self):
        base = 60
        with open(PeopleNames, 'r') as fd:
            files = fd.read()
            files = files.split("\n")
            for name in files:
                name = name.strip()
                for page in range(0, Pages):
                    url = self.url_pattern.format(page*base, base, name)
                    yield Request(url, headers=self.headers)

    def parse(self, response):
        body = response.body
        data = re.findall(r'\"img\":\"(http:.*?)\"', body)
        name = re.search(r'\?q=(.*?)&', response.url).groups()[0]
        name = urllib.unquote(name).decode('utf8') # unicode
        #name = urllib.unquote(name)
        for one in data:
            url = one.replace('\\', '') # 360 got http:\/\/.....
            media_guid = hashlib.sha1(url).hexdigest()  # change to request.url after deprecation
            media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
            fp = os.path.join(IMAGES_STORE, 'full/%s%s' % (media_guid, media_ext))
            if os.path.exists(fp): # check if exists
                continue
            item = ImageItem()
            item['name'] = name
            item['origin_url'] = response.url
            item['url'] = url
            yield item
