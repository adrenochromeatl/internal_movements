import json
import os.path
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request
import func

app = Flask(__name__)

employee = None
items = None


@app.route('/', methods=['post', 'get'])
def check_card_number() -> 'html':
    return render_template('card_number_input.html',
                           the_title='Вход')


@app.route('/list', methods=['post', 'get'])
def show_list() -> 'html':
    global employee
    try:
        card_num = request.form['card_number']
        employee = func.read_employees()[card_num]
    except:
        try:
            employee = employee
        except:
            return render_template('nice.html',
                                   the_title='Неверный номер',
                                   status='Пройдите заново авторизацию')
    with open(Path(Path.cwd(), 'resource', 'products.json')) as file:
        products = json.load(file)
    name_mainUnit = {}
    for item in products:
        name = item['name']
        mainUnit = item['mainUnit']
        name_mainUnit.update({name: mainUnit})
    return render_template('list.html',
                           username=employee,
                           the_title='Список позиций',
                           products=name_mainUnit)


@app.route('/check', methods=['post', 'get'])
def check() -> 'html':
    global items
    store_list = list(func.read_stocks().keys())
    amount_list = request.form.getlist('amount')
    with open(Path(Path.cwd(), 'resource', 'products.json')) as file:
        products = json.load(file)
    name_mainUnit = {}
    for item in products:
        name = item['name']
        mainUnit = item['mainUnit']
        name_mainUnit.update({name: mainUnit})
    products_list = list(name_mainUnit.keys())
    pram = dict(zip(products_list, amount_list))
    items = {}
    for key, value in pram.items():
        if value != '':
            items.update({key: value})
        else:
            continue
    return render_template('check.html',
                           username=employee,
                           items=items,
                           store_list=store_list,
                           name_mainUnit=name_mainUnit)


@app.route('/send', methods=['post', 'get'])
def send() -> 'html':
    date = request.form['date']
    time = request.form['time']
    storefrom = request.form['storeFrom']
    storeto = request.form['storeTo']
    comment = request.form['comment']
    dict_items = func.make_items(items)
    message = func.collect_message(date_incoming=f'{date}T{time}:00',
                                   comment=f'Отправил пользователь: {employee}. '
                                           f'Добавлен комментарий: {comment}',
                                   store_from=storefrom,
                                   store_to=storeto,
                                   items=dict_items)
    envic = func.read_envic()
    token = func.auth(envic)
    result = str(func.send_internal_movements(envic, token, message))
    if result == '<Response [200]>':
        result = 'Успешно отправлен.'
    elif result == '<Response [400]>':
        result = 'Отправка не удалась. Неверно введены данные.'
    elif result == '<Response [500]>':
        result = 'Отправка не удалась. Ошибка сервера'
    func.logout(token, envic)
    return render_template('nice.html',
                           username=employee,
                           status=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
