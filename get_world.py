import paramiko
import os

os.chdir('..')
BASE_DIR = os.getcwd()
print('Workspace: {}'.format(BASE_DIR))

data = load_server_keys('server_keys.json')
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


def sftp_show_dir(path, sftp_connection):
    sftp_connection.chdir(path)
    print('Path: {}\n{}'.format(path, sftp_connection.listdir()))


def split_list_dir(lnx_files_list):
    dirs = []
    files = []
    for file in lnx_files_list:
        if '.' in file:
            files.append(file)
        else:
            dirs.append(file)
    return files, dirs


def sftp_download_dir(remote_path, local_path, sftp_connection):
    sftp_connection.chdir(remote_path)  # переход в дерикторию
    list_dir = sftp_connection.listdir()  # получение списка файлов
    files, dirs = split_list_dir(list_dir)  # разбиение на файлы и папки

    # создаем папку, если она не существует
    if not os.path.exists(local_path):
        os.mkdir(local_path)
    # скачивание файлов
    for file_name in files:
        local_file_path = local_path + '\\' + file_name
        print('Getting {} to {}'.format(remote_path + '/' + file_name, local_file_path))
        sftp_connection.get(file_name, local_file_path)

    # рекурсивый пробег по папкам
    for dir_name in dirs:
        sftp_download_dir(remote_path + '/' + dir_name, local_path + '\\' + dir_name, sftp_connection)


def main():
    ssh_client, sftp_connection = connect_sftp(SERVER_URL, PORT, SERVER_NAME, PASSWORD)
    sftp_download_dir('/world', BASE_DIR + '\\world\\', sftp_connection)
    sftp_connection.close()
    ssh_client.close()
    print('Connection closed')


main()




