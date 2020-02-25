import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    salary = 0
    if (salary_from is not None and salary_from != 0) and (salary_to is not None and salary_to != 0):
        salary = (salary_from + salary_to) / 2
    elif (salary_to is None or salary_to == 0):
        salary = salary_from * 1.2
    elif (salary_from is None or salary_from == 0):
        salary = salary_to * 0.8
    return salary


def get_more_hh_vacancies(languages):
    vacancies = {}
    url = 'https://api.hh.ru/vacancies'
    for language in languages:
        vacancies[language] = []
        payload = {'search_field': 'name', 'text': f'{language}'}
        response = requests.get(url, params=payload)
        page = 0
        for page in range(response.json()["pages"]):
            payload.update({'page': page, 'per_page': 20})
            response = requests.get(url, params=payload)
            vacancies[language].extend(response.json()["items"])
    return vacancies


def get_more_sj_vacancies(languages, auth_header):
    vacancies = {}
    url = 'https://api.superjob.ru/2.30/vacancies/'
    for language in languages:
        vacancies[language] = []
        header = auth_header
        payload = {"keyword": f'{language}', "town": 4, "catalogues": 48, "count": 100}
        response = requests.get(url, headers=header, params=payload)
        vacancies[language].extend(response.json()["objects"])
    return vacancies


def predict_rub_salary_hh(vacancies):
    vacancies_statistics = {}
    for language, language_vacancies in vacancies.items():
        vacancies_statistics[language] = {}
        vacancies_statistics[language]['vacancies found'] = len(language_vacancies)
        vacancies_statistics[language]['vacancies processed'] = 0
        salaries_total_value = 0
        for vacancy in language_vacancies:
            if vacancy['salary'] is not None and vacancy['salary']['currency'] == "RUR":
                vacancies_statistics[language]['vacancies processed'] += 1
                salary = predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
                salaries_total_value += salary
        vacancies_statistics[language]['average salary'] = int(salaries_total_value / vacancies_statistics[language]['vacancies processed'])
    return vacancies_statistics


def predict_rub_salary_sj(vacancies):
    vacancies_statistics = {}
    for language, language_vacancies in vacancies.items():
        vacancies_statistics[language] = {}
        vacancies_statistics[language]['vacancies found'] = len(language_vacancies)
        vacancies_statistics[language]['vacancies processed'] = 0
        salaries_total_value = 0
        for vacancy in language_vacancies:
            if vacancy['payment'] == 0:
                vacancies_statistics[language]['vacancies processed'] += 1
                salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
                salaries_total_value += salary
        vacancies_statistics[language]['average salary'] = int(salaries_total_value / vacancies_statistics[language]['vacancies processed'])
    return vacancies_statistics


def create_table(vacancies_statistics, table_title):
    table_rows = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for language, statistics in vacancies_statistics.items():
        new_row = [numeric_value for numeric_value in list(statistics.values())]
        new_row.insert(0, language)
        table_rows.append(new_row)
    table = AsciiTable(table_rows, table_title)
    return table


def draw_table(table):
    print(table.table)
    print()


def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    sj_header = {'X-Api-App-Id': f'{token}'}
    languages = ["Python", "C++", "Java", "PHP", "Ruby", "Javascript", "GO"]
    hh_statistics = predict_rub_salary_hh(get_more_hh_vacancies(languages))
    sj_statistics = predict_rub_salary_sj(get_more_sj_vacancies(languages, sj_header))
    hh_table = create_table(hh_statistics, "HeadHunter Moscow")
    sj_table = create_table(sj_statistics, "SuperJob Moscow")
    draw_table(hh_table)
    draw_table(sj_table)


if __name__ == '__main__':
    main()
