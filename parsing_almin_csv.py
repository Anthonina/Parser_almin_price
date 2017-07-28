
import lxml.html as html

from pandas import DataFrame 

from bs4 import BeautifulSoup
    # pip install beautifulsoup4

from utils import get_html


def get_product_groups (html):
    soup = BeautifulSoup(html, 'lxml')
    groups_list = soup.find_all('td', class_ = 'sec_name')

    groups = []

    if len(groups_list) > 0:
        for group in groups_list:
            div = group.find('div')
            name_product_groups = div.get_text()
            id_product_groups = div.get('onclick')
            id_product_groups = id_product_groups.replace('click_plus(', '').replace(');', '')

            url_product_groups = 'http://almin.ru/catalog/list.php?SECTION_ID=00000&SHOWALL_1=1'.replace('00000', id_product_groups)

            groups.append({
                'group_name': name_product_groups,
                'group_url': url_product_groups
                })

    return groups


import csv

def write_csv(groups):
    with open ('almin.csv', 'w', newline='') as file: # Первый аргумент - имя файла, второй - ключ записи (write)
         writer = csv.writer (file, delimiter=';') # Созаём "записыватель" csv. Первый аргумент - файл с заданными параметрами. Второй - разделитель
         for group in groups:
            writer.writerow([group['group_name'], group['group_url']]) # Функция writerow принимает только массивы и списки


def main():
    url = 'http://almin.ru/catalog/catalog.php?product=all'
    html_handler = get_html(url)
    all_groups = get_product_groups(html_handler)
    #almin_groups_csv = write_csv (all_groups)

    #print(all_groups)
    write_csv(all_groups)


if __name__ == '__main__': # вызов функции при вызове файла на исполнение
    main()



