import json
import os
import requests
import hashlib
from bs4 import BeautifulSoup
from pathlib import Path

encod = 'UTF-8'


def read_envic():
    with open(Path(Path.cwd(), 'resource', 'envic.json')) as file:
        envic = json.load(file)
    return envic


def auth(envic):
    sha1pass = hashlib.sha1(envic['password'].encode('utf-8')).hexdigest()
    auth_url = (envic['protocol'] + '://' +
                envic['server'] + ':' +
                envic['port'] +
                envic['bd'] + '/api/auth?login=' +
                envic['login'] + '&pass=' + sha1pass)
    token = requests.get(auth_url)
    return token


def logout(token, server_data):
    out_url = (server_data['protocol'] + '://' +
               server_data['server'] + ':' +
               server_data['port'] +
               server_data['bd'] + '/api/logout?key=' + token.text)
    result = requests.get(out_url)
    return result


def write_stocks(token, envic):
    gets_url = (envic['protocol'] + '://' +
                envic['server'] + ':' +
                envic['port'] +
                envic['bd'] + '/api/corporation/stores?key=' + token.text)
    store = requests.get(gets_url)
    soup = BeautifulSoup(store.content, 'xml')
    stocks_list = []
    for name in soup.find_all('name'):
        stocks_list.append(name.string)
    stocks_id = []
    for id in soup.find_all('id'):
        stocks_id.append(id.text)
    stocks_full = dict(zip(stocks_list, stocks_id))
    with open(Path('resource', 'stocks.json'), 'w', encoding=encod) as file:
        json.dump(stocks_full, file, indent=4, ensure_ascii=False)
    return stocks_full


def read_stocks():
    with open(Path('resource', 'stocks.json'), encoding=encod) as file:
        stocks = json.load(file)
    return stocks


def products(token, server_data):
    url = (server_data['protocol'] + '://' +
           server_data['server'] + ':' +
           server_data['port'] +
           server_data['bd'] + '/api/products?key=' + token.text)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    result = []
    for productDto in soup.find_all('productDto'):
        try:
            id = productDto.find('id').string
        except AttributeError:
            id = 'None'

        try:
            parentId = productDto.find('parentId').string
        except AttributeError:
            parentId = 'None'

        try:
            num = productDto.find('num').string
        except AttributeError:
            num = 'None'

        try:
            code = productDto.find('code').string
        except AttributeError:
            code = 'None'

        try:
            name = productDto.find('name').string
        except AttributeError:
            name = 'None'

        try:
            productType = productDto.find('productType').string
        except AttributeError:
            productType = 'None'

        try:
            cookingPlaceType = productDto.find('cookingPlaceType').string
        except AttributeError:
            cookingPlaceType = 'None'

        try:
            mainUnit = productDto.find('mainUnit').string
        except AttributeError:
            mainUnit = 'None'

        try:
            productCategory = productDto.find('productCategory').string
        except AttributeError:
            productCategory = 'None'

        eta = {
            "id": id,
            "parentId": parentId,
            "num": num,
            "code": code,
            "name": name,
            "productType": productType,
            "cookingPlaceType": cookingPlaceType,
            "mainUnit": mainUnit,
            "productCategory": productCategory
        }
        result.append(eta)
    with open(Path('resource', 'products.json'), 'w', encoding=encod) as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    return result


def read_products():
    with open(Path('resource', 'products.json'), encoding=encod) as file:
        result = json.load(file)
    return result


def categories(token, server_data):
    url = (server_data['protocol'] + '://' +
           server_data['server'] + ':' +
           server_data['port'] +
           server_data['bd'] + "/api/v2/entities/products/category/list?key=" + token.text)
    cats = requests.get(url).json()
    with open(Path('resource', 'categories.json'), 'w', encoding=encod) as file:
        json.dump(cats, file, indent=4, ensure_ascii=False)
    return cats


def read_categories():
    with open(Path('resource', 'categories.json'), encoding=encod) as file:
        cats = json.load(file)
    return cats


def make_items(name_amount_list):
    products_dict = {}
    for item in read_products():
        products_dict.update({item['name']: item['id']})
    items = []
    for name, amount in name_amount_list.items():
        one_piece = {
            "productId": products_dict[name],
            "amount": amount
        }
        items.append(one_piece)
    return items


def collect_message(date_incoming, comment, store_from, store_to, items):  # Зашить имя в коммент
    store = read_stocks()
    message = {
        "id": "",
        "dateIncoming": date_incoming,
        "documentNumber": "",
        "status": "NEW",
        "comment": comment,
        "storeFromId": store[store_from],
        "storeToId": store[store_to],
        "items": items
    }
    return message


def send_internal_movements(envic, token, message):
    url = (envic['protocol'] + '://' +
           envic['server'] + ':' +
           envic['port'] +
           envic['bd'] + '/api/v2/documents/internalTransfer?key=' + token.text)
    headers = {'Content-Type': 'application/json'}
    answer = str(requests.post(url, json=message, headers=headers))
    return answer


def get_employees_card_number(token, envic):
    url = (envic['protocol'] + '://' +
           envic['server'] + ':' +
           envic['port'] +
           envic['bd'] + '/api/employees?key=' + token.text)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    employees = []
    for items in soup.find_all('employee'):
        employees.append(items)
    result = {}
    for i in employees:
        if i.find('name') is None:
            name = 'NoName'
        else:
            name = i.find('name').text
        if i.find('cardNumber') is None:
            card = 'NoCard'
        else:
            card = i.find('cardNumber').text
        result.update({card: name})

    with open(Path('resource', 'employees.json'), 'w', encoding=encod) as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    return result


def read_employees():
    with open(Path('resource', 'employees.json'), encoding=encod) as file:
        employees = json.load(file)
    return employees
