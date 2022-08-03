import copy


def create_cook_book(recipes_file):
    """Функция чтения файла рецептов и записи их в словарь.

       Используюется для реализации Задачи №1"""

    recipes_dict = {}
    with open(recipes_file, 'rt', encoding='utf-8') as recipes:
        line = recipes.readline()
        if line == '\n' or line == '' or not line:
            print('Ошибка структуры файла рецептов. '
                  'Работа программы завершена.')
            return
        else:
            position = 1111  # Указатель на строку в рамках рецепта.
            # 1111 это указатель на название блюда
            while True:
                if not line:
                    break

                if line == '\n' or line == '':
                    position = 1111  # Один рецепт закончился, начинается след
                    line = recipes.readline()

                if position == 1111:
                    dish = line.strip()
                    recipes_dict[dish] = []
                    position = 1112  # Перемещаем указатель на вторую строку
                    # рецепта - количество ингридиентов

                elif position == 1112:
                    line = recipes.readline()
                    position = int(line)

                else:
                    line = recipes.readline()
                    if position > 0:
                        ingredient_list = line.split(' | ')
                        ingredient_dict = {}
                        for ingredient in ingredient_list:
                            index = ingredient_list.index(ingredient)
                            if index == 0:
                                ingredient_dict['ingredient_name'] = ingredient
                            elif index == 1:
                                ingredient_dict['quantity'] = ingredient
                            else:
                                ingredient_dict['measure'] = ingredient.strip()
                        recipes_dict[dish].append(ingredient_dict)
                    position -= 1

    return recipes_dict


def get_shop_list_by_dishes(dishes, person_count):
    """Функция для формирования списка покупок.

       На вход функция принимает список блюд и количество персон,
       на которых готовится обед. На выходе получается словарь с названием
       ингредиентов и их количестом для заданного списка блюд."""

    ingridients_quantity = {}
    for dish, ingredients in dishes.items():
        for ingredient in ingredients:
            if ingredient['ingredient_name'] not in ingridients_quantity:
                ingridients_quantity[ingredient['ingredient_name']] = {}
                (ingridients_quantity[ingredient['ingredient_name']]
                 ['measure']) = ingredient['measure']
                (ingridients_quantity[ingredient['ingredient_name']]
                 ['quantity']) = int(ingredient['quantity']) * person_count
            else:
                (ingridients_quantity[ingredient['ingredient_name']]
                 ['quantity']) += int(ingredient['quantity']) * person_count
    return ingridients_quantity


def count_sort_print(file_list):
    """Функция для расчета количества строк в файлах

    :param file_list: список названий файлов для обработкию
    :return: словарь, ключ - имя файла, значение - количество строк в файлею
    Файлы в словарь записываются в порядке возрастания количества строк в них.
    """

    # Сначала создаем временный словарь с "файл - количество строк"
    temp_file_dict = {}
    for file_name in file_list:
        line_quantity = 0  # Счетчик количества строк в файле
        with open(file_name, 'rt', encoding='utf-8') as file:
            line = file.readline()
            while True:
                if not line:
                    break
                else:
                    line_quantity += 1
                    line = file.readline()
            temp_file_dict[file_name] = line_quantity
    print()

    # Создаем словарь, отсортированный по значению
    sorted_temp_file_list = sorted(temp_file_dict.values())
    file_dict = {}
    for value in sorted_temp_file_list:
        for file in temp_file_dict.keys():
            if temp_file_dict[file] == value:
                file_dict[file] = temp_file_dict[file]

    # Печатаем результат согласно условию задания №3
    for file_name, lines_quantity in file_dict.items():
        print(file_name)
        print(lines_quantity)
        with open(file_name, 'rt', encoding='utf-8') as file:
            line = file.readline().strip()
            while True:
                if not line:
                    break
                else:
                    print(line)
                    line = file.readline().strip()

    return


def task_1_2():
    """Фукция реализующая подготовительные работы по задачам 1 и 2

    :return: нет"""

    # Задание №1 - чтение списка рецептов из файла и запись их в словарь
    print()
    print('Задание №1 - чтение списка рецептов из файла и запись их в словарь')
    print()
    recipes_dict = create_cook_book('recipes.txt')
    dish_number = 1
    for dish, ingredients in recipes_dict.items():
        print(dish_number, '. ', dish, ':')
        dish_number += 1
        for ingredient in ingredients:
            print(' ', ingredient)
    print()
    input('Нажмите Enter для продолжения ')
    print()

    # Задание №2 - на входе блюда и кол-во персон,
    # на выходе - количество ингредиентов
    print('Задание №2 - Расчет ингредиентов на заданное количество персон')
    print()
    dish_string = input('Введите через запятую номера блюд из списка выше: ')

    # Удаляем проблелы из полученной строки, если пользователь их ввел:
    dish_string_replaced = dish_string.replace(' ', '')

    # Формируем список из номеров по разделителю - запятой:
    dish_string_splited = dish_string_replaced.split(',')

    # Создаем список для хранения "чистых" номеров блюд:
    dish_numbers = []
    for dish_string in dish_string_splited:
        try:
            number = int(dish_string)
            dish_numbers.append(number)
        except:
            print()
            print('Неверный формат ввода блюд.')
            exit()

    # Проверяем введенные номера на существование в списке блюд:
    dish_numbers_clone = copy.deepcopy(dish_numbers)
    flag_error = 0
    for number in dish_numbers:
        if number > len(recipes_dict):
            print(f'Номер {number} отсутствует в книге рецептов. ')
            flag_error = 1
        dish_numbers_clone.remove(number)

    if len(dish_numbers_clone) > 0:
        print(f'Номер(а) {dish_numbers_clone} введен(ы) более 1 раза. ')
        flag_error = 1

    if flag_error == 1:
        print('Необходимо повторить ввод.')
        exit()
    # Если с вводом номеров блюд ОК, вводим кол-во персон
    else:
        flag_error = 1
        while flag_error == 1:
            try:
                person_count = int(input('Введите количество персон: '))
                flag_error = 0
            except:
                print('Неверный формат ввода персон')
                flag_error = 1

    # Формирование укороченного списка блюд - только заказанные выше
    dishes = {}
    i = 1
    for dish, ingredient in recipes_dict.items():
        if i in dish_numbers:
            dishes[dish] = ingredient
        i += 1

    # Вызов функции, рассчитывающей количество ингиридентов для приготовления
    # заданных блюд
    ingridients_quantity_dict = get_shop_list_by_dishes(dishes, person_count)
    print()
    print('Ингриденты и их кол-во для приготовления заданных блюд (', end='')
    i = 1
    for key in dishes.keys():
        if i < len(dishes):
            print(key, end=',')
        else:
            print(key, end='):')
        i += 1
    print()
    i = 1
    for ingridient, quantity in ingridients_quantity_dict.items():
        if i < len(ingridients_quantity_dict):
            print(f'{ingridient}: {quantity},')
        else:
            print(f'{ingridient}: {quantity}')
        i += 1
    print()
    input('Нажмите Enter для продолжения ')

    return


while True:
    print()
    print('1. Расчет количества ингредиентов (Задачи N 1-2)')
    print('2. Объединение файлов (Задача N 3)')
    print('3. Завершение работы')
    print()
    error = 1
    while error == 1:
        try:
            choise = int(input('Введите номер пункта: '))
        except:
            print()
            print('Неверный формат ввода номера пункта.')
            continue
        if choise < 1 or choise > 3:
            print('Неверный номер пункта.')
            continue
        error = 0

    if choise == 1:
        task_1_2()
    elif choise == 2:
        # Задание №3 - объединение файлов
        print('Задание №3 - объединение файлов')
        print()
        file_list = ['first.txt', 'second.txt', 'fourth.txt', 'third.txt']
        count_sort_print(file_list)
        print()
        input('Нажмите Enter для продолжения ')
    else:
        exit()
