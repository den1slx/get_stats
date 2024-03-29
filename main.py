import requests
from terminaltables import AsciiTable
import os
from dotenv import load_dotenv
import argparse
import json


def predict_rub_salary(vacancy):
    if not vacancy.get('salary'):
        return None
    if not vacancy['salary']:
        return None
    salary_from, salary_to, salary_currency, *salary_other = vacancy['salary'].values()
    if salary_currency != 'RUR':
        return None
    salary = predict_salary(salary_from, salary_to)
    return salary


def predict_salary(payment_from, payment_to):
    if payment_from and payment_to:
        salary = (payment_from + payment_to) // 2
        return salary
    elif payment_from and not payment_to:
        salary = int(payment_from * 1.2)
        return salary
    elif not payment_from and payment_to:
        salary = int(payment_to * 0.8)
        return salary
    else:
        return None


def predict_rub_salary_for_superjob(vacancy):
    payment_from, payment_to = vacancy['payment_from'], vacancy['payment_to']
    return predict_salary(payment_from, payment_to)


def get_superjob_statistics(token, desired_strings, sj_params):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': token,
    }
    stats = {}
    for string in desired_strings:
        page = 0
        total = 0
        processed_total = 0
        average_salaries = []
        average_salary = 0
        while True:
            params = {
                "page": page,
                "keyword": string,
            }
            params.update(sj_params)
            response = requests.get(url, headers=headers, params=params)
            if not response.ok:
                stats[string] = {
                    "vacancies_found": None,
                    "vacancies_processed": None,
                    "average_salary": None,
                }
                break
            unpacked_response = response.json()
            if not total:
                total = unpacked_response['total']
                if not total:
                    break
            if not unpacked_response['objects']:
                break
            vacancies = unpacked_response['objects']
            for vacancy in vacancies:
                if vacancy:
                    average_salary = predict_rub_salary_for_superjob(vacancy)
                if average_salary:
                    average_salaries.append(average_salary)
                    processed_total += 1

            if not processed_total:
                average_salary = 0
            else:
                average_salary = sum(average_salaries) // processed_total
            more = unpacked_response['more']
            if not more:
                break
            page += 1

        stats[string] = {
            'vacancies_found': total,
            'vacancies_processed': processed_total,
            'average_salary': average_salary,
        }

    return stats


def get_stats_for_table(stats, table_headers=None):
    stats_for_table = []
    if table_headers:
        stats_for_table.append(table_headers)
    for name, stat in stats.items():
        chapter = []
        chapter.append(name)
        values = stat.values()
        for value in values:
            chapter.append(value)
        stats_for_table.append(chapter)

    return stats_for_table


def get_hh_statistics(desired_strings, hh_params):
    url = 'https://api.hh.ru/vacancies'
    stats = {}
    for string in desired_strings:
        salaries = []
        page = 0
        pages = 1
        found = 0
        while page < pages:
            page += 1
            params = {
                'text': string,
                'page': page,
            }
            params.update(hh_params)
            response = requests.get(url, params=params)
            unpacked_response = response.json()
            if not response.ok:
                stats[string] = {
                    "vacancies_found": None,
                    "vacancies_processed": None,
                    "average_salary": None,
                }
                break
            else:
                if not found:
                    found = unpacked_response['found']
                pages = unpacked_response['pages']
                vacancies = unpacked_response['items']
                for vacancy in vacancies:
                    salaries.append(predict_rub_salary(vacancy))

        redacted_salaries = [salary for salary in salaries if salary]
        if redacted_salaries:
            average_salaries = sum(redacted_salaries) // len(redacted_salaries)
        else:
            average_salaries = 0
        stats[string] = {
            "vacancies_found": found,
            "vacancies_processed": len(redacted_salaries),
            "average_salary": average_salaries,
        }
    return stats


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--desired_strings',
        nargs='+',
        help='''list strings for text in hh_params and 
        keyword in sj_params''',
        default=[
            'Программист JavaScript',
            'Программист Java',
            'Программист Python',
            'Программист Ruby',
            'Программист PHP',
            'Программист C++',
            'Программист C#',
            'Программист C',
            'Программист Go',
            'Программист Shell',
        ]
    )
    parser.add_argument(
        '-hp',
        '--hh_params',
        help='''params for hh request,
        {text: '', page: ''} not should in params''',
        default='{"professional_role": "96", "area": "1", "date_from": "2000-01-01", "per_page": 100}'
    )
    parser.add_argument(
        '-sp',
        '--sj_params',
        help='''params for superjob,
        {keyword: '', keywords: '', page: ''} not should in params''',
        default='{"period": 0, "town": 4, "catalogues": 48, "count": 100}'
    )
    parser.add_argument(
        '-thh',
        '--table_headers_hh',
        help='headers for table hh',
        nargs='+',
        default=[
            'keywords',
            'total',
            'total processed',
            'average salary',
        ],
    )
    parser.add_argument(
        '-tsj',
        '--table_headers_sj',
        help='headers for table superjob',
        nargs='+',
        default=[
            'keywords',
            'total',
            'total processed',
            'average salary',
        ],
    )
    return parser


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()
    hh_headers, sj_headers = args.table_headers_hh, args.table_headers_sj
    desired_strings = args.desired_strings
    hh_params = json.loads(args.hh_params)
    sj_params = json.loads(args.sj_params)
    sj_token = os.environ['SJ_SECRET_KEY']
    statistics_hh = get_hh_statistics(desired_strings, hh_params)
    statistics_sj = get_superjob_statistics(sj_token, desired_strings, sj_params)
    statistics_for_table_hh = get_stats_for_table(statistics_hh, table_headers=hh_headers)
    statistics_for_table_sj = get_stats_for_table(statistics_sj, table_headers=sj_headers)
    table_hh = AsciiTable(statistics_for_table_hh, title='headhunter')
    table_sj = AsciiTable(statistics_for_table_sj, title='SuperJob')
    print(table_hh.table)
    print(table_sj.table)


if __name__ == '__main__':
    main()
