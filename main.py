import json
import os.path
import datetime
from pathlib import Path
from flask import Flask, render_template, request
import func

app = Flask(__name__)

employee = None
items = None
products = None


@app.route('/', methods=['post', 'get'])
def check_card_number() -> 'html':
    return render_template('card_number_input.html',
                           the_title='Входъ')


@app.route('/list', methods=['post', 'get'])
def show_list() -> 'html':
    global employee, products
    try:
        products = func.read_products()
        employees = func.read_employees()
        card_num = request.form['card_number']
        if card_num in list(employees.keys()):
            employee = employees[card_num]
            return render_template('list.html',
                                   username=employee,
                                   the_title='Список позиций',
                                   products=products)
        else:
            return render_template('nice.html',
                                   the_title='Неверный номер',
                                   status='Пройдите заново авторизацию',
                                   button_name='Попробовать еще раз',
                                   href='/')
    except KeyError:
        employee = employee
        return render_template('list.html',
                               username=employee,
                               the_title='Список позиций',
                               products=products)


@app.route('/check', methods=['post', 'get'])
def check() -> 'html':
    global items
    store_list = list(func.read_stocks().keys())
    amount_list = request.form.getlist('amount')
    products_list = []
    for i in products:
        for key, value in i.items():
            if key == 'name':
                products_list.append(value)
            else:
                continue
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
                           store_list=store_list)


@app.route('/send', methods=['post', 'get'])
def send() -> 'html':
    if request.form['date'] or request.form['time'] == '' or None:
        dateTtime = str(datetime.datetime.now().isoformat())
        # dateTtime = str((datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=10)))).isoformat())[0:-6]
    else:
        date = request.form['date']
        time = request.form['time']
        dateTtime = f'{date}T{time}:00'
    storefrom = request.form['storeFrom']
    storeto = request.form['storeTo']
    comment = request.form['comment']
    dict_items = func.make_items(items)
    message = func.collect_message(date_incoming=dateTtime,
                                   comment=f'Отправил пользователь: {employee}. '
                                           f'Добавлен комментарий: {comment}',
                                   store_from=storefrom,
                                   store_to=storeto,
                                   items=dict_items)
    envic = func.read_envic()
    token = func.auth(envic)
    result = str(func.send_internal_movements(envic, token, message))
    if result == '<Response [200]>':
        resultus = 'Успешно отправлен.'
    elif result == '<Response [400]>':
        resultus = 'Отправка не удалась. Неверно введены данные.'
    elif result == '<Response [500]>':
        resultus = 'Отправка не удалась. Ошибка сервера'
    func.logout(token, envic)
    return render_template('nice.html',
                           the_title='Результат обработки',
                           username=employee,
                           status=resultus,
                           href='/list',
                           button_name='Создать новый документ')


@app.route('/synch', methods=['post', 'get'])
def synch() -> 'html':
    envic = func.read_envic()
    token = func.auth(envic=envic)
    func.write_stocks(token, envic)
    func.products(token, envic)
    func.get_employees_card_number(token, envic)
    func.logout(token, envic)
    return render_template('nice.html',
                           the_title='Синхронизация выполнена',
                           status='Синхронизация успешно выполнена',
                           href='/',
                           button_name='Создать документ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
