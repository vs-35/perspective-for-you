from class_api import HeadHunterAPI, SuperJobAPI
from class_vacancy import Vacancy
from class_ison import JSONopener

# Функция для взаимодействия с пользователем
def user_interaction():
    """Функция для получения исходного запроса пользователя"""

    user_choice = int(input('Приветствуем! С какой платформы  получить вакансии: 1 - HeadHunter, 2 - SuperJob, 3 - оба'))

    if user_choice != 1 and user_choice != 2 and user_choice != 3:
        print("Ошибка выбора")
        exit()
    keyword = input('Введите интересующее вас слово для поиска')

    filter = input('Введите дополнительный показатель для фильтрации (оставить пустым, если не нужно фильтровать)?')

    job_max = int(input("Введите число вакансий для вывода (не более 100): "))

    # Запрос к API сайтов с вакансиями проводим в зависимости от выбора пользователя
    if user_choice == 1:
        HeadHunterAPI().get_vacancies(keyword)
        source_data = JSONopener('hh.json').open_json()
    elif user_choice == 2:
        SuperJobAPI().get_vacancies(keyword)
        source_data = JSONopener('superjob.json').open_json()
    elif user_choice == 3:
        HeadHunterAPI().get_vacancies(keyword)
        SuperJobAPI().get_vacancies(keyword)
        source_data = JSONopener('hh.json').open_json() + JSONopener('superjob.json').open_json()


    # Если пользователь указал дополнительный показатель фильтрации, вакансии фильтруются не нему
    filtered_data = [x for x in source_data if filter in x['title'] or filter in x['requirement']]
    # Создаем список из экземпляров класса Vacancy из отфильтрованного списка
    vacancies = [Vacancy(x['title'], x['url'], x['salary_from'], x['salary_to'], x['salary_currency'], x['requirement'])
                 for x in filtered_data]
    n = 1
    for vacancy in vacancies:
        print(f"{n}. {vacancy}")

        # Проверяем достигло ли число выведенных вакансий максимального (указанного пользователем)
        if n == job_max:
            break
        else:
            n += 1

    #Дополнительный показатель для сортировки заработной платы
    sort_choice = int(input('Отсортировать вакансии по зарплате? Нажмите - 1'))
    if sort_choice == 1:

        sorted_vacancies = sorted(vacancies, reverse=True)
        n = 1
        for vacancy in sorted_vacancies:
            print(f"{n}. {vacancy}")
            if n == job_max:
                break
            else:
                n += 1
    else:
        print("Сортировка завершена")

if __name__ == "__main__":
    user_interaction()