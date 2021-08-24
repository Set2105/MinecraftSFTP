import paramiko
import os

os.chdir('..')
BASE_DIR = os.getcwd()
print('Workspace: {}'.format(BASE_DIR))

data = load_server_keys('server_keys.json')
ID, API_KEY = data['ID'], data['API_KEY']
SERVER_URL, PORT, SERVER_NAME, PASSWORD = data['URL'], data['PORT'], data['SERVER_NAME'], data['PASSWORD']


def load_server_keys(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def connect_sftp(host, port, user_name, password):
    print('Connecting {}:{} by {} {}'.format(host, port, user_name, password))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,
                   port=port,
                   username=user_name,
                   password=password,
                   look_for_keys=False,
                   allow_agent=False)
    return client, client.open_sftp()


def split_list_dir(lnx_files_list):
    dirs = []
    files = []
    for file in lnx_files_list:
        if '.' in file:
            files.append(file)
        else:
            dirs.append(file)
    return files, dirs


def sftp_upload_dir(local_path, remote_path, sftp_connection):
    list_dir = os.listdir(local_path)  # получение списка файлов
    files, dirs = split_list_dir(list_dir)  # разбиение на файлы и папки

    # заливка файлов
    for file_name in files:
        local_file_path = local_path + '\\' + file_name
        print('Sending {} to {}'.format(local_file_path, remote_path + '/' + file_name))
        sftp_connection.put(local_file_path, remote_path + '/' + file_name)

    # рекурсивый пробег по папкам
    for dir_name in dirs:
        sftp_upload_dir(local_path + '\\' + dir_name,  remote_path + '/' + dir_name, sftp_connection)


SSHClient, sftp_connection = connect_sftp(SERVER_URL, PORT, SERVER_NAME, PASSWORD)
sftp_upload_dir(BASE_DIR + '\\world\\', '/world',  sftp_connection)
sftp_connection.close()
SSHClient.close()
print('Connection closed')
