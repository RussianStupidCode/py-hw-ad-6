import documentHandler  # как так можно писать ужасный код?
import pytest
# оригинал взят отсюда https://replit.com/@RussianStupidCo/documentHandler#main.py


# чтоб в тестах на изменения случайно не запортить оригинал
def get_documents():
    return [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    ]


def get_directories():
    return {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': []
    }


def compare_directories(expected, actual):
    for exc, act in zip(expected.items(), actual.items()):
        to_string = lambda items: f'{items[0]} {items[1]}'
        expected = to_string(exc)
        actual = to_string(act)
        assert expected == actual


def compare_documents(expected, actual):
    for exc, act in zip(expected, actual):
        to_string = lambda items: "_".join("-".join([" ".join(i) for i in items]))
        expected = to_string(exc.items())
        actual = to_string(act.items())
        assert expected == actual


@pytest.mark.get_name_owner
def test_not_find_owner():
    try:
        documentHandler.get_name_owner('11-22', get_documents())
    except ValueError as er:
        assert f'Нет документа с таким номером 11-22' == str(er)


@pytest.mark.get_name_owner
def test_find_owner():
    assert "Геннадий Покемонов" == documentHandler.get_name_owner('11-2', get_documents())


@pytest.mark.is_document_available
def test_doc_not_available():
    assert not documentHandler.is_document_available('11-22', get_documents())


@pytest.mark.is_document_available
def test_doc_available():
    assert documentHandler.is_document_available('11-2', get_documents())


@pytest.mark.get_shelf_number
def test_not_shelf_find():
    try:
        documentHandler.get_shelf_number('5522', get_directories())
    except ValueError as er:
        assert 'Нет документа с таким номером 5522' == str(er)


@pytest.mark.get_shelf_number
def test_shelf_find():
    assert '2' == documentHandler.get_shelf_number('10006', get_directories())


@pytest.mark.document_index
def test_find_doc_index():
    assert 1 == documentHandler.document_index('11-2', get_documents())


@pytest.mark.document_index
def test_not_find_doc_index():
    try:
        documentHandler.document_index('5522', get_documents())
    except ValueError as er:
        assert 'Нет документа с таким номером 5522' == str(er)


@pytest.mark.show_all_documents
def test_show_documents():
    assert 'passport 2207 876234 Василий Гупкин\n' \
           'invoice 11-2 Геннадий Покемонов\n' \
           'insurance 10006 Аристарх Павлов' == documentHandler.show_all_documents(get_documents())


@pytest.mark.add_document
def test_correct_add_document():
    documents = get_documents()
    directories = get_directories()
    documentHandler.add_document({"type": "passport", "number": "666", "name": "Патриарх Кирилл"},
                                 '3', documents, directories)

    expected_documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        {"type": "passport", "number": "666", "name": "Патриарх Кирилл"}
    ]

    expected_directories = {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': ['666']
    }

    compare_documents(expected_documents, documents)
    compare_directories(expected_directories, directories)


@pytest.mark.add_document
def test_not_exist_shelf():
    documents = get_documents()
    directories = get_directories()
    try:
        documentHandler.add_document({"type": "passport", "number": "666", "name": "Патриарх Кирилл"},
                                     '3', documents, directories)
    except ValueError as er:
        assert f'Несуществующий номер полки 3' == str(er)


@pytest.mark.add_document
def test_exist_doc():
    documents = get_documents()
    directories = get_directories()
    try:
        documentHandler.add_document({"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
                                     '3', documents, directories)
    except ValueError as er:
        assert 'Документ с таким номером существует' == str(er)


@pytest.mark.delete_document_in_shelf
def test_uncorrect_shelf():
    try:
        documentHandler.delete_document_in_shelf('11-2', '0', get_directories())
    except KeyError as er:
        assert str(er) == str(KeyError('0'))


@pytest.mark.delete_document_in_shelf
def test_not_find_doc_in_shelf():
    directories = get_directories()
    documentHandler.delete_document_in_shelf('11-22', '1', directories)

    expected_directories = {
        '1': ['2207 876234', '11-2'],
        '2': ['10006'],
        '3': []
    }

    compare_directories(expected_directories, directories)


@pytest.mark.delete_document_in_shelf
def test_delete_doc_in_shelf():
    directories = get_directories()
    documentHandler.delete_document_in_shelf('11-2', '1', directories)

    expected_directories = {
        '1': ['2207 876234'],
        '2': ['10006'],
        '3': []
    }

    compare_directories(expected_directories, directories)


@pytest.mark.delete_document
def test_not_find_document():
    try:
        documentHandler.delete_document('0', get_documents(), get_directories())
    except ValueError as er:
        assert 'Нет документа с таким номером 0' == str(er)


@pytest.mark.delete_document
def test_delete_document():
    documents = get_documents()
    directories = get_directories()
    documentHandler.delete_document('11-2', documents, directories)

    expected_documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    ]
    compare_documents(expected_documents, documents)

    expected_directories = {
        '1': ['2207 876234'],
        '2': ['10006'],
        '3': []
    }
    compare_directories(expected_directories, directories)
