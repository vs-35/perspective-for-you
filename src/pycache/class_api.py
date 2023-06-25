import json
import os
import requests

from class_abc import API


class HeadHunterAPI(API):
    """Класс, наследующийся от абстрактного класса API, для работы с сайтом HeadHunter через подключение к API"""
    def get_vacancies(self, keyword):
        """Функция для получения вакансий с сайта HeadHunter"""
        response = requests.get(
        "https://api.hh.ru/vacancies?",
        headers={"HH-User-Agent": 'perspective_for_you/1.0 (ksop.gubaha@gmail.com)'},
        params={"text": keyword, "per_page": 100}
        )
        job_list = []
        # Создаем общий формат выдачи по API от HeadHunter и SuperJob с проверкой отсутствия необязательных полей
        for item in response.json()['items']:
            if item['snippet']['requirement'] is None:
                item['snippet']['requirement'] = ""

            if item['salary'] is None:
                salary_from = 0
                salary_to = 0
                salary_currency = ""
            else:
                salary_from = item['salary']['from']
                salary_to = item['salary']['to']
                salary_currency = item['salary']['currency']
            if salary_from == None:
                salary_from = 0
            if salary_to == None:
                salary_to = 0
            # данные списка формируются и сохраняются в локальный файл(формат .json)
            data = {
                "title": item['name'],
                "url": "https://hh.ru/vacancy/" + item['id'],
                "salary_from":  salary_from,
                "salary_to": salary_to,
                "salary_currency": salary_currency,
                "requirement": item['snippet']['requirement']
            }
            job_list.append(data)

        with open("hh.json", "w", encoding='cp1251') as f:
            json.dump(job_list, f, ensure_ascii=False)


class SuperJobAPI(API):
    """Класс, наследующийся от абстрактного класса API, для работы с сайтом SuperJob через подключение к API"""
    def get_vacancies(self, keyword):
        """Функция для получения вакансий с сайта SuperJob"""
        response = requests.get(
        "https://api.superjob.ru/2.0/vacancies/",
        headers={"X-Api-App-Id": os.getenv('SJ_SECRET_KEY')},
        params={"keyword": keyword}
    )
        job_list = []
        # Создаем общий формат выдачи по API от HeadHunter и SuperJob с проверкой отсутствия необязательных полей
        for object in response.json()['objects']:
            if object['candidat'] is None:
                object['candidat'] = ""
            # данные списка формируются и сохраняются в локальный файл(формат.json)
            data = {
                "title": object['profession'],
                "url": object['link'],
                "salary_from":  int(object['payment_from']),
                "salary_to": int(object['payment_to']),
                "salary_currency":  "RUB",
                "requirement": object['candidat']
            }
            job_list.append(data)
        with open("superjob.json", "w", encoding='cp1251') as f:
            json.dump(job_list, f, ensure_ascii=False)
