import json
import os.path
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request
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
    employee = request.form['card_number']
    products_list = list(read_products_name().keys())
    return render_template('list.html',
                           the_title='Список позиций',
                           products_list=products_list)


@app.route('/check', methods=['post', 'get'])
def check() -> 'html':
    global items
    store_list = list(read_stocks().keys())
    amount_list = request.form.getlist('amount')
    products_list = list(read_products_name().keys())
    pram = dict(zip(products_list, amount_list))
    items = {}
    for key, value in pram.items():
        if value != '':
            items.update({key: value})
        else:
            continue
    return render_template('check.html',
                           items=items,
                           store_list=store_list)


@app.route('/send', methods=['post', 'get'])
def send() -> 'html':
    date = request.form['date']
    time = request.form['time']
    storefrom = request.form['storeFrom']
    storeto = request.form['storeTo']
    comment = request.form['comment']
    dict_items = make_items(items)
    message = collect_message(date_incoming=f'{date}T{time}:00',
                              comment=f'Отправил пользователь: {employee}. '
                                      f'Добавлен комментарий: {comment}',
                              store_from=storefrom,
                              store_to=storeto,
                              items=dict_items)
    envic = read_envic()
    token = auth(envic)
    result = str(send_internal_movements(envic, token, message))
    logout(token, envic)
    return render_template('nice.html',
                           status=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
