# encoding: utf-8

import scrapy

class Demo(scrapy.Spider):
    name = 'challenge15'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repo in response.xpath('//div[@class="application-main "]').xpath('.//div[@id="user-repositories-list"]/ul/li'):
            yield {
                    'name': repo.xpath('.//h3/a/text()').re_first("\s+(\S+)"),
                    'update_time': repo.xpath('.//relative-time/@datetime').extract_first()
                    }

