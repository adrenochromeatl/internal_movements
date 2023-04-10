import json
import requests
from bs4 import BeautifulSoup

import func
import random
from pathlib import Path


envic = func.read_envic()
token = func.auth(envic)
func.write_stocks(token, envic)
func.write_products_name(token, envic)
func.write_products_id(token, envic)
func.get_employees_card_number(token, envic)
func.logout(token, envic)
# with open(Path(Path.cwd(), 'resource', 'products.json')) as file:
#     products = json.load(file)
#
# name_mainUnit = {}
# for item in products:
#     name = item['name']
#     mainUnit = item['mainUnit']
#     name_mainUnit.update({name: mainUnit})
#
# print(name_mainUnit)
