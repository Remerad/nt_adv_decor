import datetime

mn_log_file_name = 'log_file.txt'


def make_trace_in_definite_log_file(log_file_name):

    def make_trace(func):

        def log_function_called(*args, **kwargs):
            result = func(*args, **kwargs)
            temp_str = (f'{datetime.datetime.now()} Вызвана функция {func.__name__} '
                  f'с аргументами {args} {kwargs}, которая вернула значение {result}')
            print(temp_str)
            with open(log_file_name, 'w') as lf:
                lf.write(temp_str)

        return log_function_called

    return make_trace


class CookBook:
    def __init__(self):
        self.cook_book = {}

    @make_trace_in_definite_log_file(mn_log_file_name)
    #@make_trace
    def read_cook_book_file(self, cook_book_file_name):
        temp_dish_name = ""
        temp_dish_components = []
        with open(cook_book_file_name, 'r', encoding='utf-8') as f:
            my_lines = list(f)
            for i in my_lines:
                temp_str = i.strip()
                if not temp_str.isdigit():
                    temp_list = temp_str.split(" | ")
                    if len(temp_list) == 1 and temp_list[0] != '':
                        temp_dish_name = temp_list[0]
                        temp_dish_components = []
                    elif len(temp_list) > 1:
                        temp_dish_components.append({'ingredient_name': temp_list[0],
                                                     'quantity': int(temp_list[1]),
                                                     'measure': temp_list[2]})
                    elif len(temp_list) == 1 and temp_list[0] == '':
                        self.cook_book.update({temp_dish_name: temp_dish_components})
            self.cook_book.update({temp_dish_name: temp_dish_components})
        return 0


    def get_shop_list_by_dishes(self, dishes, person_count):
        dishes_components_list = {}
        for dish in dishes:
            if dish in self.cook_book:
                for component in self.cook_book[dish]:
                    if component['ingredient_name'] not in dishes_components_list:
                        dishes_components_list.update({component['ingredient_name']:
                                                           {'measure': component['measure'],
                                                            'quantity': component['quantity'] * person_count}})
                    else:
                        q = dishes_components_list.get(component['ingredient_name'])['quantity'] \
                            + component['quantity'] * person_count
                        dishes_components_list.update({component['ingredient_name']:
                                                           {'measure': component['measure'],
                                                            'quantity': q}})
        return dishes_components_list


if __name__ == '__main__':
    print(f'Текущий путь к файлу логов: {mn_log_file_name}')
    x = input('Нажмите Enter, если Вас устраивает этот путь, либо введите новый:')
    if x != '':
        print(x)
        mn_log_file_name = x

    CB = CookBook()
    CB.read_cook_book_file(cook_book_file_name='recipes.txt')

    shop_list = CB.get_shop_list_by_dishes(["Омлет", "Фахитос"], 4)
    for i in shop_list:
        print(f"{i}, {shop_list[i]['quantity']} {shop_list[i]['measure']}")