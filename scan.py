import time
import json
import random

from telethon.sync import TelegramClient
from binance.client import Client
from db import DataBase
import db_current
import db_history

api_key = 'guc1lTxCyiS1rvEzD3LrK3MEsfnl5DyNkZaA9LcnzBKyk8BmMHTJ01t142ncvfqz'
api_secret = 'm1xf8NO7ZUGpaNq0hoC3AYvOtdVCou3oX4zlRGKl9wpTY48droq1it6wZOphTNay'
pump_percent = 0.5


def convert_to_dict(symbols: list):
    result_dict = {}
    for i in symbols:

        if i['symbol'] in result_dict.keys() and float(i['stopPrice']) > float(result_dict[i['symbol']]['stopPrice']):
            result_dict[i['symbol']] = i
        elif i['symbol'] not in result_dict.keys():
            result_dict[i['symbol']] = i
    return result_dict


def check_count_numbers(number):
    number = str(number)
    print(number)
    second_part = number.split('.')[1]
    return len(second_part)


def scan_main_value():
    client_bin = Client(api_key, api_secret)
    tickers = client_bin.futures_ticker()
    for i in tickers:
        if i['symbol'][-3:] == 'BTC':
            print(i)
            if database.check_symbol(i['symbol']):
                database.new_value(i['symbol'], i['lastPrice'])
            else:
                database.register(i['symbol'], i['lastPrice'])


def scan_current_price():
    full_list = []
    client_bin = Client(api_key, api_secret)
    tickers = client_bin.get_ticker()
    base = database.get_symbols()
    exchange = convert_to_dict(client_bin.futures_exchange_info()['symbols'])
    for i in tickers:
        if i['symbol'][-3:] == 'BTC':
            try:
                if float(i['lastPrice']) - float(base[i['symbol']]) > float(base[i['symbol']])/100 * pump_percent:
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print(i['symbol'])
                    print(i['lastPrice'])
                    print(base[i['symbol']])
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    amount_precision = int(check_count_numbers(float(i['lastPrice'])))
                    full_list.append([i['symbol'], i['lastPrice'], amount_precision])

            except KeyError:
                continue
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

        print(setting)
        old = []
        for index, dialog in enumerate(dialogs):
            if index < 250:
                if str(dialog.id) == setting['channels']['first_channel']:
                    first_channel = dialog
                elif str(dialog.id) == setting['channels']['second_channel']:
                    second_channel = dialog

    scan_main_value()
    i = 0
    while True:
        time.sleep(15)

        print(i)
        i += 1
        try:
            results = scan_current_price()
        except Exception as e:
            print(e)
            time.sleep(60)
            continue
        for symbol in results:
            if symbol[0] not in old:
                final_price = [float(symbol[1]), symbol[2]]
                if int(symbol[2]) < 3:
                    continue
                round_number = check_count_numbers(symbol[1])
                currency = symbol[0].replace("BTC", "/BTC")
                message = f"""
⚡️⚡️ #{currency} ⚡️⚡️
Signal Type: Spot

Entry Targets:
1) {round(final_price[0]/100*97, final_price[1])}
2) {final_price[0]}

Take-Profit Targets:
1) {round(final_price[0]/100*103, final_price[1])}
2) {round(final_price[0]/100*105, final_price[1])}
3) {round(final_price[0]/100*107, final_price[1])}
4) {round(final_price[0]/100*109, final_price[1])}
        """
                client.send_message(first_channel, message)
                client.send_message(second_channel, message)
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
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                time.sleep(random.randint(60*60*1, 60*60*2))
# correct_number(float('{:.12f}'.format(float(symbol[1])/100*97).rstrip('0')))
# Попробуй поработать с начальным часло, на самом первом этапе
