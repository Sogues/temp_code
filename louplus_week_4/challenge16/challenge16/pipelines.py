# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from challenge16.items import GithubItem
from sqlalchemy.orm import sessionmaker
from challenge16.models import engine, Repository
from datetime import datetime

class Challenge16Pipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, GithubItem):
            self._process_github_item(item)
        return item

    def _process_github_item(self, item):
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        if 'update_time' not in item.keys() or not item['update_time']:
            item['update_time'] = datetime.strptime(datetime.now(), date_format)
        else:
            item['update_time'] = datetime.strptime(item['update_time'], date_format)
        item['commits'] = int(''.join(item['commits'].split(',')))
        item['branches'] = int(''.join(item['branches'].split(',')))
        item['releases'] = int(''.join(item['releases'].split(',')))
        self.session.add(Repository(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
