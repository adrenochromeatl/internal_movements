import json

import requests
from bs4 import BeautifulSoup
import datetime
import func
import random
from pathlib import Path

# envic = read_envic()
#
# token = auth(envic)
#

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

server_data = func.read_envic()
token = func.auth(server_data)
print(func.categories(token, server_data))
func.logout(token, server_data)
