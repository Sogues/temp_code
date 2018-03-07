# -*- coding: utf-8 -*-
import scrapy
from challenge16.items import GithubItem


class GithubSpider(scrapy.Spider):
    name = 'github'

    @property
    def start_urls(self):
        return ("https://github.com/shiyanlou?page={}&tab=repositories".format(i) for i in range(1, 5))

    def parse(self, response):
        for repo in response.xpath('//ul[@data-filterable-for="your-repos-filter"]/li'):
            yield GithubItem({
                'name': repo.xpath('.//h3/a/text()').re_first('\s+(\S+)'),
                'update_time': repo.xpath('.//relative-time/@datetime').extract_first()
                })
