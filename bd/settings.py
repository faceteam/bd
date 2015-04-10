# -*- coding: utf-8 -*-

# Scrapy settings for bd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bd'

SPIDER_MODULES = ['bd.spiders']
NEWSPIDER_MODULE = 'bd.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bd (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'bd.pipelines.ImagePipeline': 300,
}

IMAGES_STORE = 'E:/baidu'

PeopleNames = 'E:/GIT/bd/a.txt'
Pages = 5