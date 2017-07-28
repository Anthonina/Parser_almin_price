
import lxml.html as html
from pandas import DataFrame
from datetime import datetime, date



import requests
	# pip install requests

from bs4 import BeautifulSoup
	# pip install beautifulsoup4


def get_html(url):
	r_html = requests.get(url) 
	# r - response - ответ сервера, который будет получать значение от модуля requests от метода get.
	# Метод get в качестве аргумента получает url
	return r_html.text	# возвращает html-код страницы, которая передана в качестве аргумента (url)


def get_table_data(html):
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table', class_ = 'sale_basket')
    table_rows = table.find_all('tr')

    goods = []

    if len(table_rows) > 0:
        for table_row in table_rows:
            
            table_cells = table_row.find_all('td')
            if len(table_cells) == 4:
                artnumber = table_cells[0].get_text()
                product_name = table_cells[1].find('a').get_text()
                detail_url = table_cells[1].find('a').get('href')
                price = table_cells[2].find('input').get('value')

                #print("Артикул: {}; Наименование: {}; Ссылка: {}; Цена: {}".format(artnumber,product_name,detail_url,price))

                goods.append({'artnumber':artnumber, 'product_name': product_name, 'detail_url': detail_url, 'price': price})

    return goods


import csv


def read_almin_csv(group_file):

    groups = []

    with open (group_file, 'r') as file:
         reader = csv.reader (file, delimiter=';')
         for row in reader:
            groups.append({'group_name': row[0], 'group_url': row[1]})

    return groups

            # print(row[0])
            #" ".join(
            #writer.writerow([group['group_name'], group['group_url']]) # Функция writerow принимает только массивы и списки          



def writer_almin_csv(all_groups):
    today = date.today()

    with open ('almin_goods_{}.csv'.format(today) , 'w', newline='') as file:
        writer = csv.writer (file, delimiter=';')
        writer.writerow(['Товарная группа', 'Артикул', 'Наименование товара', 'Цена', 'Ссылка на детальную страницу'])

        for group in all_groups:
            html_handler = get_html (group['group_url'])
            all_goods = get_table_data (html_handler)
            
            for product in all_goods:
                writer.writerow([group ['group_name'], product['artnumber'], product['product_name'], product ['price'], product ['detail_url']])
            
            #break



def main ():
    all_groups = read_almin_csv('almin.csv')

    writer_almin_csv(all_groups)

    # url = 'http://almin.ru/catalog/list.php?SECTION_ID=18108&SHOWALL_1=1'

    #html_handler = get_html(all_groups[0]['group_url'])

    #all_goods = get_table_data(html_handler)

    #print(all_goods)

    #all_links = get_all_links(html_handler)

    #for i in all_links:
    #	print(i)


if __name__ == '__main__':
    main()