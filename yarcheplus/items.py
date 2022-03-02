# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from dataclasses import dataclass, field
from typing import Optional

pattern = '.0'


def is_promo(value):
    value_prices = re.findall('\d*\,\d*', value)
    print(value_prices)
    print(len(value_prices))
    input('посмотри')
    if len(value_prices) > 1:
        price = value_prices[0]
        price_promo = value_prices[1]
        price = price_go_float_with_point(price)
        price = get_normal_price(price)
        price_promo = price_go_float_with_point(price_promo)
        price_promo = get_normal_price(price_promo)
        print('промо-цена : ', price_promo)
        prices = {
            'price': price,
            'price_promo': price_promo
        }
        print('цена обычная : ', prices['price'])
        print('промо-цена : ', prices['price_promo'])
        return prices
    else:
        price = value_prices[0]
        price = price_go_float_with_point(price)
        price = get_normal_price(price)
        print('возврат форматированной цены : ', price)
        prices = {
            'price': price,
        }
        return prices


def price_promo_out(prices):
    price_promo = prices['price']
    print('функция в out промо - цену : ', price_promo)
    return price_promo


def price_out(prices):
    price = prices['price']
    print('функция в out цену : ', price)
    return price


def price_go_float_with_point(value_price):
    value_price = value_price.replace(',', '.')
    value_price = float(value_price)
    value_price = round(value_price, 1)
    print('цена  - вещественное число округленное : ', value_price)
    return value_price


def get_normal_price(value_price):
        price = str(value_price)
        price = price.replace(pattern, '')
        price = float(price)
        price = str(price)
        print('цена(строка): ', price)
        if re.search(pattern, price):
            price = int(float(price))
            print('цена целого типа, без нулей :', price)
            return price
        else:
            print('нет в цене целого числа, с точкой : ', price)
            return price


class Product(scrapy.Item):
    # define the fields for your item here like:
    # parser_id = scrapy.Field(
    #
    # )
    # chain_id = scrapy.Field()
    # tt_id = scrapy.Field()
    # tt_region = scrapy.Field()
    # tt_name = scrapy.Field()
    price_datetime = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(is_promo, price_out),
        output_processor=TakeFirst(),
    )
    price_promo = scrapy.Field(
        input_processor=MapCompose(price_promo_out),
        output_processor=TakeFirst()
    )
    # # price_card = scrapy.Field()
    # price_card_promo = scrapy.Field()
    # promo_start_date = scrapy.Field()
    # promo_end_date = scrapy.Field()
    # promo_type = scrapy.Field()
    # in_stock = scrapy.Field()
    # sku_status = scrapy.Field()
    # sku_barcode = scrapy.Field()
    # sku_article = scrapy.Field()
    sku_name = scrapy.Field()
    # sku_category = scrapy.Field()
    # sku_brand = scrapy.Field()
    # sku_country = scrapy.Field()
    # sku_manufacturer = scrapy.Field()
    # sku_package = scrapy.Field()
    # sku_packed = scrapy.Field()
    # sku_weight_min = scrapy.Field()
    # sku_volume_min = scrapy.Field()
    # sku_quantity_min = scrapy.Field()
    # sku_fat_min = scrapy.Field()
    # sku_alcohol_min = scrapy.Field()
    # sku_link = scrapy.Field()
    # api_link = scrapy.Field()
    # sku_parameters_json = scrapy.Field()
    # sku_images = scrapy.Field()
    # server_ip = scrapy.Field()
    # parser_date = scrapy.Field()
    # models_date = scrapy.Field()
    # promodata = 'promodata'


def searcher_link():
    pass


class Link(scrapy.Item):
    link = scrapy.Field()
    internal_link = scrapy.Field()
    internal_internal_link = scrapy.Field()






















