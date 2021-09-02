import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.sports.ru/la-liga/table/?s=8000&sub=table"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
FILE = 'table_1995.csv'


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_contact(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('table.stat-table tbody > tr:nth-child(3)')

    table = []
    for item in items:
        table.append({
            'games': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(3)').text),
            'wins': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(4)').text),
            'draws': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(5)').text),
            'defeats': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(6)').text),
            'goal_scored': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(7)').text),
            'goal_conceded': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(8)').text),
            'points': int(item.select_one('table.stat-table tbody > tr:nth-child(3) td:nth-child(9)').text)
        })

    save_file(table, FILE)


def save_file(items, path):
    if path:
        with open(path, 'w', newline='') as file:
            file.writer = csv.writer(file, delimiter=';')
            file.writer.writerow(
                ['Количество игр', 'Победы', "Ничьи", "Поражение", 'Забитые голы', 'Пропущенные голы', 'Очки'])
            for item in items:
                file.writer.writerow([item['games'], item['wins'], item['draws'], item['defeats'], item['goal_scored'],
                                      item['goal_conceded'], item['points']])
    else:
        print('Ошибка с переменной path')


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_contact(html.text)
        print('Таблица сохранена в файл', FILE)
    else:
        print("error")


parse()
