import sqlite3


class DatabaseWrapper:
    """Обертка для базы данных SQLite."""

    def __init__(self, db):
        self.db = db

    def get_tables(self):
        """Получаем список всех таблиц из бд."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        conn.close()
        return [table[0] for table in tables]

    def get_fields(self, table):
        """Получаем списко всех полей из таблицы table в бд."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info('{table}')".format(table))
        fields = cur.fetchall()
        conn.close()
        return [field[1] for field in fields]

    def create_table(self, table_name, columns):
        """Добавляем новую таблицу table_name в бд
        с полями из списка columns."""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        columns_str = ", ".join(columns)
        cur.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(
            table_name, columns_str
        ))
        conn.commit()
        conn.close()

    def drop_table_if_empty(self, table_name):
        """Удаляем таблицу table_name из бд в случае, если в ней нет данных.
        Если в таблице хранятся данные, сообщаем,
        что она не может быть удалена"""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM {}".format(table_name))
        result = cur.fetchone()[0]

        if result == 0:
            cur.execute("DROP TABLE {}".format(table_name))
            conn.commit()
        else:
            return f"Таблица {table_name} содержит данные и не может быть удалена"

        conn.close()

    def add_column(self, table, column_name, column_type):
        """Добавляем дополнительное поле с именем column_name
        типа column_type в таблицу table."""

        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("ALTER TABLE {} ADD COLUMN {} {}".format(
            table, column_name, column_type
        ))
        conn.commit()
        conn.close()

    def drop_column_if_empty(self, table_name, column_name):
        """Удаляем поле column_name в таблице table_name,
        если оно не содержит данных.
        Если поле содержит данные, то сообщаем,
        что оно не может быть удалено."""

        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(f'SELECT {column_name} FROM {table_name}')
        if not cur.fetchone():
            cur.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
            conn.commit()
        else:
            return f"Столбец {column_name} в таблице {table_name} содержит данные, он не может быть удален"
        conn.close()


