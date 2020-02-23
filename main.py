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
            for vacancy in response.json()["items"]:
                vacancies[language].append(vacancy)
    return vacancies


def get_more_sj_vacancies(languages, auth_header):
    vacancies = {}
    url = 'https://api.superjob.ru/2.30/vacancies/'
    for language in languages:
        vacancies[language] = []
        header = auth_header
        payload = {"keyword": f'{language}', "town": 4, "catalogues": 48, "count": 100}
        response = requests.get(url, headers=header, params=payload)
        for vacancy in response.json()["objects"]:
            vacancies[language].append(vacancy)
    return vacancies


def predict_rub_salary_hh(vacancies):
    vacancies_data = {}
    for language in vacancies.keys():
        vacancies_data[language] = {}
        vacancies_data[language]['vacancies found'] = len(vacancies[language])
        vacancies_data[language]['vacancies processed'] = 0
        salaries_sum = 0
        for vacancy in vacancies[language]:
            if vacancy['salary'] is not None and vacancy['salary']['currency'] == "RUR":
                vacancies_data[language]['vacancies processed'] += 1
                salary = predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
                salaries_sum += salary
        vacancies_data[language]['average salary'] = int(salaries_sum / vacancies_data[language]['vacancies processed'])
    return vacancies_data


def predict_rub_salary_sj(vacancies):
    vacancies_data = {}
    for language in vacancies.keys():
        vacancies_data[language] = {}
        vacancies_data[language]['vacancies found'] = len(vacancies[language])
        vacancies_data[language]['vacancies processed'] = 0
        salaries_sum = 0
        for vacancy in vacancies[language]:
            if vacancy['payment'] == 0:
                vacancies_data[language]['vacancies processed'] += 1
                salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
                salaries_sum += salary
        vacancies_data[language]['average salary'] = int(salaries_sum / vacancies_data[language]['vacancies processed'])
    return vacancies_data


def draw_table(vacancies_data, table_title):
    table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for key, value in vacancies_data.items():
        new_row = [item for item in list(value.values())]
        new_row.insert(0, key)
        table_data.append(new_row)
    table = AsciiTable(table_data, table_title)
    print(table.table)
    print()


def main():
    languages = ["Python", "C++", "Java", "PHP", "Ruby", "Javascript", "GO"]
    hh_data = predict_rub_salary_hh(get_more_hh_vacancies(languages))
    sj_data = predict_rub_salary_sj(get_more_sj_vacancies(languages, sj_header))
    draw_table(hh_data, 'HeadHunter Moscow')
    draw_table(sj_data, 'Superjob Moscow')


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    sj_header = {'X-Api-App-Id': f'{token}'}
    main()
