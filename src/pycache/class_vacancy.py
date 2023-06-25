class Vacancy:
    """ Класс для работы с вакансиями.
        Класс поддерживает методы сравнения вакансий между собой по заработной плате.
        Параметры класса:
            title: название вакансии,
            url: ссылка на вакансию,
            salary_from: зарплата от...,
            salary_to: зарплата до...,
            salary_currency: валюта,
            description: описание (требования)
    """
    def __init__(self, title, url, salary_from, salary_to, salary_currency, requirement):
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.requirement = requirement

    """Метод для вывода информации о вакансии соискателю"""
    def __str__(self):
        return f'{self.title} ({self.url}) {self.salary_from} {self.salary_to} {self.salary_currency} {self.requirement}'


    """Методы сравнения вакансий между собой по заработной плате"""
    def __lt__(self, other):
        return self.salary_from < other.salary_from
    def __gt__(self, other):
        return self.salary_from > other.salary_from