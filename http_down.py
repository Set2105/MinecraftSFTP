import requests
import json
from time import sleep


data = load_server_keys('server_keys.json')
ID, API_KEY = data['ID'], data['API_KEY']


def load_server_keys(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def send_signal(id, API_key, signal):
    print('sending signal: {}'.format(signal))
    response = requests.post(
        'https://mgr.hosting-minecraft.ru/api/client/servers/{}/power'.format(id),
        headers={
            'Authorization': 'Bearer {}'.format(API_key),
            'Content-Type': 'application / json',
            'Accept': 'Application / vnd.pterodactyl.v1 + json'
                },
        # data='\"{}\": \"{}\"'.format('command', 'say test api')
        params={"signal": "{}".format(signal)}
    )
    return response


def send_command(id, API_key, command):
    print('executing command: {}'.format(command))
    response = requests.post(
        'https://mgr.hosting-minecraft.ru/api/client/servers/{}/command'.format(id),
        headers={
            'Authorization': 'Bearer {}'.format(API_key),
            'Content-Type': 'application / json',
            'Accept': 'Application / vnd.pterodactyl.v1 + json'
                },
        params={"command": "{}".format(command)}
    )
    return response


send_command(ID, API_KEY, 'say Идет выключение сервера')
send_command(ID, API_KEY, 'say После выключения сервер будет доступен на 83.167.103.151:25565 через несколько минут')
for i in range(2):
    send_command(ID, API_KEY, 'say Осталось {} сек'.format((3 - i)*10))
    sleep(10)
for i in range(10):
    sleep(1)
    send_command(ID, API_KEY, 'say Осталось {} сек'.format(10 - i))
send_command(ID, API_KEY, 'say Выключение'.format(10 - i))
send_signal(ID, API_KEY, 'stop')
sleep(5)
