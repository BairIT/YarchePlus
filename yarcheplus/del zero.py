
import math
import re
pattern = '.0'
list_str = []
v = input('введите число : ')
list_str.append(v)
w = input('введите второе число : ')
list_str.append(w)

for i in range(len(list_str)):
    list_str[i] = list_str[i].replace(',', '.')
    list_str[i] = float(list_str[i])
    list_str[i] = round(list_str[i], 1)
print('список вещественных чисел : ' + '\n', list_str)
print(len(list_str))

price = list_str[0]
price_promo = list_str[1]

if price > price_promo:
    price = str(price)
    price = price.replace(pattern, '')
    price = float(price)
    price = str(price)
    if re.search(pattern, price):
        price= int(float(price))
        print(price)
    else:
        print('нету целого числа')
        pass
    # price = str(price)
    # price = price.replace(pattern, '')
    # print(price)
    # price = float(price)

    print('цена акции : ', price_promo)
    print('обычная цена : ', price)
else:
    price = ''
    price_promo = ''
    print(' обычная цена : ', price)
    print(' цена акции : ', price_promo)

# string = str(v)
# pattern = '.0'
# if re.search(pattern, string):
#     string = string.replace(pattern, '')
# else:
#     print('нету')
#
# print(string)


