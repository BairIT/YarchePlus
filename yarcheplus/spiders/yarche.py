import html.parser
import re
import time

import requests
import json
import scrapy
import logging
import json
import requests_html
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions


logger = logging.getLogger('yarchepluslogs')

with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fs:
    data = json.load(fs)


class yarcherCrawler(scrapy.Spider):

    name = 'yarcherCrawler'
    start_urls = ['https://yarcheplus.ru/category']
    # with open('cookies', 'r') as file:
    #     file_coo = json.load(file)

    def start_requests(self):
        headers = data['headers']
        print(headers)
        for url in self.start_urls:
            yield scrapy.Request(url, cookies='cookies', callback=self.parse)

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
                yield response.follow(href, callback=self.parse_catalog)

    def parse_catalog(self, response):
        print('begin 2')
        catalog_list = response.xpath('//a[contains(@href,"catalog")]')
        for j, i in enumerate(catalog_list):
            dict_attrib = i.attrib
            if 'style' in dict_attrib:
                pass
            else:
                href1 = 'https://yarcheplus.ru' + dict_attrib['href']
                print(href1)
                yield response.follow(href1, callback=self.parse_product)

    def parse_product(self, response):
        print('parse_product')
        root = response.text
        xtml = BeautifulSoup(root, 'lxml')
        a = xtml.find_all('a', draggable='true')
        b = xtml.find_all()
        pass
        # for i in a:
        #     pict = i.findChildren('picture')
        #     if pict:
        #         print('pict')
        #         if pict[0].parent.parent.parent['class'] == 'deff':
















