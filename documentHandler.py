import sys

documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def my_help():
    '''
    Список комманд:
      p – команда спросит номер документа и выведет имя человека, которому он принадлежит.
      s – команда спросит номер документа и выведет номер полки, на которой он находится.
      l – команда выведет список всех документов в формате passport "2207 876234" "Василий Гупкин".
      a – команда добавит новый документ в каталог и в перечень полок, спросив его номер,
          тип, имя владельца и номер полки, на котором он будет храниться.
      d – команда спросит номер документа и удалит его из каталога и из перечня полок.
      m – команда спросит номер документа и целевую полку и переместит его с текущей полки на целевую.
      as - команда спросит номер новой полки и добавит ее в перечень
      exit - выход
    '''
    pass


def get_name_owner(doc_number: str, documents=documents):
    for document in documents:
        if document['number'] == doc_number:
            return document['name']
    raise ValueError(f'Нет документа с таким номером {doc_number}')


def is_document_available(doc_number: str, documents=documents):
    try:
        get_name_owner(doc_number)
        return True
    except:
        return False


def get_shelf_number(document_number: str, directories=directories):
    for shelf, document_numbers in directories.items():
        if document_number in document_numbers:
            return shelf
    raise ValueError(f'Нет документа с таким номером {document_number}')


def document_index(document_number: str, documents=documents):
    for index, document in enumerate(documents):
        if document['number'] == document_number:
            return index
    raise ValueError(f'Нет документа с таким номером {document_number}')


def show_all_documents(documents=documents):
    lines = []
    for document in documents:
        out_line = " ".join(list(document.values()))
        lines.append(out_line)
    return "\n".join(lines)


def add_document(document, shelf_number: str, documents=documents, directories=directories):
    if shelf_number not in directories:
        raise ValueError(f'Несуществующий номер полки {shelf_number}')

    document_number = document['number']
    if is_document_available(document_number):
        raise ValueError(f'Документ с таким номером существует')

    documents.append(document)
    directories[shelf_number].append(document['number'])


def delete_document_in_shelf(document_number: str, shelf_number: str, directories=directories):
    shelf = directories[shelf_number]
    if document_number in shelf:
        shelf.remove(document_number)


def delete_document(document_number: str, documents=documents, directories=directories):
    shelf_number = get_shelf_number(document_number, directories)
    delete_document_in_shelf(document_number, shelf_number, directories)

    doc_index = document_index(document_number)
    documents.pop(doc_index)


def move_document(document_number: str, new_shelf: str, documents=documents, directories=directories):
    old_shelf = get_shelf_number(document_number)
    if old_shelf == new_shelf:
        return

    if new_shelf not in directories:
        raise ValueError(f'Нет такой полки{new_shelf}')

    delete_document_in_shelf(document_number, old_shelf)
    directories[new_shelf].append(document_number)


def add_shelf(new_shelf: str, directories=directories):
    if new_shelf in directories:
        return
    directories[new_shelf] = []


def document_list(documents=documents):
    if len(documents) == 0:
        return 'Список документов пуст'

    return f'Список всех документов:\n {show_all_documents(documents)}'


def people_command():
    document_number = input('Введите номер документа: ')
    document_owner = get_name_owner(document_number)
    print(f'{document_owner}\n')


def add_command():
    document_number = input('Введите номер документа: ')
    document_type = input('Введите тип документа: ')
    document_owner = input('Введите имя владельца: ')
    shelf_number = input('Введите номер полки: ')

    document = {'type': document_type,
                'number': document_number,
                'name': document_owner
                }

    for key, value in document.items():
        if len(value) < 1:
            raise ValueError(f'Пустое значение поля документа {key}: {value}')

    add_document(document, shelf_number)


def delete_command():
    document_number = input('Введите номер документа: ')
    delete_document(document_number)
    print()


def shelf_command():
    document_number = input('Введите номер документа: ')
    shelf_number = get_shelf_number(document_number)
    print(f'Номер полки документа {shelf_number}')


def move_command():
    document_number = input('Введите номер документа: ')
    shelf_number = input('Введите номер новой полки: ')
    move_document(document_number, shelf_number)
    print()


def add_shelf_command():
    shelf_number = input('Введите номер новой полки: ')
    add_shelf(shelf_number)
    print()


def command_handler():
    input_line = input('Введите команду: ').split()
    if len(input_line) < 1:
        return

    command = input_line[0].lower()

    if command == 'help':
        help(my_help)

    elif command == 'l':
        print(document_list())

    elif command == 'exit':
        sys.exit()

    elif command == 'p':
        people_command()

    elif command == 'a':
        add_command()

    elif command == 'd':
        delete_command()

    elif command == 's':
        shelf_command()

    elif command == 'm':
        move_command()

    elif command == 'as':
        add_shelf_command()

    else:
        print('Неверная комманда. Введите help\n')

    return False


if __name__ == '__main__':
    while True:
        try:
            command_handler()
        except ValueError as error:
            print(f'{error}\n')
