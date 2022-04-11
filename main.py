import csv
import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_data(city_code='2398'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    }

    responce = requests.get(url='https://prom.ua/Avtozapchasti', headers=headers)

    # with open(f'index.html', 'w', encoding='utf-8') as file:
    #     file.write(responce.text)

    # with open(f'index.html', 'r', encoding='utf-8') as file:
    #     src = file.read()

    soup = BeautifulSoup(responce.text, 'lxml')
    cards = soup.findAll('div', class_='js-productad')

    output_file = f'{cur_time}.csv'

    with open(output_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            'Продукт',
            'Цена',
            'Компания',
            'Город',
            'Рейтинг'
        ))

    for card in cards:
        title = card.select('span[data-qaid="product_name"]')[0].text.strip()
        price = card.select('span[data-qaid="product_price"]')[0].text.strip().replace('&nbsp;', ' ')
        city = card.select('span[data-qaid="region_title"]')[0].text.strip()
        rate = card.select('span[data-qaid="short_company_rating"]')[0].text.strip()
        company = card.select('a[data-qaid="company_name"]')[0].text.strip()
        print(title + '\n' + price + '\n' + city + '\n' + company + '\n' + rate)

        with open(output_file, 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                title,
                price,
                company,
                city,
                rate
            ))

        print(f'{output_file} is ready')

def main():
    collect_data()


if __name__ == '__main__':
    main()
