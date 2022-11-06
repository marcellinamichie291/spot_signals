import sqlite3
import time


class DataBase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def register(self, symbol, target_1, target_2, target_3, target_4, start_value, date):
        with self.connection as con:
            con.execute("INSERT INTO symbols (symbol, target_1, target_2, target_3, target_4, date, start_value)"
                        " ""VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (symbol, target_1, target_2, target_3, target_4, date, start_value))

    def new_value(self, symbol, target_1, target_2, target_3, target_4, start_value, date):
        with self.connection:
            self.cursor.execute("UPDATE symbols SET target_1=? WHERE symbol=?", (target_1, symbol,))
            self.cursor.execute("UPDATE symbols SET target_2=? WHERE symbol=?", (target_2, symbol,))
            self.cursor.execute("UPDATE symbols SET target_3=? WHERE symbol=?", (target_3, symbol,))
            self.cursor.execute("UPDATE symbols SET target_4=? WHERE symbol=?", (target_4, symbol,))
            self.cursor.execute("UPDATE symbols SET date=? WHERE symbol=?", (date, symbol,))
            self.cursor.execute("UPDATE symbols SET start_value=? WHERE symbol=?", (start_value, symbol,))

    def new_none(self, symbol, number):
        with self.connection:
            self.cursor.execute(f"UPDATE symbols SET target_{number}=? WHERE symbol=?", (None, symbol,))

    def get_symbols(self):
        final_list = []
        with self.connection:
            row_list = self.cursor.execute("SELECT * FROM symbols WHERE target_4<>'None'").fetchall()
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

    def check_complete(self, symbol):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM symbols WHERE symbol=? AND target_4='None'", (symbol,)
                                         ).fetchone()

            if result is not None:
                return True
            else:
                return False


if __name__ == '__main__':
    timer = time.time()
    db = DataBase('current_signals.db')
    print(db.check_complete('CRVBTC'))
    # print(db.get_symbols())
    # db.new_none('BCDBTC', 1)
    # print(db.register('QLCBTC', str("%.16f" % round(float('0.0000002')/100*103, 10)).rstrip('0'), '0.00000085',
    # time.time()))
    print(f"Прошло - {time.time() - timer} секунд")
