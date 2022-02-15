
import requests as req
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime


url = 'https://yarcheplus.ru/category/'

# ua = UserAgent()
# headers = {
#     'user-agent': ua.random
# }
# print(headers)
# source = req.get(url, headers=headers)
# # print(source.status_code)
# soup = BeautifulSoup(source.content, 'html.parser')

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# scr = soup.findAll('a')
# print(scr)
# for i in scr:
#     print(i.get('href'))

# soup = BeautifulSoup(source)
# print(soup)
