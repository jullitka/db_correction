from db_wrapper import DatabaseWrapper
from utils import (common_elements, get_first_elements,
                   missing_elements, same_elements)


class DatabaseCorrection:
    """Корректировка бд target_db по бд source_db."""

    def __init__(self, source_db, target_db):
        self.source_db = source_db
        self.target_db = target_db

    def correct_table(self):
        """Корректировка таблиц: добавление новых, удаление старых."""
        # получаем список таблиц из обеих бд
        source_tables = self.source_db.get_tables()
        target_tables = self.target_db.get_tables()
        # сравнивам их
        if not same_elements(source_tables, target_tables):
            # если названия таблиц отличаются, получаем списки отличающихся
            missing_element = missing_elements(target_tables, source_tables)
            # перебираем все таблицы, которых нет в базе target_db
            for element in missing_element[0]:
                # получаем данные о столбцах таблицы (название, тип)
                table_info = self.source_db.get_fields(element)
                # получаем данные из таблицы
                data = self.source_db.get_all_data(element)
                # создаем новую таблицу в бд target_bd
                self.target_db.create_table(element, table_info)
                # добавляем данные в созданную таблицу
                self.target_db.insert_data(element, data)

            for element in missing_element[1]:
                # перебираем все таблицы, которых нет в базе source_db
                self.target_db.drop_table_if_empty(element)

            return 'Таблицы скорректированы'
        return 'Нет таблиц для удаления или добавления'

    def correct_fields(self):
        """Корректировка столбцов: добавление новых, удаление старых"""
        # получаем список таблиц из обеих бд
        source_tables = self.source_db.get_tables()
        target_tables = self.target_db.get_tables()
        # находим таблицы, которые есть в обеих базах
        common_tables = common_elements(source_tables, target_tables)
        # получаем информацию о полях из каждой таблицы
        for table in common_tables:
            source_fields = source_db.get_fields(table)
            target_fields = target_db.get_fields(table)

            if not same_elements(source_fields, target_fields):
                # если в таблицах с одинаковыми названиями есть отличия в полях
                # получаем отличающиеся элементы
                elements = get_first_elements(target_fields, source_fields)
                dif_elements = missing_elements(*elements)

                # добавляем недостающие поля в таблицу target_table
                for field in dif_elements[0]:
                    for source_field in source_fields:
                        if source_field[0] == field:
                            type_field = source_field[1]
                    self.target_db.add_column(table, field, type_field)

                # удаляем поля в target_table, если в них нет данных
                # если данные есть, предупреждаем, что удаление невозможно
                for field in dif_elements[1]:
                    self.target_db.drop_column_if_empty(table, field)
                print(f'Поля таблицы {table} скорректированы')
        return 'Поля скорректированы'

    def correct_primary_key(self):
        """Добавление внешних ключей при необходимости"""
        source_foreign_key = self.source_db.get_all_foreign_keys()
        self.target_db.set_foreign_keys(source_foreign_key)
        return "Ключи скорректированы"

    def correct_data(self):
        """Корректировка бд target_db по бд source_db."""
        self.correct_fields()
        self.correct_table()
        self.correct_primary_key()
        return 'База данных скорректирована'


if __name__ == '__main__':
    source_db = DatabaseWrapper('employees_2.db')
    target_db = DatabaseWrapper('employees_1.db')
    corrector = DatabaseCorrection(source_db, target_db)
    data = corrector.correct_data()
    print(data)
    source_db.close_connection()
    target_db.close_connection()
