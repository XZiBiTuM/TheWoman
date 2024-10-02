import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from catalog.models import Product, Category, NameOfClothe, Type, Secondary, Color, Inventory  # Импортируйте модель NameOfClothe
from django.utils import timezone
from django.db import IntegrityError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from transliterate import translit
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import schedule
import time


class Command(BaseCommand):
    help = 'Добавление товаров'

    def create_inventory(self, product):
        colors = Color.objects.all()
        for color in colors:
            Inventory.objects.create(product=product, color=color.name, quantity=5000)

    def handle(self, *args, **kwargs):
        # Здесь выполняем логику сбора данных
        data_from_source = self.get_data_from_web()

        products_to_create = []  # Создаем список для объектов Product

        for item_data in data_from_source:
            #category_name = item_data.get('category', '')
            category_name = 'KML'

            # Проверяем, существует ли категория с таким именем
            category, created = Category.objects.get_or_create(name=category_name)

            # Преобразуем значение в поле name_of_clothe в соответствии с вашими правилами
            raw_name_of_clothe = item_data['name_of_clothe']
            name_mapping = {
                "пижама": "пижаму",
                "маска": "маска",
                "пояс": "пояс",
                "халат/пеньюар": "халат/пеньюар",
                "эротическое белье": "эротическое белье",
                "комплект": "комплект",
                "трусы": "трусы",
                "сорочка": "сорочку",
                "бюстгальтер": " бюстгальтер",
                # Другие соответствия значений
            }
            if raw_name_of_clothe in name_mapping:
                name_of_clothe = name_mapping[raw_name_of_clothe]
            else:
                if category == 'Accessories':
                    name_of_clothe = 'аксессуар'
                elif category == 'Beachwear':
                    name_of_clothe = 'туника'
                else:
                    name_of_clothe = 'одежду'

            raw_size = item_data['size_cup']
            size_name_mapping = {
                'A': 'A',
                'B': 'B',
                'C': 'C',
                'D': 'D',
                'E': 'E',
                'F': 'F',
                'B,C': 'B, C',
                'B, C': 'B, C',
                'B и C': 'B, C',
                'C,B': 'B, C',
                'C, B': 'B, C',
                'C и B': 'B, C',
            }
            if raw_size in size_name_mapping:
                size = size_name_mapping[raw_size]
            else:
                size = item_data['size_cup']

            name_of_clothe_obj, created = NameOfClothe.objects.get_or_create(name=name_of_clothe)

            raw_type = item_data['type_s']
            type_name_mapping = {
                'бюстгалтеров': 'бюстгальтер',
                'масок': 'маску',
                'поясов': 'пояс',
                '': 'аксессуар',
            }

            if raw_type in type_name_mapping:
                type_s = type_name_mapping[raw_type]
            else:
                type_s = item_data['type_s']

            type_obj, created = Type.objects.get_or_create(name=type_s)

            raw_secondary = item_data['secondary']
            secondary_name_mapping = {
                'трусов': 'трусы',
            }

            if raw_secondary in secondary_name_mapping:
                secondary = secondary_name_mapping[raw_secondary]
            else:
                secondary = None

            if secondary is not None:
                secondary_obj, created = Secondary.objects.get_or_create(name=secondary)
            else:
                secondary_obj = None

            if secondary_obj is None:
                is_set = False
            else:
                is_set = True

            input_string = item_data['name']

            result_string = translit(input_string, 'ru', reversed=True).replace(' ', '-').lower()

            is_new_temp = item_data['is_new']

            if is_new_temp != '0':
                is_new = 'Новинка'
            else:
                is_new = 'Не новинка'

            is_sale_temp = item_data['is_sale']

            if is_sale_temp != '0':
                is_sale = 'Скидка'
            else:
                is_sale = 'Нет скидки'

            # Создаем объект Product, но не сохраняем его в базе данных
            product = Product(
                name=item_data['name'],
                slug=result_string,
                article=item_data['article'],
                price=item_data['price'],
                description=item_data['description'],
                category=category,
                name_of_clothe=name_of_clothe_obj,
                num_of_colors=item_data['num_of_colors'],
                num_of_products_in_packet=item_data['num_of_products_in_packet'],
                type=type_obj,
                secondary=secondary_obj,
                size_70=item_data['first_table_size'][0],
                num_of_size_70=int(item_data['first_table_num'][0][:1]),
                size_75=item_data['first_table_size'][1],
                num_of_size_75=int(item_data['first_table_num'][1][:1]),
                size_80=item_data['first_table_size'][2],
                num_of_size_80=int(item_data['first_table_num'][2][:1]),
                size_85=item_data['first_table_size'][3],
                num_of_size_85=int(item_data['first_table_num'][3][:1]),
                size_90=item_data['first_table_size'][4],
                num_of_size_90=int(item_data['first_table_num'][4][:1]),
                size_xs=item_data['second_table_size'][0],
                num_of_size_xs=int(item_data['second_table_num'][0][:1]),
                size_s=item_data['second_table_size'][1],
                num_of_size_s=int(item_data['second_table_num'][1][:1]),
                size_m=item_data['second_table_size'][2],
                num_of_size_m=int(item_data['second_table_num'][2][:1]),
                size_l=item_data['second_table_size'][3],
                num_of_size_l=int(item_data['second_table_num'][3][:1]),
                size_xl=item_data['second_table_size'][4],
                num_of_size_xl=int(item_data['second_table_num'][4][:1]),
                size=size,
                is_set=is_set,
                is_in_new_key=is_new,
                is_sale=is_sale,
                sale_price=item_data['sale_price'],
                # Заполняем остальные поля модели
            )

            products_to_create.append(product)  # Добавляем объект в список для массового создания

            # Создаем Inventory для текущего продукта

        # Массовое создание объектов Product в базе данных
        Product.objects.bulk_create(products_to_create)

        for product in products_to_create:
            self.create_inventory(product)

    def get_data_from_web(self):
        # Здесь выполняем HTTP-запрос к веб-странице и парсим данные
        url = 'https://optombelie.ru/catalog/accessories/'  # Замените на актуальный URL
        print(url)
        temp = int(input("Input num of product: "))

        if temp < 500:
            try:
                # Инициализируем браузер
                chrome_options = Options()
                chrome_options.add_argument("--headless")  # Этот аргумент включает режим "без графического интерфейса"

                # Инициализируем WebDriver с настройками
                driver = webdriver.Chrome()  # Предполагается, что вы используете Chrome WebDriver
                driver.maximize_window()
                driver.get(url)
                # Добавьте код для ожидания загрузки страницы, если это необходимо
                # Например, можно использовать WebDriverWait

                current_active_button = driver.find_element(By.CLASS_NAME, 'i-switch.active')

                # Получаем значение data-page для текущей активной кнопки
                current_page_value = current_active_button.get_attribute('data-page')
                print(current_page_value)

                try:
                    # Попытка найти кнопку для перехода на следующую страницу по значению data-page
                    next_page_element = driver.find_element(By.CSS_SELECTOR,
                                                            f'[data-page="{str(int(current_page_value) + 1)}"]')
                    print(next_page_element)
                    # Кликаем на следующей кнопке
                    next_page_element.click()
                except:
                    pass

                time.sleep(7)
                data = []

                while True:
                    # Здесь используйте методы Selenium для поиска и извлечения данных
                    i = 0
                    wait = WebDriverWait(driver, 15)
                    elements = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cart-item')))
                    elements = driver.find_elements(By.CLASS_NAME, 'cart-item')
                    elements = elements[temp:]
                    for item_element in elements:
                        i = i + 1
                        try:
                            raw_name = item_element.find_element(By.CLASS_NAME, 'PTSB.fs18').text.strip()
                            raw_article = item_element.find_element(By.CLASS_NAME, 'PTSB.fs12.grey7')
                            raw_price_text = item_element.find_element(By.CLASS_NAME, 'item-price').text.strip()
                            raw_category = item_element.find_element(By.CLASS_NAME, 'floatr').text.strip()
                            raw_name_of_clothe = item_element.find_element(By.CLASS_NAME, 'fs14.PTSB').text
                            raw_temp = item_element.find_elements(By.CLASS_NAME, 'PTSB.fs13')

                            if len(raw_temp) >= 2:
                                raw_num_of_colors = raw_temp[1]
                                size_cup = raw_temp[0].text
                            else:
                                size_cup = 'NoneSize'
                                raw_num_of_colors = raw_temp[0]

                            # Удаляем первый и последний символ из 'name'
                            name = raw_name[1:-1]
                            # Извлекаем только цифры из 'article' и оставляем их в строковом формате
                            span_article = raw_article.find_elements(By.TAG_NAME, 'span')
                            if span_article:
                                article_from_span = span_article[0]
                                article_temp = article_from_span.text[9:]
                                article = article_temp
                            else:
                                article = '1'
                            # Извлекаем цену, убирая все символы, кроме цифр, и преобразуем ее в целое число
                            if raw_price_text:
                                price = int(''.join(filter(str.isdigit, raw_price_text)))
                            else:
                                price = 0

                            category = raw_category[1:-1]

                            name_of_clothe = raw_name_of_clothe[8:-1]

                            if raw_num_of_colors:
                                num_of_colors = 2
                            else:
                                num_of_colors = 1

                            product_links = driver.find_elements(By.CLASS_NAME, 'PTSB.fs18')

                            product_link = product_links[temp]

                            product_url = product_link.get_attribute('href')
                            driver.get(product_url)

                            num_of_products_in_packet = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fs24.pl10')))
                            num_of_products_in_packet = driver.find_element(By.CLASS_NAME, 'fs24.pl10').text
                            # Здесь парсим данные с текущей страницы товара
                            # Например, используя BeautifulSoup
                            description = driver.find_element(By.CLASS_NAME, 'pt30').text
                            # После того как вы спарсили данные, можете сохранить их в файл или базу данных
                            try:
                                # Ищем таблицу

                                tables = driver.find_elements(By.CLASS_NAME, 'size-table')

                                table = tables[0]

                                # Извлекаем значения из первой строки (размеры)
                                size_values = []
                                size_row = table.find_element(By.TAG_NAME, 'tr')
                                for cell in size_row.find_elements(By.TAG_NAME, 'td')[:5]:
                                    size_values.append(cell.text)

                                # Извлекаем значения из второй строки (количество)
                                quantity_values = []
                                quantity_row = size_row.find_element(By.XPATH, './following-sibling::tr')
                                for cell in quantity_row.find_elements(By.TAG_NAME, 'td')[:5]:
                                    quantity_values.append(cell.text)

                                # Если второй элемент с классом "size-table" существует
                                if len(tables) >= 2:
                                    # Выбираем второй элемент
                                    secondary_table = tables[1]

                                    secondary_size_values = []
                                    secondary_size_row = secondary_table.find_element(By.TAG_NAME, 'tr')
                                    for cell in secondary_size_row.find_elements(By.TAG_NAME, 'td')[:5]:
                                        secondary_size_values.append(cell.text)

                                    secondary_quantity_values = []
                                    secondary_quantity_row = secondary_size_row.find_element(By.XPATH, './following-sibling::tr')
                                    for cell in secondary_quantity_row.find_elements(By.TAG_NAME, 'td')[:5]:
                                        secondary_quantity_values.append(cell.text)
                                else:
                                    # Если второго элемента нет, вы можете обработать этот случай или бросить исключение
                                    secondary_size_values = []
                                    secondary_quantity_values =[]

                            except Exception as e:
                                print(f"Произошла ошибка: {str(e)}")

                            # Заполняем размеры и количество '0' до максимальной длины в 5 элементов
                            size_values.extend(['0'] * (5 - len(size_values)))
                            quantity_values.extend(['0 шт'] * (5 - len(quantity_values)))
                            secondary_size_values.extend(['0'] * (5 - len(secondary_size_values)))
                            secondary_quantity_values.extend(['0 шт'] * (5 - len(secondary_quantity_values)))

                            colors = driver.find_elements(By.CLASS_NAME, 'item-color')

                            colors_list = []

                            x = 0
                            for color_one in colors:
                                color_one = colors[x].get_attribute('color').capitalize()
                                colors_list.append(color_one)
                                x = x + 1

                            temp_type = driver.find_elements(By.CLASS_NAME, 'diblock.w200.right.pl10.PTSB')

                            type_text = temp_type[2].text[8:-1]

                            if len(temp_type) >= 4:
                                secondary_type_text = temp_type[3].text[8:-1]
                            else:
                                secondary_type_text = '0'

                            try:
                                is_new = driver.find_element(By.CLASS_NAME, 'hot')
                            except NoSuchElementException:
                                is_new = '0'

                            try:
                                is_sale = driver.find_element(By.CLASS_NAME, 'disc')
                            except NoSuchElementException:
                                is_sale = '0'

                            try:
                                old_price_temp = driver.find_element(By.CLASS_NAME, 'old-price.mb-5.mt0')
                                raw_old_price_text = old_price_temp.find_element(By.TAG_NAME, 'div').text.strip()
                            except NoSuchElementException:
                                raw_old_price_text = '0'

                            if raw_price_text:
                                sale_price = int(''.join(filter(str.isdigit, raw_old_price_text)))
                            else:
                                sale_price = 0

                            item_data = {
                                'name': name,
                                'article': article,
                                'price': price,
                                'category': category,
                                'name_of_clothe': name_of_clothe,
                                'num_of_colors': num_of_colors,
                                'num_of_products_in_packet': num_of_products_in_packet,
                                'description': description,
                                'first_table_size': size_values,
                                'first_table_num': quantity_values,
                                'second_table_size': secondary_size_values,
                                'second_table_num': secondary_quantity_values,
                                'color': colors_list,
                                'size_cup': size_cup,
                                'type_s': type_text,
                                'secondary': secondary_type_text,
                                'is_new': is_new,
                                'is_sale': is_sale,
                                'sale_price': sale_price,
                                # Извлекайте остальные данные
                            }
                            data.append(item_data)
                            temp = temp + 1
                        except StaleElementReferenceException:

                            continue

                    print(data)
                    return data

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при запросе к веб-странице: {e}'))
                return []

            finally:
                # Важно закрыть браузер после использования
                driver.quit()
