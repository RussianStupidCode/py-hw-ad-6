import requests
BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
TOKEN = ''
try:
    import my_token
    TOKEN = my_token.TOKEN
except ImportError:
    pass


def make_directory(dir_path, token=TOKEN):
    """Создание дирректории на я.диске"""

    dir_path = dir_path.strip().strip("/")
    params = {'path': dir_path}
    resp = requests.put(f'{BASE_URL}/resources', headers={'Authorization': token}, params=params)

    text = resp.json()
    if resp.status_code != 201 and text['message'] != 'Директория с таким именем уже существует':
        raise ValueError(text['message'])
    return 'Директория создана успешно'


def is_dir_exist(dir_path,token=TOKEN):
    params = {'path': 'dir_path'}
    resp = requests.get(f'{BASE_URL}/resources', headers={'Authorization': token}, params=params)
    if resp.status_code != 200:
        return False
    return True
