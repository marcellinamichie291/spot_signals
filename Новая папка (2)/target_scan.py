from binance.client import Client
from telethon.sync import TelegramClient
import time
import db_current as db
import db_history
import datetime
from humanfriendly import format_timespan

db = db.DataBase('current_signals.db')
history_db = db_history.DataBase('history.db')


def convert(time_float) -> str:
    # return round(time_float / 3600, 1)
    return format_timespan(time_float)


def scan():
    api_key = 'guc1lTxCyiS1rvEzD3LrK3MEsfnl5DyNkZaA9LcnzBKyk8BmMHTJ01t142ncvfqz'
    api_secret = 'm1xf8NO7ZUGpaNq0hoC3AYvOtdVCou3oX4zlRGKl9wpTY48droq1it6wZOphTNay'
    client_bin = Client(api_key, api_secret)
    tickers_dict = {}
    tickers = client_bin.get_all_tickers()
    for ticker in tickers:
        tickers_dict[ticker['symbol']] = ticker['price']

    print('Скан...')

    target_symbols = db.get_symbols()
    print('!!!!!!!!!!!!!!')
    print(target_symbols)
    for symbol in target_symbols:
        try:
            if float(tickers_dict[symbol[1]]) >= float(symbol[5]):
                print('yes')
                currency = symbol[1].replace("BTC", "/BTC")
                try:
                    profit = round(float(tickers_dict[symbol[1]]) / (float(symbol[6]) / 100) - 100, 1)
                except TypeError:
                    continue
                print('!!!!!!')
                print(symbol)
                print(symbol[3])
                timer = convert(time.time() - float(symbol[7]))
                message = f"""
Binance
#{currency} Take-Profit target 4 ✅
Profit: {profit}% 📈
Period: {timer}⏰
                """
                print(message)
                client.send_message(script_channel, message)
                print('Сообщение отправлено!')
                try:
                    db.new_none(symbol[1], 4)
                except Exception as e:
                    print(e)
                    print('tyt')

                history_db.new_value(symbol[1], 4)
            elif float(tickers_dict[symbol[1]]) >= float(symbol[4]):
                print('yes')
                currency = symbol[1].replace("BTC", "/BTC")
                try:
                    profit = round(float(tickers_dict[symbol[1]]) / (float(symbol[6]) / 100) - 100, 1)
                except TypeError:
                    continue
                print('!!!!!!')
                print(symbol)
                print(symbol[3])
                timer = convert(time.time() - float(symbol[7]))
                message = f"""
            Binance
#{currency} Take-Profit target 3 ✅
Profit: {profit}% 📈
Period: {timer} Hours ⏰
                            """
                print(message)
                client.send_message(script_channel, message)
                print('Сообщение отправлено!')
                db.new_none(symbol[1], 3)
                history_db.new_value(symbol[1], 3)

            elif float(tickers_dict[symbol[1]]) >= float(symbol[3]):
                print('yes')
                currency = symbol[1].replace("BTC", "/BTC")
                try:
                    profit = round(float(tickers_dict[symbol[1]]) / (float(symbol[6]) / 100) - 100, 1)
                except TypeError:
                    continue
                print('!!!!!!')
                print(symbol)
                print(symbol[3])
                timer = convert(time.time() - float(symbol[7]))
                message = f"""
            Binance
#{currency} Take-Profit target 2 ✅
Profit: {profit}% 📈
Period: {timer} Hours ⏰
                            """
                print(message)
                client.send_message(script_channel, message)
                print('Сообщение отправлено!')
                db.new_none(symbol[1], 2)
                history_db.new_value(symbol[1], 2)

            elif float(tickers_dict[symbol[1]]) >= float(symbol[2]):
                print('yes')
                currency = symbol[1].replace("BTC", "/BTC")
                try:
                    profit = round(float(tickers_dict[symbol[1]]) / (float(symbol[6]) / 100) - 100, 1)

                except TypeError:
                    continue
                print('!!!!!!')
                print(symbol)
                print(symbol[3])
                timer = convert(time.time() - float(symbol[7]))
                message = f"""
            Binance
#{currency} Take-Profit target 1 ✅
Profit: {profit}% 📈
Period: {timer} Hours ⏰
                            """
                print(message)
                client.send_message(script_channel, message)
                print('Сообщение отправлено!')
                db.new_none(symbol[1], 1)
                history_db.new_value(symbol[1], 1)
        except KeyError:
            continue
        except Exception as e:
            print(e)


if __name__ == '__main__':

    with open("setting.json", 'r', encoding='utf8') as out:

        client = TelegramClient(
            "session_symbol",
            3566267,
            "77c8ec3ad6b760c7d247ef4159721524",
        )

        client.start()

    dialogs = client.get_dialogs()

    for index, dialog in enumerate(dialogs):
        print(f'[{index}] {dialog.name}')

    script_channel = dialogs[int(input("Output script-channel index: "))]

    while True:
        try:
            scan()
            time.sleep(20)
        except Exception as e:
            print(e)
            time.sleep(60)

