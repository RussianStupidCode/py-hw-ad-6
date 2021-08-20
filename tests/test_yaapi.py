import yaapi


def test_unauthorize():
    try:
        expected = yaapi.make_directory('new_dir', 'fgdfgdfg')
    except ValueError as er:
        assert 'Не авторизован.' == str(er)


def test_new_dir():
    expected = yaapi.make_directory('new_dir')
    assert 'Директория создана успешно' == expected
    assert yaapi.is_dir_exist('new_dir')


def test_error_path():
    try:
        expected = yaapi.make_directory('/qqq/new_dir')
    except ValueError as er:
        assert 'Указанного пути "qqq/new_dir" не существует.' == str(er)