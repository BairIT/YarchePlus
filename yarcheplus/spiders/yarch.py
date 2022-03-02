
import re
import scrapy
import logging
# from yarcheplus.items import Product
import json
import datetime


from scrapy.loader import ItemLoader
from yarcheplus.items import Product


from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger('yarchepluslogs')
with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fs:
    data = json.load(fs)

#
# class YarchePlusSpider(scrapy.Spider):
#
#     name = 'yarch'
#     start_urls = ['https://yarcheplus.ru/category']
#
#     def parse_1(self, response, **kwargs):
#         hrefs = response.css('a::attr(href)').getall()
#         hrefss = []
#         for i in hrefs:
#             if re.search('/category/', i):
#                 i = 'https://yarcheplus.ru' + i
#                 hrefss.append(i)
#                 print(i)
#             else:
#                 continue
#             yield from response.follow(i, callback=self.parse_1)
#
#         pagination_links = response.css('a::attr(href)').getall()
#
#         hrefscat = []
#         for i in pagination_links:
#             if re.search('/catalog/', i):
#                 i = 'https://yarcheplus.ru' + i
#                 hrefscat.append(i)
#                 print(i)
#             else:
#                 continue
#             yield from response.follow_all(i, callback=self.parse_product_1)
#
#         input('проверка вторая просмотри меня')
#
#         pagination_links2 = response.css('a::attr(href)').getall()
#         hrefscat2 = []
#         for i in pagination_links2:
#             if re.search('/product/', i):
#                 i = 'https://yarcheplus.ru' + i
#                 hrefscat2.append(i)
#                 print(i)
#             else:
#                 continue
#             yield from response.follow_all(i, callback=self.parse)
#
#         input('проверка третья посмотри меня')
#
#     def parse_product_1(self, response, **kwargs):
#         loader = ItemLoader(item=Product(), response=response)
#         print(response.follow_all)
#
#         # item['parser_id']: data["parser_id"]
#         # print(data['parser_id'])
#         # item['chain_id']: data["chain_id"]
#         # item['tt_id']: data["tt_id"]
#         # item['tt_region']: data["tt_region"]
#         # item['tt_name']: data["tt_name"]
#         loader.load_item['price_datetime']: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         input('STOP в пауке')
#         loader.add_xpath('price', '//div[@class = "product-cart__price"]')
#         input('поиск элемента')
#         loader.add_value('sku_name', 'h1::text')
#         yield loader.load_item()
#         print('endering загрузка поля')
#

            # 'Наименование продукта': response.css('h1::text').get(),

