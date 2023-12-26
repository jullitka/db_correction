import sqlite3


class DatabaseWrapper:
    def __init__(self, db):
        self.db = db

    def get_tables(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        conn.close()
        return [table[0] for table in tables]

    def get_fields(self, table):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info('{}')".format(table))
        fields = cur.fetchall()
        conn.close()
        return [field[1] for field in fields]

    def create_table_like(self, source_table, target_table):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS {} AS SELECT * FROM {}".format(
                target_table, source_table
            )
        )
        conn.commit()
        conn.close()


source_db = DatabaseWrapper('employees_1.db')
target_db = DatabaseWrapper('employees_2.db')

print(source_db.get_tables())
print(source_db.get_fields('employees'))

print(target_db.get_tables())
print(target_db.get_fields('employees'))
