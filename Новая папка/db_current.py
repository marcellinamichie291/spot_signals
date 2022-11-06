import sqlite3
import time


class DataBase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def register(self, symbol, value, start_value, date):
        with self.connection as con:
            con.execute("INSERT INTO symbols (symbol, value, date, start_value) ""VALUES (?, ?, ?, ?)", (symbol, value, date, start_value))

    def new_value(self, symbol, value, start_value, date):
        with self.connection:
            self.cursor.execute("UPDATE symbols SET value=? WHERE symbol=?", (value, symbol,))
            self.cursor.execute("UPDATE symbols SET date=? WHERE symbol=?", (date, symbol,))
            self.cursor.execute("UPDATE symbols SET start_value=? WHERE symbol=?", (start_value, symbol,))

    def get_symbols(self):
        final_list = []
        with self.connection:
            row_list = self.cursor.execute("SELECT * FROM symbols WHERE value<>'None'").fetchall()
            for i in row_list:
                final_list.append(list(i))
            return final_list

    def check_symbol(self, symbol):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM symbols WHERE symbol=?", (symbol,)).fetchone()

            if result is not None:
                return True
            else:
                return False


if __name__ == '__main__':
    timer = time.time()
    db = DataBase('binance.db')

    print(db.new_value('QLCBTC', '0.00000093', '0.00000085', time.time()))
    print(f"Прошло - {time.time() - timer} секунд")
