import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import re

current_datetime = datetime.now()
day = current_datetime.day
hour = current_datetime.hour
minute = current_datetime.minute

URL = 'https://blackterminal.ru/dividends'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': '*/*'}
FILE = f'data-{day}-{hour}-{minute}.xlsx'
COUNT_PAGE = 20


# Подключение к серверу. Возвращает response(ответ)
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# Получение количества страниц и удаление кнопок "назад", "далее"
# def get_pages_count(html):
#     soup = BeautifulSoup(html, 'lxml')
#     pagination_delete = soup.find_all('a', class_='index__withWiderPaddings--164')
#     if pagination_delete:
#         for item in pagination_delete:
#             item.decompose()
#     pagination = soup.find_all('a', class_='index__paginationItem--1e8')
#     if pagination:
#         for item in pagination:
#             return int(pagination[-1].get_text())
#     else:
#         return 1


# Получение контента со страницы
def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('tr.w14')
    stocks = []
    for item in items:
        stocks.append({
            'title': item.select_one('tr.w14 > td:first-child > a').text,
            'sector': item.select_one('tr.w14 > td:nth-child(2) > a').text,
            'price': item.select_one('tr.w14 > td:nth-child(3)').text.replace('\xa0₽', '').replace('\xa0$', '').replace('\xa0HK$', '').replace('\xa0NOK', '').replace('\xa0€', '').replace('\xa0£', '').replace('\xa0CA$', '').replace('\xa0', ''),
            'currency': re.sub("[0-9]", "", item.select_one('tr.w14 > td:nth-child(3)').text.replace(',', '')),
            'percentage_of_dividends': item.select_one('tr.w14 > td:nth-child(5)').text,
            'buy_before': item.select_one('tr.w14 > td:nth-child(8)').text,
        })
    print(stocks)
    return stocks


# Сохранение данных в файл.csv
def save_file(items, path):
    if path:
        with open(path, 'a+', newline='') as file:
            file.writer = csv.writer(file, delimiter=',')
            file.writer.writerow(['Название Компании', 'Сектор', "Цена", "Валюта", 'Див дох', 'До какого купить'])
            for item in items:
                file.writer.writerow([item['title'], item['sector'], item['price'], item['currency'], item['percentage_of_dividends'], item['buy_before']])
    else:
        print('Ошибка с переменной path')


# Парсинг данных
def parse():
    html = get_html(URL)
    if int(html.status_code) == 200:
        stocks = []
        for i in range(1, COUNT_PAGE + 1):
            print(f'Работаем над страницей {i} из {COUNT_PAGE}...')
            html = get_html(URL, params={'page': i})
            stocks.extend(get_content(html.text))

        save_file(stocks, FILE)
        print(f'Обработанно {len(stocks)} акций! И добавленны в файл {FILE}')
    else:
        print(f'Ошибка! Сервер вернул код: {html.status_code}')


parse()

# response = requests.get(URL)
# soup = BeautifulSoup(response.text, 'lxml')
# items = soup.find_all('tr', class_='QuoteTable__tableRow--1AA QuoteTable__withHover--1vT')
#
# stocks = []
# for item in items:
#     stocks.append({
#         'title': item.find('a', class_='InstrumentLink__instrument--1PO').get_text().replace('ао',''),
#         'price': item.find('td', class_='QuoteTable__tableCell--1Lh QuoteTable__right--166').get_text().replace('\xa0₽','')
#     })
# print(stocks)
#
# # if stocks:
# #     for stock in stocks:
# #         if stock['price'] != '':
# #             x = stock['price']
# #             x = float(x)
# #             if x > 500:
# #                 print(stock['title'], x)
#
#
#
#
#
# # print(x['price'])
