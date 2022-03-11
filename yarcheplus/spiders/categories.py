import re
import scrapy
import logging
from yarcheplus.items import Link
import json
import datetime
import time

from scrapy.loader import ItemLoader
from yarcheplus.items import Product

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


logger = logging.getLogger('yarchepluslogs')

with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fs:
    data = json.load(fs)


class yarcherCrawler(scrapy.Spider):

    name = 'yaCrawler'
    start_urls = ['https://yarcheplus.ru/category']

    def parse(self, response, **kwargs):
        print('begin')
        category_list = response.xpath('//a[contains(@href,"category")]')

        for i in category_list:
            dict_attrib = i.attrib
            if 'style' in dict_attrib:
                pass
            else:
                href = 'https://yarcheplus.ru' + dict_attrib['href']
                print(href)
                yield response.follow(href, cb_kwargs=dict(url=href), callback=self.parse_catalog)

    def parse_catalog(self, response, url):
        print('begin 2')
        catalog_list = response.xpath('//a[contains(@href,"catalog")]')
        name_1 = response.xpath('//span[@itemprop = "name"]/text()').getall()[2]
        print('ccылка категории', name_1)
        for j, i in enumerate(catalog_list):
            dict_attrib = i.attrib
            print('отсчёт цикла :', j)
            print('переменная категории : ', i)
            print('атрибутика переменной категории : ', dict_attrib)
            if 'style' in dict_attrib:
                pass
            else:
                href1 = 'https://yarcheplus.ru' + dict_attrib['href']
                print('ccылка каталога', href1)
                name_2 = i.css('img').attrib['title']
                print('список каталогов : ')
                # for k in name_2:
                #     print('   ', k)
                print(name_2)
                yield {
                    'url_parent': url,
                    'url': href1,
                    'name': name_1 + ' ' + '|' + ' ' + name_2
                }








