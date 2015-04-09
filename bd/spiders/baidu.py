import os
import json
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
        'Host': 'h.hiphotos.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
    }

    #url_pattern = "http://image.baidu.com/i?tn=resultjsonavatarnew&ie=utf-8&word={0}&cg=star&pn={0}&rn={1}"
    url_pattern = "http://image.baidu.com/data/star/listjson?pn={0}&rn={1}&name={2}"

    def start_requests(self):
        for name in PeopleNames:
            for page in range(1, Pages+1):
                url = self.url_pattern.format(page, 100, name)
                yield Request(url, headers=self.headers)

    def parse(self, response):
        data = json.loads(response.body)
        data = data['data']
        for one in data:
            if one == {}:
                continue
            url = one['image_url']
            media_guid = hashlib.sha1(url).hexdigest()  # change to request.url after deprecation
            media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
            fp = os.path.join(IMAGES_STORE, 'full/%s%s' % (media_guid, media_ext))
            if os.path.exists(fp):
                continue
            item = ImageItem()
            item['name'] = one['tag']
            item['url'] = one['image_url']
            yield item