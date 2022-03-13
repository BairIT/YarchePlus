# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


def price_vs_price_promo(price, price_promo):
    print(' пришёл в сравнение цен ')
    if price < price_promo:
        print('случай сравнения невозможен, т.к промо выше обычной')
        price = ''
        price_promo = ''
        return price, price_promo

    else:
        print('возвращаю, price : ', price)
        print('возвращаю, price : ', price_promo)
        return price, price_promo


class SkuStatusPipeline(object):
    def process_item(self, item, spider):
        print('пришёл в статус')
        if item['sku_status'] == '':
            print('item[sku_status] = ''')
            item['sku_status'] = 0
            return item
        else:
            print(f"item[sku_status] = {item['sku_status']}")
            item['sku_status'] = 1
            return item


class PricePipeline(object):

    pattern = '.0'

    def process_item(self, item, spider):
        print('пришёл в цену')
        if item['price']:
            price = item['price']
            price = price.replace(' ', '')
            price = re.findall('\d*\,\d*', price)
            print(price)
            price = price[0].replace(',', '.')
            price = round(float(price), 1)
            price = str(price)
            price = price.replace(self.pattern, '')
            if re.search(self.pattern, price):
                item['price'] = int(float(price))
                print(item['price'])
                return item
            else:
                print(f'нету целого числа в {price}')
                item['price'] = price
                return item
        else:
            return DropItem('missing price')


class PricePromoPipeline(object):
    pattern = '.0'

    def process_item(self, item, spider):
        print('пришёл в цену промо')
        if item['price_promo']:
            price_promo = item['price_promo']
            price_promo = price_promo.replace(' ', '')
            price_promo = re.findall('\d*\,\d*', price_promo)
            print(price_promo)
            price_promo = price_promo[0].replace(',', '.')
            price_promo = round(float(price_promo), 1)
            price_promo = str(price_promo)
            price_promo = price_promo.replace(self.pattern, '')
            if re.search(self.pattern, price_promo):
                item['price_promo'] = int(float(price_promo))
                print(item['price_promo'])
                return item
            else:
                print(f'нету целого числа в {price_promo}')
                item['price_promo'] = price_promo
                return item
        else:
            item['price_promo'] = 'нету прайс цены'
            return item
            # return DropItem(f'missing price {item}')

# class SkuPackedPipeline(object):
#     def process_item(self, item, spider):
#         if item['sku_packed'] == 'Вес':
#             item['sku_packed'] = 0
#             return item
#         elif item['sku_packed'] == 'Объём':
#             item['sku_packed'] = 1
#             return item
#         else:
#             item['sku_packed'] = 2
#             return item




