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
    sha1pass = hashlib.sha1('restoRtest'.encode('utf-8')).hexdigest()
    auth_url = (envic['protocol'] + '://' +
                envic['server'] + ':' +
                envic['port'] +
                envic['bd'] + '/api/auth?login=' +
                'admin' + '&pass=' + sha1pass)
    token = requests.get(auth_url)
    return token


def logout(token, envic):
    out_url = (envic['protocol'] + '://' +
               envic['server'] + ':' +
               envic['port'] +
               envic['bd'] + '/api/logout?key=' + token.text)
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


def write_products_name(token, envic):
    url = (envic['protocol'] + '://' +
           envic['server'] + ':' +
           envic['port'] +
           envic['bd'] + '/api/products?key=' + token.text)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    products_list = []
    for name in soup.find_all('name'):
        products_list.append(name.string)
    products_id = []
    for id in soup.find_all('id'):
        products_id.append(id.text)
    products_full = dict(zip(products_list, products_id))
    with open(Path('resource', 'products_name.json'), 'w', encoding=encod) as file:
        json.dump(products_full, file, indent=4, ensure_ascii=False)
    # return products_full
    return soup

def write_products_id(token, envic):
    url = (envic['protocol'] + '://' +
           envic['server'] + ':' +
           envic['port'] +
           envic['bd'] + '/api/products?key=' + token.text)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    products_list = []
    for name in soup.find_all('name'):
        products_list.append(name.string)
    products_id = []
    for id in soup.find_all('id'):
        products_id.append(id.text)
    products_full = dict(zip(products_id, products_list))
    with open(Path('resource', 'products_id.json'), 'w', encoding=encod) as file:
        json.dump(products_full, file, indent=4, ensure_ascii=False)
    return products_full


# Прочитать ИЗ ЛОГА продукты {name:id}
def read_products_name():
    with open(Path('resource', 'products_name.json'), encoding=encod) as file:
        products = json.load(file)
    return products


def read_products_id():
    with open(Path('resource', 'products_id.json'), encoding=encod) as file:
        products = json.load(file)
    return products


def make_items(name_amount_list):
    products_dict = read_products_name()
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
