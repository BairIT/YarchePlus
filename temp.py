#
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, FirefoxOptions
import json
import time
import requests as req
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent
#
# # with open('/home/hooch/PycharmProjects/YarchePlus/config.json', 'r') as fil:
# #     jsfilconfig = json.load(fil)
# #
# # with open('cookies', 'r') as file_cookie:
# #     data = json.load(file_cookie)
# #
# #
# # m={}
# # for i in data:
# #     key_data = i['name']
# #     value_data = i['value']
# #     m.update({key_data: value_data})
# #
# # print(m)
#
#
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27"

url = 'https://yarcheplus.ru/category'
driver_path = '/home/hooch/PycharmProjects/YarchePlus/geckodriver'
options = FirefoxOptions()
driver = Firefox(executable_path=driver_path, options=options)
driver.get(url)
time.sleep(3)
address_location = driver.find_element_by_xpath('//button[@title ="Уточните адрес доставки"]')
address_location.click()
print('yes')
address_input = 'Россия, Москва, Вересаева, 10'
address = driver.find_element_by_xpath('//input[@name = "receivedAddress"]')
address.send_keys(address_input)
address.send_keys(Keys.RETURN)
time.sleep(2)
accept_button = driver.find_element_by_xpath('//span[text()="Подтвердить"]')
accept_button.click()

cooks = driver.get_cookies()
# with open('/куки/cookiess', 'w') as file:
for cookie in cooks:
    print(cookie)
driver.close()
time.sleep(5)

driver.add_cookie(cooks)
driver.get(url)


#
# # page = req.get('https://yarcheplus.ru/category', cookies=data)
# # data = BeautifulSoup(page.text, 'html.parser')