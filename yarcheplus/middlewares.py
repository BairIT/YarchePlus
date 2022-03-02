# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import sys

import scrapy_cookies.storage
from scrapy import signals
from os.path import isfile
import scrapy
import logging
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, FirefoxOptions
import time
from bs4 import BeautifulSoup
import requests as req
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

url = 'https://yarcheplus.ru/category'
with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fil:
    jsfilconfig = json.load(fil)
address_input = jsfilconfig['tt_id']
print('c файла адрес: ', address_input)


class YarcheplusSpiderMiddleware:

    # headers = jsfilconfig['headers']
    # print(headers)
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def get_cookies_yarch(self, address_input):
        driver_path = '/home/hooch/PycharmProjects/YarchePlus/geckodriver'
        options = FirefoxOptions()
        driver = Firefox(executable_path=driver_path, options=options)
        driver.get(url)
        time.sleep(2)

        address_location = driver.find_element_by_xpath('//button[@title ="Уточните адрес доставки"]')
        address_location.click()

        address = driver.find_element_by_xpath('//input[@name = "receivedAddress"]')
        address.send_keys(address_input)
        address.send_keys(Keys.RETURN)
        time.sleep(2)

        accept_button = driver.find_element_by_xpath('//span[text()="Подтвердить"]')
        accept_button.click()
        print('адрес вбит')

        cooks = driver.get_cookies()
        print('получаем куки с селениума')

        correct_cookies_from_selenium = {}
        for i in cooks:
            key_data = i['name']
            value_data = i['value']
            correct_cookies_from_selenium.update({key_data: value_data})
        print('куки скорректированы : ', correct_cookies_from_selenium)
        return correct_cookies_from_selenium

    def test_cookies(self, file_cookies):
        headers = {
            'User-Agent': jsfilconfig['headers']
        }
        print(headers)
        page = req.get(url, cookies=file_cookies, headers=headers)
        data = BeautifulSoup(page.text, 'html.parser')
        button = data.find_all('button')
        if button[1] == jsfilconfig['tt_id']:
            print('Да искомый адрес найден, поехали далее ', jsfilconfig['tt_id'])
            return None
        else:
            print('нет адреса в кнопке')
            pass
            # else:
            #     print('получается вообще не нашёл данного адреса вообще')
            #     continue

    def process_spider_input(self, response, spider):
        quetion_address = response.xpath('//button[@title="Уточните адрес доставки"]')
        if quetion_address:
            print('"уточните адрес доставки" есть' + '\n')
            if not isfile('cookies'):
                print('нет куков')
                save_cook = self.get_cookies_yarch(address_input)
                print('куки : ', save_cook)
                with open('cookies', 'w+') as file_cook:
                    json.dump(save_cook, file_cook, indent=4)
                return self.test_cookies(file_cook)
            else:
                print('куки есть')
                pass

        #     print('обратно на страницу для получения куков' + '\n')
        #     self.get_cookies_yarch(self.jsfilconfig['tt_id'])
        #     return None
        #
        # # scrapy_cookies.storage.BaseStorage =
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        #     return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class YarcheplusDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



