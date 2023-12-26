import sqlite3

from db_wrapper import DatabaseWrapper
from utils import same_elements, missing_elements

class DatabaseCorrection:

    def __init__(self, source_db, target_db):
        self.source_db = source_db
        self.target_db = target_db

    def correct_data(self):

        source_tables = self.source_db.get_tables()
        target_tables = self.target_db.get_tables()

        if not same_elements(source_tables, target_tables):
            print(missing_elements(source_tables, target_tables))

        for table in source_tables:
            if table in target_tables:
                source_fields = self.source_db.get_fields(table)
                target_fields = self.target_db.get_fields(table)


            else:
                # Если таблица отсутствует во второй базе, вы можете решить, что делать в этом случае
                # Например, создать новую таблицу во второй базе, скопировав структуру и данные из первой
                self.target_db.create_table_like(source_table, target_table)

        # Возвращайте информацию о выполненных коррекциях
        return "Данные скорректированы успешно"


source_db = DatabaseWrapper('employees_1.db')
target_db = DatabaseWrapper('employees_2.db')
corrector = DatabaseCorrection(source_db, target_db)
data = corrector.correct_data()
print(data)
