
from os.path import isfile
import scrapy
import logging
import json
from bs4 import BeautifulSoup
from yarcheplus.middlewares import jsfilconfig
from yarcheplus.items import Product
import datetime
import http.client

import yarcheplus.middlewares
from yarcheplus.middlewares import address_input

logger = logging.getLogger('yarchepluslogs')

# with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fs:
#     data = json.load(fs)


class yarcherCrawler(scrapy.Spider):
    print('поехали')
    name = 'yarcherCrawler'
    # allowed_domains = ['yarcheplus.ru']
    start_urls = ['https://yarcheplus.ru/category']

    file_cook = yarcheplus.middlewares.get_cookies_yarche()

    def start_requests(self):
        headers = jsfilconfig['headers']
        # print('заголовки из конфы : ', headers)
        print('старт реквестов')
        # print('файлы куки : ' + '\n', self.file_cook)
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        print('парсинг категории')
        category_list = response.xpath('//a[contains(@href,"category")]')
        for i in category_list:
            dict_attrib = i.attrib
            if 'style' in dict_attrib:
                pass
            else:
                # href = dict_attrib['href']
                href = 'https://yarcheplus.ru' + dict_attrib['href']
                print('ccылка на дальнейший парсинг с каталога : ', href)
                yield scrapy.Request(href, callback=self.parse_catalog)

    def parse_catalog(self, response):
        print('парсинг каталога')
        catalog_list = response.xpath('//a[contains(@href,"catalog")]')
        name_1 = response.xpath('//span[@itemprop = "name"]/text()').getall()[2]
        for i in catalog_list:
            dict_attrib = i.attrib
            if 'style' in dict_attrib:
                href1 = 'https://yarcheplus.ru' + dict_attrib['href']
                print('ссылка на дальнейший парсинг с продукта : ', href1)
                yield scrapy.Request(href1, cb_kwargs=dict(name_1=name_1), callback=self.parse_product_lite)
            else:
                pass

    def parse_product_lite(self, response, name_1):
        item = Product()
        print('парсинг продукта_лайт')

        root = response.text
        xtml = BeautifulSoup(root, 'lxml')

        butt = xtml.find_all('button')
        print(butt[1].text)

        a = xtml.find_all('a', draggable='true')
        a = a[::2]

        name_2 = response.xpath('//span[@itemprop = "name"]/text()').getall()[-1]
        print('name_2 : ', name_2)
        for i in a:
            price = i.parent.parent.contents[3].contents[1].contents[0].contents[0].contents[0].text
            href2 = 'https://yarcheplus.ru' + i.get('href')
            item['parser_id'] = jsfilconfig['parser_id']
            item['chain_id'] = jsfilconfig['chain_id']
            item['tt_id'] = jsfilconfig['tt_id']
            item['tt_region'] = jsfilconfig['tt_id'].split(sep=', ')[1]
            item['tt_name'] = jsfilconfig['tt_name']
            item['price_datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # item['price_card'] = ''
            # item['price_card_promo'] = ''
            # item['promo_start_date'] = ''
            # item['promo_end_date'] = ''
            # item['promo_type'] = ''
            # item['in_stock'] = ''
            conn = http.client.HTTPConnection('ifconfig.me')
            conn.request("GET", '/ip')
            get_ip = conn.getresponse().read()
            item['server_ip'] = get_ip
            item['parser_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['models_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['promodata'] = 'promodata'
            item['sku_status'] = i.parent.parent.find_all('button')[1].text
            item['sku_name'] = i.parent.parent.contents[3].contents[0].text
            item['sku_category'] = name_1 + ' ' + '|' + ' ' + name_2
            if i.parent.parent.find('div', text='Акция'):
                print('!!!!!!!!!!!!!!!!!! есть акция !!!!!!!!!!!!!!!!!!!!')
                price_promo = i.parent.parent.contents[3].contents[1].contents[0].contents[0].contents[1].text
                item['price_promo'] = price_promo
                if jsfilconfig['promo_only'] == 'True':
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! только промо товары "!!!!!!!!!!!!!!!!!!!!')
                    item['price_promo'] = price_promo
                    item['price'] = 'был выбор только промотоваров'
                else:
                    item['price'] = price
                    item['price_promo'] = price_promo
            else:
                item['price'] = price

            #ссылка на картинку
            if jsfilconfig['sku_images_enable'] == 'True':
                href_image = i.contents[0].contents[4]['src']
                print('ссылка на картинку : ', href_image)
            else:
                continue

            # условие конечного парсинга продукта
            if jsfilconfig['sku_parameters_enable'] == 'True':
                print('ссылка на конечный парсинг продукта c лайта: ', href2)
                yield scrapy.Request(href2, cb_kwargs=dict(name_2=name_2), callback=self.parse_product_end)
            else:
                continue
            # переход обратно на парсинг продукта со страниц
            # next_page = xtml.find('a', text='next')
            # if next_page is not None:
            #     next_page = response.urljoin(next_page)
            #     yield scrapy.Request(next_page, callback=self.parse_product_lite)

    def parse_product_end(self, response, name_2):
        print('name_2 : ', name_2)
        item = Product()
        root = response.text
        page = BeautifulSoup(root, 'lxml')
        scripts = page.findAll('script')
        my_scripts = scripts[3].prettify(encoding=None, formatter='minimal')
        api = my_scripts.split(';</script>')[0].split('script charset="UTF-8">\n window.__INITIAL_STATE__=')[1]
        js = json.loads(api)
        apis = js['api']
        data = apis['product']['data']

        data_price = data['price']
        print('цена : ',data_price)
        data_prev_price = data['previousPrice']
        print('предыдущая цена : ', data_prev_price)
        data_categories = data['categories']
        print('категория : ', data_categories)
        data_propertyValues = data['propertyValues']
        print('свойства продукта : ',data_propertyValues)

        yield item
        # item['sku_country'] = opis[0].contents[1].contents[1].text
        # item['sku_storage'] = opis[0].contents[2].contents[1].text
        # item['package'] = opis[0].contents[6].contents[1].text
        # item['packed'] = opis[0].contents[4].contents[0].text
        # value = item['sku_packed']
        # print('sku_packed : ', value)
        # # sku_weight_min = scrapy.Field()
        # sku_volume_min = scrapy.Field()
        # sku_quantity_min = scrapy.Field()
        # sku_fat_min = scrapy.Field()
        # sku_alcohol_min = scrapy.Field()
        # sku_link = scrapy.Field()
        # api_link = scrapy.Field()
        # sku_parameters_json = scrapy.Field()
        # sku_images = scrapy.Field()
        # item['sku_barcode'] = ''
        # item['sku_article'] = ''

        next_page = page.find('a', text='next')
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_product_lite)



























