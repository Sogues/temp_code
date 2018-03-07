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
            item =  GithubItem()
            item['name'] = repo.xpath('.//h3/a/text()').re_first('\s+(\S+)')
            item['update_time'] = repo.xpath('.//relative-time/@datetime').extract_first()
            new_url = response.urljoin(repo.xpath('.//h3/a/@href').extract_first())
            request = scrapy.Request(new_url, callback=self.parse_repo)
            request.meta['item'] = item
            yield request

    def parse_repo(self, response):
        item = response.meta['item']
        li = response.xpath('//ul[@class="numbers-summary"]/li')
        item['commits'] = li[0].xpath('.//span/text()').re_first('\s+(\S+)\s+')
        item['branches'] = li[1].xpath('.//span/text()').re_first('\s+(\S+)\s+')
        item['releases'] = li[2].xpath('.//span/text()').re_first('\s+(\S+)\s+')
        yield item
