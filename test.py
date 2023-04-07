import json

import requests
from bs4 import BeautifulSoup

from func import read_envic, \
    read_products_name, \
    read_products_id, \
    read_stocks, \
    write_stocks, \
    write_products_name, \
    write_products_id, \
    auth, \
    logout, \
    collect_message, \
    send_internal_movements, \
    read_employees, \
    make_items, \
    get_employees_card_number, encod
import random
from pathlib import Path

# envic = read_envic()
#
# token = auth(envic)
#
# get_employees_card_number(token, envic)
# write_stocks(token, envic)
# write_products_name(token, envic)
# write_products_id(token, envic)
# log_out = logout(token, envic)
# print(log_out.url)

# store = read_stocks()
# products = read_products_name()
# products_id = read_products_id()
# names = list(products.keys())
#
# message = collect_message(date_incoming='2023-03-28T00:20',
#                           comment='test',
#                           store_from=store["test_goose"],
#                           store_to=store["Кофе"],
#                           items=make_items(products_list=random.sample(names, 4), amount_list=[2, 2.5, 3.2, 1.98]))
#
# print(message)

# result = send_internal_movements(envic=envic, token=token, message=message)
# print(result)

envic = read_envic()
token = auth(envic)
print(token.text)
# ier = requests.get(envic['protocol'] + '://' +
#                    envic['server'] + ':' +
#                    envic['port'] +
#                    envic['bd'] + 'api/corporation/stores?key=' + token.text)
# soup = BeautifulSoup(ier.content, 'xml')
# print(soup)
print(write_stocks(token, envic))
logout(token, envic)
