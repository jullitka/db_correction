def same_elements(list_1, list_2):
    """Проверяет, содержат ли два списка одинаковые элементы.
    Элементы в каждом из списков различны.
    Возвращает False, если списки различны"""
    if len(list_1) != len(list_2):
        return False
    set_1 = set(list_1)
    set_2 = set(list_2)

    return set_1 == set_2

def missing_elements(list_1, list_2):
    """Находит элементы, которыми отличаются два списка.
    Выводит кортеж: первый элемент - элементы, отсутствующие в первом списке,
    но есть во втором, второй элемент - элементы, отсутствующие во втором списке,
    но есть в первом"""

    set_1 = set(list_1)
    set_2 = set(list_2)

    missing_in_list_1 = set_2 - set_1
    missing_in_list_2 = set_1 - set_2

    return (list(missing_in_list_1), list(missing_in_list_2))
