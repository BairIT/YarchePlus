
from os.path import isfile
import scrapy
import logging
import json
from bs4 import BeautifulSoup
from yarcheplus.middlewares import jsfilconfig
from yarcheplus.items import Product
from yarcheplus.pipelines import price_vs_price_promo
from yarcheplus.pipelines import PricePipeline
import datetime
import http.client

import yarcheplus.middlewares
from yarcheplus.middlewares import address_input

logger = logging.getLogger('yarchepluslogs')

# with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fs:
#     data = json.load(fs)


def item_input(i, name_1, name_2):
    item = Product()
    item['parser_id'] = jsfilconfig['parser_id']
    item['chain_id'] = jsfilconfig['chain_id']
    item['tt_id'] = jsfilconfig['tt_id']
    item['tt_region'] = jsfilconfig['tt_id'].split(sep=', ')[1]
    item['tt_name'] = jsfilconfig['tt_name']
    item['price_datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = http.client.HTTPConnection('ifconfig.me')
    conn.request("GET", '/ip')
    get_ip = conn.getresponse().read()
    item['server_ip'] = get_ip
    item['parser_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item['models_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item['promodata'] = 'promodata'
    print("item['skustatus'] : ", i.parent.parent.find_all('button')[1].text)
    s = i.parent.parent.find_all('button')[1].text
    print('текст : ', s)
    item['sku_status'] = i.parent.parent.find_all('button')[1].text
    item['sku_name'] = i.parent.parent.contents[3].contents[0].text
    item['sku_category'] = name_1 + ' ' + '|' + ' ' + name_2
    yield item


def test_pro(i):
    # ссылка на картинку
    if jsfilconfig['sku_images_enable'] == 'True':
        href_image = i.contents[0].contents[4]['src']
        print('ссылка на картинку : ', href_image)
        return href_image
    else:
        pass


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
            print(' урло : ', url)
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
        print('*'*20+'на начале цикла парсинга продуктов'+'*'*20)
        for i in a:

            price = i.parent.parent.contents[3].contents[1].contents[0].contents[0].contents[0].text
            sku_status = i.parent.parent.find_all('button')[1].text
            item['sku_status'] = sku_status
            href2 = 'https://yarcheplus.ru' + i.get('href')
            if i.parent.parent.find('div', text='Акция'):
                print('Есть акция')
                price_promo = i.parent.parent.contents[3].contents[1].contents[0].contents[0].contents[1].text
                if jsfilconfig['promo_only'] == 'True':
                    print('только промо товары ')
                    item['price_promo'] = price_promo
                    item['price'] = 'был выбор только промотоваров'
                    # условие конечного парсинга продукта
                    if jsfilconfig['sku_parameters_enable'] == 'True':
                        print('ску параметр инайбл, ссылка на конечный парсинг продукта c лайта: ', href2)
                        yield scrapy.Request(href2, cb_kwargs=dict(name_2=name_2, name_1=name_1, i=i), callback=self.parse_product_end)
                    else:
                        print(' ску параметр не инейбл, пошли дальше')
                        continue

                else:
                    print('не промо товары')
                    item['price'] = price
                    item['price_promo'] = price_promo
                    item_input(i, name_1, name_2)
                    yield item
                    # условие конечного парсинга продукта

            else:
                print('я здесь смотри на нет акции')

                item['price'] = price
                item['price_promo'] = ''
                item_input(i, name_1, name_2)
                yield item
                # условие конечного парсинга продукта

        pggg = xtml.find('a', text='next')
        print('pggg : ', pggg)
        if pggg is None:
            print('_______ненашла некст в предпоследнем парсе')
            pass
        else:
            print('______нашла некст в предпоследнем парсе')

            print(xtml.find('a', text='next')['href'])
            print(type(xtml.find('a', text='next')['href']))

            next_page = 'https://yarcheplus.ru' + xtml.find('a', text='next')['href']

            print('next_page_сформирована : ', next_page)

            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_product_lite)

    def parse_product_end(self, response, name_1, name_2, i):
        print('name_2 : ', name_2)
        item = Product()
        item_input(i, name_1, name_2)
        root = response.text
        page = BeautifulSoup(root, 'lxml')
        scripts = page.findAll('script')
        need_scripts = scripts[3].prettify(encoding=None, formatter='minimal')
        data_js = need_scripts.split(';'+'\n'+'</script>')[0].split('script charset="UTF-8">\n window.__INITIAL_STATE__=')[1]
        js = json.loads(data_js)
        apis = js['api']
        data = apis['product']['data']
        data_name = data['name']
        print('имя : ', data_name)
        # data_description = data['description']
        # print('описание : ', data_description)
        print('_____________')
        data_price = data['price']
        print('цена : ', data_price)
        data_prev_price = data['previousPrice']
        print('предыдущая цена : ', data_prev_price)
        data_categories = data['categories'][0]['name']
        print('категория : ', data_categories)

        data_propertyValues = data['propertyValues']

        for i in data_propertyValues:
            print(' я здесь в цикле')
            if 'item' in i:
                print('good item')
                print(i['property']['title'] + ' : ' + i['item']['label'])
                yield {
                    i['property']['title']: i['item']['label']
                }
            else:
                if 'list' in i:
                    print('good list')
                    print(i['property']['title'] + ' : ' + i['list'][0]['label'])
                    yield {
                        i['property']['title']: i['list'][0]['label']
                    }
                else:
                    if 'strValue' in i:
                        print('good_strValue')
                        print(i['property']['title'] + ' : ' + i['strValue'])
                        yield {
                            i['property']['title']: i['strValue']
                        }
                    else:
                        print(i)
                        pass

        yield item

        next_page = page.find('a', text='next')
        print('next page в последнем месте, братан: ', next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_product_end)



























