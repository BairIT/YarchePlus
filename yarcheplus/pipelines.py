# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class PricePipeline(object):
    # def process_item(self, item, spider):
    #     return item

    # def __init__(self,price,price_promo):
    #     self.price = price
    #     self.price_promo = price_promo

    def process_item(self, item, spider):

        pattern = '.0'
        print(ItemAdapter(item))
        adapter = ItemAdapter(item)
        print(adapter)
        print(type(adapter))
        print(adapter['price'])
        price_list = adapter['price']

        input('stop в пайплайне')
        print('тип : ', type(price_list))
        print(' значение : ', price_list)
        input(' подожди!!  : '  )

        price_list = re.findall('\d*\,\d*', price_list)
        print('цена : ', price_list)
        if price_list is list:
            for i in range(len(price_list)):
                price_list[i] = price_list[i].replace(',', '.')
                price_list[i] = float(price_list[i])
                price_list[i] = round(price_list[i], 1)

            price = price_list[0]
            price_promo = price_list[1]

            if price > price_promo:
                price = str(price)
                price = price.replace(pattern, '')
                price = float(price)
                price = str(price)
                if re.search(pattern, price):
                    price = int(float(price))
                    return [price, price_promo]
                else:
                    print('в цене нет целого числа')
                    print(price)
                    print(price_promo)
                    return [price, price_promo]

            else:
                print('ошибка цена акции больше обычной цены')
                pass
        else:
            print(type(price_list))
            print(price_list)
            price_list = price_list[0].replace(',', '.')
            price_list = float(price_list)
            price_list = round(price_list, 1)
            price = str(price_list)
            if re.search(pattern, price):
                price = int(float(price))
                print(price)
                return price
            else:
                print('в цене нет целого числа')
                print(price)
                return price


        #     adapter['price'] =
        #
        # return item


