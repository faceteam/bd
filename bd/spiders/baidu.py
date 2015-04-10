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

class BaiduSpider(scrapy.Spider):
    """
        baidu pictures for face project
    """
    name = 'Baidu'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'image.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
    }
    url_pattern = "http://image.baidu.com/i?tn=resultjsonavatarnew&ie=utf-8&word={2}&cg=star&pn={0}&rn={1}&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1"

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
        data = re.findall(r'\"objURL\":\"(http://.*?)\"', body)
        name = re.search(r'word=(.*?)&', response.url).groups()[0]
        name = urllib.unquote(name).decode('utf8') # unicode
        #name = urllib.unquote(name)
        for one in data:
            url = one
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
