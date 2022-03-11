# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class SkuStatusPipeline(object):
    def process_item(self, item, spider):
        if item['sku_status'] == 'Нет в наличии':
            item['sku_status'] = 0
            return item
        else:
            item['sku_status'] = 'есть в наличии'
            return item


class PricePipeline(object):

    pattern = '.0'

    def process_item(self, item, spider):
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


class SkuPackedPipeline(object):
    def process_item(self, item, spider):
        if item['sku_packed'] == 'Вес':
            item['sku_packed'] = 0
            return item
        elif item['sku_packed'] == 'Объём':
            item['sku_packed'] = 1
            return item
        else:
            item['sku_packed'] = 2
            return item




