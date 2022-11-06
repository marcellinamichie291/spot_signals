import time
import json
import random

from telethon.sync import TelegramClient
from telethon import events
from binance.client import Client
from db import DataBase
import db_current
import db_history

api_key = 'guc1lTxCyiS1rvEzD3LrK3MEsfnl5DyNkZaA9LcnzBKyk8BmMHTJ01t142ncvfqz'
api_secret = 'm1xf8NO7ZUGpaNq0hoC3AYvOtdVCou3oX4zlRGKl9wpTY48droq1it6wZOphTNay'
pump_percent = 2.5


def correct_number(target):
    target = list(target)
    target.reverse()

    result_list = []
    last_num = None

    for num in target:
        if num == "0" and last_num == ".":
            break
        else:
            result_list.append(num)
            last_num = num

    result_list.reverse()
    print(result_list)

    if result_list[0] == ".":
        result_list.pop(0)

    while True:
        if result_list[0] == "0":
            result_list.pop(0)
        else:
            break

    line = ""
    for char in result_list:
        line += char
    if "." in line:
        return float(line)
    else:
        return int(float(line))


def check_count_numbers(number):
    number = str(number)
    second_part = number.split('.')[1]
    return len(second_part)


def scan_main_value():
    client_bin = Client(api_key, api_secret)
    tickers = client_bin.get_all_tickers()
    for i in tickers:
        if i['symbol'][-3:] == 'BTC':
            if database.check_symbol(i['symbol']):
                database.new_value(i['symbol'], i['price'])
            else:
                database.register(i['symbol'], i['price'])


def scan_current_price():
    full_list = []
    client_bin = Client(api_key, api_secret)
    tickers = client_bin.get_all_tickers()
    base = database.get_symbols()
    for i in tickers:
        if i['symbol'][-3:] == 'BTC':
            if float(i['price']) - float(base[i['symbol']]) > float(base[i['symbol']])/100 * pump_percent or i['symbol']=='ALGOBTC':
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(i['symbol'])
                print(i['price'])
                print(base[i['symbol']])
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                full_list.append([i['symbol'], i['price']])
    return full_list


if __name__ == '__main__':

    database = DataBase('db.db')
    target_db = db_current.DataBase('current_signals.db')
    history_db = db_history.DataBase('history.db')

    post_count = random.randint(3, 8)
    counter = 0
    with open("setting.json", 'r', encoding='utf8') as out:
        setting = json.load(out)

        client = TelegramClient(
            setting['account']['session'],
            setting['account']['api_id'],
            setting['account']['api_hash']
        )

        client.start()

    dialogs = client.get_dialogs()

    for index, dialog in enumerate(dialogs):
        print(f'[{index}] {dialog.name}')

    first_channel = dialogs[int(input("First channel index: "))]
    old = []

    scan_main_value()
    i = 0
    while True:
        time.sleep(3)

        print(i)
        i += 1
        results = scan_current_price()
        for symbol in results:
            if symbol[0] not in old:
                final_price = int(correct_number(str(symbol[1])))
                print(len(str(final_price)))
                if len(str(final_price)) < 3 or 5 <= len(str(final_price)):
                    print('yts')
                    continue
                round_number = check_count_numbers(symbol[1])
                currency = symbol[0].replace("BTC", "/BTC")
                message = f"""
#{currency}
Buy: {int(final_price/100*97)} - {final_price}
Sell: {int(final_price/100*103)} - {int(final_price/100*105)} - {int(final_price/100*107)} - {int(final_price/100*109)}
        """
                client.send_message(first_channel, message)
                old.append(symbol[0])
                if target_db.check_symbol(symbol[0]):
                    if target_db.check_complete(symbol[0]):
                        target_db.new_value(symbol[0],
                                            str("%.16f" % round(float(symbol[1])/100*103, round_number)).rstrip('0'),
                                            str("%.16f" % round(float(symbol[1])/100*105, round_number)).rstrip('0'),
                                            str("%.16f" % round(float(symbol[1])/100*107, round_number)).rstrip('0'),
                                            str("%.16f" % round(float(symbol[1])/100*109, round_number)).rstrip('0'),
                                            symbol[1],
                                            time.time())
                        try:
                            history_db.register(symbol[0])

                            print(symbol[0])
                            print('Ok')
                        except Exception as e:
                            print(e)
                else:
                    target_db.register(symbol[0],
                                       str("%.16f" % round(float(symbol[1])/100*103, round_number)).rstrip('0'),
                                       str("%.16f" % round(float(symbol[1])/100*105, round_number)).rstrip('0'),
                                       str("%.16f" % round(float(symbol[1])/100*107, round_number)).rstrip('0'),
                                       str("%.16f" % round(float(symbol[1])/100*109, round_number)).rstrip('0'),
                                       symbol[1],
                                       time.time())
                    try:
                        history_db.register(symbol[0])
                        print(symbol[0])
                        print('Ok')
                    except Exception as e:
                        print(e)

# correct_number(float('{:.12f}'.format(float(symbol[1])/100*97).rstrip('0')))
# Попробуй поработать с начальным часло, на самом первом этапе
