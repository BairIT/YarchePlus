
import re
import scrapy
import logging
from yarcheplus.items import Product
import json
import datetime
from scrapy import Request


logger = logging.getLogger('yarchepluslogs')
with open('/home/hooch/PycharmProjects/YarchePlus/yarcheplus/config.json', 'r') as fs:
    data = json.load(fs)


class YarchePlusSpider(scrapy.Spider):

    name = 'yarch'
    start_urls = ['https://yarcheplus.ru/']

    def parse(self, response, **kwargs):
        hrefs = response.css('a::attr(href)').getall()
        hrefss = []
        for i in hrefs:
            if re.search('/category/', i):
                i = 'https://yarcheplus.ru' + i
                hrefss.append(i)
                print(i)
            else:
                continue
        yield from response.follow_all(hrefss, callback=self.parse)

        pagination_links = response.css('a::attr(href)').getall()
        hrefscat = []
        for i in pagination_links:
            if re.search('/catalog/', i):
                i = 'https://yarcheplus.ru' + i
                hrefscat.append(i)
                print(i)
            else:
                continue
        yield from response.follow_all(hrefscat, callback=self.parse)

        pagination_links2 = response.css('a::attr(href)').getall()
        hrefscat2 = []
        for i in pagination_links2:
            if re.search('/product/', i):
                i = 'https://yarcheplus.ru' + i
                hrefscat2.append(i)
                print(i)
            else:
                continue
        yield from response.follow_all(hrefscat2, callback=self.parse_product)

    def parse_product(self, response, **kwargs):

        item = Product()
        item['parser_id']: data["parser_id"]
        print(data['parser_id'])
        item['chain_id']: data["chain_id"]
        item['tt_id']: data["tt_id"]
        item['tt_region']: data["tt_region"]
        item['tt_name']: data["tt_name"]
        item['price_datetime']: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        k = response.xpath('//div[@class = "product-cart__price"]').get()

        item['price']: response.xpath('//div[@class = "product-cart__price"]').get()
        input('STOP_1 в пауке')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!посмотри : ', k)
        input('STOP_2 в пауке')
        item['sku_name']: response.css('h1::text').get()

        # def extract_with_css(query):
            # return response.css(query).get().strip()

        yield item


             # 'parser_id,
            # 'chain_id' :chain_id,                 #Значение берется из конфига.
            # 'tt_id': tt_id,                       #id торговой точки.Значение берется из конфига.
            # 'tt_region': tt_region,               # Регион торговой точки.
            # 'tt_name': tt_name,                   #Название сети (chain_name) с указанием адреса в скобках. Пример:
            #                                       #“Globus (Московская обл., Новорижское ш., 22-й км, вл. 1, стр. 1)”.
            # 'price_datetime':
            #
            # 'Наименование продукта': response.css('h1::text').get(),
            # ''
            # # 'description_table': extract_with_css('div class="product-props__sub-section"'),
            # 'description_table_values': extract_with_css('.items::text'),
            # 'Наименование продукции': extract_with_css('td.n::text'),
            # 'Объём': extract_with_css('td.v::text'),
            # 'В наличии': extract_with_css('td.a span::text')
