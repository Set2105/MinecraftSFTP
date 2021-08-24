import requests

data = load_server_keys('server_keys.json')
ID, API_KEY = data['ID'], data['API_KEY']


def load_server_keys(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def show_server_attributes(id, API_key):
    response = requests.get(
        'https://mgr.hosting-minecraft.ru/api/client/servers/{}'.format(id),
        headers={
            'Authorization': 'Bearer {}'.format(API_key),
            'Content-Type': 'application / json',
            'Accept': 'Application / vnd.pterodactyl.v1 + json'
                }
    )

    server_attributes = response.json()["attributes"]
    for attribute in server_attributes:
        print('{}: {}'.format(attribute, server_attributes[attribute]))
    return 0


def send_command(id, API_key, command):
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


def send_signal(id, API_key, signal):
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


def show_request(request_obj):
    for line in request_obj:
        print(line)


send_signal(ID, API_KEY, 'restart')







