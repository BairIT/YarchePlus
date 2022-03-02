# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re


class PricePipeline(object):
    def process_item(self, item, spider):
        return item

    # def __init__(self,price,price_promo):
    #     self.price = price
    #     self.price_promo = price_promo




