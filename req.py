#!/usr/bin/env python3

import gitlab
import os
from sys import exit
import yaml
import pprint


# Теперь эти настройки лежат в '/etc/gbkpy/config.yaml'
# Вам нужно получить токен доступа в ваш локальный gitlab с правами:
# read_api, read_user, read_repository, read_registry, read_service_ping
# private_token = ''
# Ссылка на gitlab
# gitlab_instance = ''

# Расположение файла конфигурации
config_file = '/etc/gbkpy/config.yaml'
# Название файла для хранения ссылок на репозитории
repos_list = 'repos.yaml'

def read_config(config_file=config_file):
    result = None
    try:
       with open(config_file, 'r') as file:
           result = yaml.safe_load(file)
    except:
       print("Что-то пошло не так или файла конфигурации не существует!")
    return result


def repos_update(output):
    # сформируем файл репозиториев заново, чтобы не потерять новые
    # репозитории и ветки, а старые не затереть
    data = {}

    # Считываем список сайтов и их подробности, формируем общий список
    # репозиториев и их веток
    for gitlab_instance, details in read_config().items():
        try:
           gl = gitlab.Gitlab(
               url=details.get("instance_link"),
               private_token=details.get("private_token")
           )

           # Если запись об инстансе не вызвала ошибку, то дополняем список инстансом
           data[gitlab_instance] = {}

           projects = gl.projects.list(iterator=True)

           print(f"Начато обновление списка репозиториев для {gitlab_instance}")

           # Пробегаем по ресурсу, собирая имена репозиториев,
           # ссылки на них и имена веток
           for project in projects:
               print(f"\tДобавляется проект: {project.name}") # немного дебага
               data[gitlab_instance][project.name] = {
                           'name': project.name,
                           'details': {
                               'ssh_url_to_repo': project.ssh_url_to_repo,
                               'branches': [branch.name for branch in project.branches.list()]
                           }
                       }
        except:
            print("Что-то пошло не так!")
            print("-" * 40)
            print(f"Репозитории с инстанса(сайта) {gitlab_instance} не добавлены в список!")
            return False

    with open(output, 'w') as file:
        yaml.safe_dump(data, file, sort_keys=False)
    return True


#print(read_config(config_file))

if repos_update(repos_list):
    print('Список репозиториев и веток для перечисленных инстансов обновлен')
else:
    print('Список репозиториев содержит ошибочные данные или истекшие токены')
    print('Пожалуйста, проверьте актуальность последнего в списке обновлений инстанса')
    exit(1)

# TODO примонтировать жёсткие диски, если их нет, то указать временную папку и поднять флажок

# TODO создать структуру папок

# TODO клонировать репозитории в папки

# TODO отмонтировать жёсткие диски если они были установлены, либо ждать установки жёстких дисков
# и, при их установке - синхронизировать и отмонтировать

# TODO
