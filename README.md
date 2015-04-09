bd
===

爬取百度图库上的名人图片

### Install

Windows 下最好先安装一个Python的科学计算发行版

`$ pip install -r requirements.txt`

### Settings

在 `bd/settings.py` 的 `IMAGES_STORE` 中设置下载目录, 在 `bd/settings.py` 的 `PeopleNames` 中添加名人的名字

### Crawl

`$ scrapy crawl Baidu`

### Stopping

`Ctrl+C` 来停止爬取，可能要等一会才会停止