import sqlite3


class DatabaseWrapper:
    """Обертка для базы данных SQLite."""

    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def close_connection(self):
        """Закрываем соединение с бд."""
        self.conn.close()

    def get_tables(self):
        """Получаем список всех таблиц из бд."""
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()
        return [table[0] for table in tables]

    def get_fields(self, table):
        """Получаем списко всех полей и информацию о них
        из таблицы table в бд."""
        self.cur.execute(f"PRAGMA table_info('{table}')")
        fields = self.cur.fetchall()
        fields_without_id = [field[1:] for field in fields]
        return fields_without_id

    def get_foreign_keys_info(self, table_name):
        """Получаем информацию о внешних ключах таблицы."""
        self.cur.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys_info = self.cur.fetchall()
        return [(item[2], item[3], item[4]) for item in foreign_keys_info]

    def create_table(self, table_name, fields, foreign_keys=None):
        """Добавляем новую таблицу table_name в бд
        с полями из списка fields и внешними ключами foreign_keys."""
        columns_str = ", ".join(
            [f"{field[0]} {field[1]} NOT NULL" if field[4] == 1
             else f"{field[0]} {field[1]}" for field in fields]
        )
        if foreign_keys is not None:
            foreign_keys_str = ", ".join(
                [f"""FOREIGN KEY ({key_info[1]}) REFERENCES
                 {key_info[0]}({key_info[2]})""" for key_info in foreign_keys]
            )
            self.cur.execute(
                f"""CREATE TABLE IF NOT EXISTS
                {table_name} ({columns_str}, {foreign_keys_str})"""
            )
        else:
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
            )
        self.conn.commit()

    def drop_table_if_empty(self, table_name):
        """Удаляем таблицу table_name из бд в случае, если в ней нет данных.
        Если в таблице хранятся данные, сообщаем,
        что она не может быть удалена"""
        self.cur.execute("SELECT count(*) FROM {}".format(table_name))
        result = self.cur.fetchone()[0]

        if result == 0:
            self.cur.execute("DROP TABLE {}".format(table_name))
            self.conn.commit()
        else:
            print(f"""Таблица {table_name}
                  содержит данные и не может быть удалена""")
            return f"""Таблица {table_name}
                    содержит данные и не может быть удалена"""

    def add_column(self, table, column_name, column_type):
        """Добавляем дополнительное поле с именем column_name
        типа column_type в таблицу table."""
        self.cur.execute("ALTER TABLE {} ADD COLUMN {} {}".format(
            table, column_name, column_type
        ))
        self.conn.commit()

    def drop_column_if_empty(self, table_name, column_name):
        """Удаляем поле column_name в таблице table_name,
        если оно не содержит данных.
        Если поле содержит данные, то сообщаем,
        что оно не может быть удалено."""
        self.cur.execute(f'SELECT {column_name} FROM {table_name}')
        if not self.cur.fetchone():
            self.cur.execute(f"""ALTER TABLE {table_name}
                             DROP COLUMN {column_name}""")
            self.conn.commit()
        else:
            print(f"""Столбец {column_name} в таблице {table_name}
                   содержит данные, он не может быть удален""")
            return f"""Столбец {column_name} в таблице {table_name}
                    содержит данные, он не может быть удален"""

    def get_all_data(self, table):
        """Собираем все данные из таблицы table."""
        self.cur.execute(f'PRAGMA table_info({table})')
        columns = [column[1] for column in self.cur.fetchall()]
        self.cur.execute(f"SELECT * FROM {table}")
        data = self.cur.fetchall()

        result = []
        for row in data:
            row_data = dict(zip(columns, row))
            result.append(row_data)
        return result

    def insert_data(self, table, data):
        """Добавляем данные в таблицу table."""
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join('?'*len(data[0]))
        for row in data:
            values = tuple(row.values())
            self.cur.execute(
                f"""INSERT INTO {table} ({columns})
                 VALUES ({placeholders})""", values
            )
        self.conn.commit()
