import sqlite3
import time


class DataBase:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def register(self, symbol, value):
        with self.connection as con:
            con.execute("INSERT INTO symbols (symbol, price) ""VALUES (?, ?)",
                        (symbol, value))

    def new_value(self, symbol, value):
        with self.connection:
            self.cursor.execute("UPDATE symbols SET price=? WHERE symbol=?", (value, symbol,))

    def get_symbols(self):
        final_dict = {}
        with self.connection:
            row_list = self.cursor.execute("SELECT * FROM symbols").fetchall()
            for i in row_list:
                final_dict[list(i)[1]] = list(i)[2]
            return final_dict

    def check_symbol(self, symbol):
        with self.connection:
            result = self.cursor.execute("SELECT id FROM symbols WHERE symbol=?", (symbol,)).fetchone()

            if result is not None:
                return True
            else:
                return False


if __name__ == '__main__':
    timer = time.time()
    db = DataBase('db.db')

    print(db.get_symbols())
    print(f"Прошло - {time.time() - timer} секунд")
