import sqlite3
import time
import datetime

str_1 = 'UPDATE symbols SET target_1=? WHERE id = (SELECT id FROM symbols WHERE symbol=? ORDER BY id DESC LIMIT 1)'
str_2 = 'UPDATE symbols SET target_2=? WHERE id = (SELECT id FROM symbols WHERE symbol=? ORDER BY id DESC LIMIT 1)'
str_3 = 'UPDATE symbols SET target_3=? WHERE id = (SELECT id FROM symbols WHERE symbol=? ORDER BY id DESC LIMIT 1)'
str_4 = 'UPDATE symbols SET target_4=? WHERE id = (SELECT id FROM symbols WHERE symbol=? ORDER BY id DESC LIMIT 1)'


class DataBase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def register(self, symbol):
        with self.connection as con:
            con.execute("INSERT INTO symbols (symbol) ""VALUES (?)",
                        (symbol,))

    def new_value(self, symbol, number_target):
        now = datetime.datetime.now()
        str_date = str(now.strftime("%d-%m-%Y %H:%M"))
        with self.connection:
            if number_target == 1:
                self.cursor.execute(str_1, (str_date, symbol,))
            elif number_target == 2:
                self.cursor.execute(str_2, (str_date, symbol,))
            elif number_target == 3:
                self.cursor.execute(str_3, (str_date, symbol,))
            elif number_target == 4:
                self.cursor.execute(str_4, (str_date, symbol,))

    def check_symbol(self, symbol):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM symbols WHERE symbol=?", (symbol,)).fetchone()

            if result is not None:
                return True
            else:
                return False


if __name__ == '__main__':
    timer = time.time()
    db = DataBase('history.db')

    print(db.new_value('TEST', 4))
    print(f"Прошло - {time.time() - timer} секунд")
