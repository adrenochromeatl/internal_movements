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

# envic = func.read_envic()
# token = func.auth(envic)
# func.products(token, envic)
# print(func.read_products())
# func.logout(token, envic)
t = str((datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=10)))).isoformat())[0:-6]
print(t)
