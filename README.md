bd
===

爬取百度图库上的名人图片

### Install

Windows 下最好先安装一个Python(2.7)的科学计算发行版

`$ pip install -r requirements.txt`

### Settings

复制 `bd/settings_example.py` 到 `bd/settings.py`

在 `bd/settings.py` 的 `IMAGES_STORE` 中设置下载目录, 在 `bd/settings.py` 的 `PeopleNames` 中设置名人txt文件路径,在 `bd/settings.py` 的 `Pages` 中选择爬取的页数

### Crawl

`$ scrapy crawl Baidu`

### Stopping

`Ctrl+C` 来停止爬取，可能要等一会才会停止