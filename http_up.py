import requests
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


sleep(5)
send_signal(ID, API_KEY, 'start')
