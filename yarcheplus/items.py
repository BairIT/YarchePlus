# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


def serialize_price(value):
    pass


class Product(scrapy.Item):
    # define the fields for your item here like:
    parser_id = scrapy.Field(
        
    )
    chain_id = scrapy.Field()
    tt_id = scrapy.Field()
    tt_region = scrapy.Field()
    tt_name = scrapy.Field()
    price_datetime = scrapy.Field()
    price = scrapy.Field()
    # price_promo = scrapy.Field()
    # price_card = scrapy.Field()
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

