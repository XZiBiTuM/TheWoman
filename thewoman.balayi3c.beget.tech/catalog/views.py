from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import OrderForm
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.core.exceptions import ValidationError
import shutil
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, When, Value, IntegerField
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.core.mail import EmailMessage
import urllib.parse
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


logger = logging.getLogger(__name__)


def my_view(request):
    # Ваш код
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    # Ваш код


def send_order_mail(order):
    gmail_user = 'thewoman.optombelie@gmail.com'
    gmail_password = 'sngl lyjc hfuj hbcr'

    # Создание объекта SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Установка TLS-соединения
    server.starttls()

    # Вход в учетную запись
    server.login(gmail_user, gmail_password)

    to_email = order.email

    product_name_list = order.product_name.split(", ")
    product_article_list = order.product_article.split(", ")
    product_size_list = order.product_size.split(", ")
    product_price_for_one_list = order.product_price_for_one.split(", ")
    product_quantity_list = order.product_quantity.split(", ")
    product_image_list = order.product_img.split(", ")
    product_size_comment_list = order.product_comment_size.split(", ")

    subject = "Подтверждение заказа"
    message = "*** Это письмо сформировано автоматически, отвечать на него не нужно ***<br><br><br>"
    message += f"Здравствуйте, уважаемый покупатель!<br><br>"
    message += f"Благодарим вас за заказ!<br><br>"
    message += f"Ваш заказ:<br><br>"
    message += "<table border='1'>"
    message += "<tr><th>№</th><th>Изображение товара</th><th>Название</th><th>Артикул</th><th>Размер чашки</th><th>Цена за упаковку</th><th>Количество</th><th>Размер товара (если поштучно)</th></tr>"
    
    for i in range(len(product_name_list)):
        message += "<tr>"
        message += f"<td>{i + 1}</td>"
        message += f"<td style='text-align:center; vertical-align:middle;'><img src='https://exoptombelie.store/media/{product_image_list[i]}' alt='product_image' width='45px' height='60px'></td>"
        message += f"<td>{product_name_list[i]}</td>"
        message += f"<td>{product_article_list[i]}</td>"
        message += f"<td>{product_size_list[i]}</td>"
        message += f"<td>{product_price_for_one_list[i]}₽</td>"
        message += f"<td>{product_quantity_list[i]}шт.</td>"
        if product_size_comment_list[i] != 'None':
            message += f"<td>{product_size_comment_list[i]}</td>"
        else:
            message += "<td>-</td>"
        message += "</tr>"
    
    message += "</table>"
    message += "<br><br><br>"
    message += f"Сумма вашего заказа: {order.product_price_total}₽<br><br>"
    message += "Если у вас есть вопросы, свяжитесь с нами.<br>"
    message += "Почта для связи: sales@optombelie.ru<br><br>"
    message += "С уважением,<br>The Woman©<br><br>"

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    server.sendmail(gmail_user, to_email, msg.as_string())

    # Завершение сеанса
    server.quit()


def send_order_mail_to_admin(order):
    gmail_user = 'thewoman.optombelie@gmail.com'
    gmail_password = 'sngl lyjc hfuj hbcr'

    # Создание объекта SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Установка TLS-соединения
    server.starttls()

    # Вход в учетную запись
    server.login(gmail_user, gmail_password)

    to_email = 'punktik@inbox.ru' # поменять на нужную почту
    #to_email = 'balayi323161@mail.ru'
    
    product_name_list = order.product_name.split(", ")
    product_article_list = order.product_article.split(", ")
    product_size_list = order.product_size.split(", ")
    product_price_for_one_list = order.product_price_for_one.split(", ")
    product_quantity_list = order.product_quantity.split(", ")
    product_image_list = order.product_img.split(", ")
    product_size_comment_list = order.product_comment_size.split(", ")

    subject = "Подтверждение заказа"
    message = "*** Это письмо сформировано автоматически, отвечать на него не нужно ***<br><br><br>"
    message += "<br><br>Покупатель:<br><br>"
    message += f"<table border='1'>"
    message += "<tr><th>Имя</th><th>Фамилия</th><th>Телефон</th><th>Эл. Почта</th><th>Адрес</th></tr>"
    message += "<tr>"
    message += f"<td>{order.first_name}</td>"
    message += f"<td>{order.last_name}</td>"
    message += f"<td>{order.phone_number}</td>"
    message += f"<td>{order.email}</td>"
    message += f"<td>{order.address}</td>"
    message += "</tr>"
    message += "</table><br><br>"
    message += f"Заказ:<br><br>"
    # Теперь у вас есть списки с отдельными элементами
    # Вы можете использовать цикл для обработки элементов
    message += "<table border='1'>"
    message += "<tr><th>№</th><th>Изображение товара</th><th>Название</th><th>Артикул</th><th>Размер чашки</th><th>Цена за упаковку</th><th>Количество</th><th>Размер товара (если поштучно)</th></tr>"
    
    for i in range(len(product_name_list)):
        message += "<tr>"
        message += f"<td>{i + 1}</td>"
        message += f"<td style='text-align:center; vertical-align:middle;'><img src='https://exoptombelie.store/media/{product_image_list[i]}' alt='product_image' width='45px' height='60px'></td>"
        message += f"<td>{product_name_list[i]}</td>"
        message += f"<td>{product_article_list[i]}</td>"
        message += f"<td>{product_size_list[i]}</td>"
        message += f"<td>{product_price_for_one_list[i]}₽</td>"
        message += f"<td>{product_quantity_list[i]}шт.</td>"
        if product_size_comment_list[i] != 'None':
            message += f"<td>{product_size_comment_list[i]}</td>"
        else:
            message += "<td>-</td>"
        message += "</tr>"
    
    message += "</table>"
    message += "<br><br><br>" 
    message += f"Сумма заказа: {order.product_price_total}₽<br>"
    message += "Powered by The Woman©"

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    server.sendmail(gmail_user, to_email, msg.as_string())

    # Завершение сеанса
    server.quit()
    
    
def send_order_mail_to_admin_two(order):
    gmail_user = 'thewoman.optombelie@gmail.com'
    gmail_password = 'sngl lyjc hfuj hbcr'

    # Создание объекта SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Установка TLS-соединения
    server.starttls()

    # Вход в учетную запись
    server.login(gmail_user, gmail_password)

    to_email = 'sales@optombelie.ru' # поменять на нужную почту
    #to_email = 'balayi3228@mail.ru'
    
    product_name_list = order.product_name.split(", ")
    product_article_list = order.product_article.split(", ")
    product_size_list = order.product_size.split(", ")
    product_price_for_one_list = order.product_price_for_one.split(", ")
    product_quantity_list = order.product_quantity.split(", ")
    product_image_list = order.product_img.split(", ")
    product_size_comment_list = order.product_comment_size.split(", ")

    subject = "Подтверждение заказа"
    message = "*** Это письмо сформировано автоматически, отвечать на него не нужно ***<br><br><br>"
    message += "<br><br>Покупатель:<br><br>"
    message += f"<table border='1'>"
    message += "<tr><th>Имя</th><th>Фамилия</th><th>Телефон</th><th>Эл. Почта</th><th>Адрес</th></tr>"
    message += "<tr>"
    message += f"<td>{order.first_name}</td>"
    message += f"<td>{order.last_name}</td>"
    message += f"<td>{order.phone_number}</td>"
    message += f"<td>{order.email}</td>"
    message += f"<td>{order.address}</td>"
    message += "</tr>"
    message += "</table><br><br>"
    message += f"Заказ:<br><br>"
    # Теперь у вас есть списки с отдельными элементами
    # Вы можете использовать цикл для обработки элементов
    message += "<table border='1'>"
    message += "<tr><th>№</th><th>Изображение товара</th><th>Название</th><th>Артикул</th><th>Размер чашки</th><th>Цена за упаковку</th><th>Количество</th><th>Размер товара (если поштучно)</th></tr>"
    
    for i in range(len(product_name_list)):
        message += "<tr>"
        message += f"<td>{i + 1}</td>"
        message += f"<td style='text-align:center; vertical-align:middle;'><img src='https://exoptombelie.store/media/{product_image_list[i]}' alt='product_image' width='45px' height='60px'></td>"
        message += f"<td>{product_name_list[i]}</td>"
        message += f"<td>{product_article_list[i]}</td>"
        message += f"<td>{product_size_list[i]}</td>"
        message += f"<td>{product_price_for_one_list[i]}₽</td>"
        message += f"<td>{product_quantity_list[i]}шт.</td>"
        if product_size_comment_list[i] != 'None':
            message += f"<td>{product_size_comment_list[i]}</td>"
        else:
            message += "<td>-</td>"
        message += "</tr>"
    
    message += "</table>"
    message += "<br><br><br>" 
    message += f"Сумма заказа: {order.product_price_total}₽<br>"
    message += "Powered by The Woman©"

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    server.sendmail(gmail_user, to_email, msg.as_string())

    # Завершение сеанса
    server.quit()

"""
def product_detail(request, slug, size):
    product = Product.objects.filter(slug=slug, size=size).first()
    return render(request, 'product_detail.html', {'product': product, 'size': size})
"""


def main(request):
    advertisement = Advertisement.objects.first()
    return render(request, 'main.html', {'title': 'Главная', 'advertisement': advertisement})


def contacts(request):
    return render(request, 'contacts.html', {'title': 'Контакты / Доставка'})


def about_us(request):
    return render(request, 'about_us.html', {'title': 'О нас / Условия сотрудничества'})


def policy(request):
    return render(request, 'policy.html', {'title': 'Политика конфиденциальности'})


def product_detail(request, slug, article, size):
    product = Product.objects.filter(slug=slug, article=article, size=size).first()
    group_products = Product.objects.filter(article=product.article)
    inventories = Inventory.objects.filter(product=product)
    context = {
        'product': product,
        'group_products': group_products,
        'article': article,
        'size': size,
        'inventories': inventories,
        'title': product.name
    }
    if product.get_absolute_url() is not None:
        return render(request, 'product_detail.html', context)
    else:
        # Обработка случая, когда нет slug или других значений
        return render(request, 'product_not_available.html')  # Создайте шаблон для этой ситуации


def product_detail1(request, slug, article, size):
    product = Product.objects.filter(slug=slug, article=article, size=size).first()
    group_products = Product.objects.filter(article=product.article)
    inventories = Inventory.objects.filter(product=product)
    context = {
        'product': product,
        'group_products': group_products,
        'article': article,
        'size': size,
        'inventories': inventories,
        'title': product.name
    }
    if product.get_absolute_url() is not None:
        return render(request, 'product_detail.html', context)
    else:
        # Обработка случая, когда нет slug или других значений
        return render(request, 'product_not_available.html')  # Создайте шаблон для этой ситуации


def product_detail2(request, slug, article, size):
    product = Product.objects.filter(slug=slug, article=article, size=size).first()
    group_products = Product.objects.filter(article=product.article)
    inventories = Inventory.objects.filter(product=product)
    context = {
        'product': product,
        'group_products': group_products,
        'article': article,
        'size': size,
        'inventories': inventories,
        'title': product.name
    }
    if product.get_absolute_url() is not None:
        return render(request, 'product_detail.html', context)
    else:
        # Обработка случая, когда нет slug или других значений
        return render(request, 'product_not_available.html')


def product_detail3(request, slug, article, size):
    product = Product.objects.filter(slug=slug, article=article, size=size).first()
    group_products = Product.objects.filter(article=product.article)
    inventories = Inventory.objects.filter(product=product)
    context = {
        'product': product,
        'group_products': group_products,
        'article': article,
        'size': size,
        'inventories': inventories,
        'title': product.name
    }
    if product.get_absolute_url() is not None:
        return render(request, 'product_detail.html', context)
    else:
        # Обработка случая, когда нет slug или других значений
        return render(request, 'product_not_available.html')


def product_detail4(request, slug, article, size):
    product = Product.objects.filter(slug=slug, article=article, size=size).first()
    group_products = Product.objects.filter(article=product.article)
    inventories = Inventory.objects.filter(product=product)
    context = {
        'product': product,
        'group_products': group_products,
        'article': article,
        'size': size,
        'inventories': inventories,
        'title': product.name
    }
    if product.get_absolute_url() is not None:
        return render(request, 'product_detail.html', context)
    else:
        # Обработка случая, когда нет slug или других значений
        return render(request, 'product_not_available.html')


def product_detail5(request, slug, article, size):
    product = Product.objects.filter(slug=slug, article=article, size=size).first()
    group_products = Product.objects.filter(article=product.article)
    inventories = Inventory.objects.filter(product=product)
    context = {
        'product': product,
        'group_products': group_products,
        'article': article,
        'size': size,
        'inventories': inventories,
        'title': product.name
    }
    if product.get_absolute_url() is not None:
        return render(request, 'product_detail.html', context)
    else:
        # Обработка случая, когда нет slug или других значений
        return render(request, 'product_not_available.html')


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = 'price'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = ['C', 'B', 'D', 'B, C', 'NoneSize']

        # Добавить параметры фильтров и флаги активности в контекст
        context['is_new_key'] = self.request.GET.get('is_new_key', '')
        context['is_in_stock_key'] = self.request.GET.get('is_in_stock_key', '')
        context['color_exists'] = self.request.GET.getlist('color_exists')
        context['selected_sizes'] = self.request.GET.getlist('size[]')
        context['is_sale'] = self.request.GET.get('is_sale', '')

        # Добавить флаги активности фильтров в контекст
        context['is_new_key_active'] = bool(context['is_new_key'])
        context['is_in_stock_key_active'] = bool(context['is_in_stock_key'])
        context['color_exists_active'] = bool(context['color_exists'])
        context['is_sale_active'] = bool(context['is_sale'])

        sort = self.request.GET.get('sort')
        if sort is None or sort == '':
            context['products'] = context['products'].order_by('is_sale', '-last_in_stock_change')
        else:
            context['products'] = context['products']
        paginator = Paginator(context['products'], 24)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['title'] = "Erotica"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Применить фильтры, если они переданы в GET-параметрах
        filters = {}
        if not search_query:
        # Применить фильтр по категории только если нет поискового запроса
            queryset = queryset.filter(category__name="Erotica").exclude(color="Синий")
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by()

        if search_query:
            # Filter the queryset to match the search query by article and name
            queryset = queryset.filter(
                Q(article__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        is_new_key = self.request.GET.get('is_new_key')
        if is_new_key:
            filters['is_in_new_key'] = is_new_key

        queryset = queryset.exclude(name__icontains="Шаблон")

        # Исключить продукты с is_in_stock_key равным "Нет в наличии"
        filters['is_in_stock_key'] = 'Есть в наличии'

        color_exists = self.request.GET.getlist('color_exists')
        if color_exists:
            filters['color_exist__name__in'] = color_exists

        err_size = 'B,C'
        
        selected_sizes = self.request.GET.getlist('size[]')
        if selected_sizes:
            if err_size in selected_sizes:
                for i, size in enumerate(selected_sizes):
                    selected_sizes[i] = size.replace(', ', ',')
                filters['size__in'] = selected_sizes
            else:
                filters['size__in'] = selected_sizes

        is_sale = self.request.GET.get('is_sale')
        if is_sale:
            filters['is_sale'] = is_sale

        clear_filter = self.request.GET.get('clear_filter')
        if clear_filter:
            filters.clear()

        return queryset.filter(**filters).distinct()


class ProductListView1(ListView):
    model = Product
    template_name = 'product_list_1.html'
    context_object_name = 'products'
    ordering = 'price'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = ['C', 'B', 'D', 'B, C', 'NoneSize']

        # Добавить параметры фильтров и флаги активности в контекст
        context['is_new_key'] = self.request.GET.get('is_new_key', '')
        context['is_in_stock_key'] = self.request.GET.get('is_in_stock_key', '')
        context['color_exists'] = self.request.GET.getlist('color_exists')
        context['selected_sizes'] = self.request.GET.getlist('size[]')
        context['is_sale'] = self.request.GET.get('is_sale', '')

        # Добавить флаги активности фильтров в контекст
        context['is_new_key_active'] = bool(context['is_new_key'])
        context['is_in_stock_key_active'] = bool(context['is_in_stock_key'])
        context['color_exists_active'] = bool(context['color_exists'])
        context['is_sale_active'] = bool(context['is_sale'])

        sort = self.request.GET.get('sort')
        if sort is None or sort == '':
            context['products'] = context['products'].order_by('-last_in_stock_change')
        else:
            context['products'] = context['products']
        paginator = Paginator(context['products'], 24)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['title'] = "Panties"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Применить фильтры, если они переданы в GET-параметрах
        filters = {}
        if not search_query:
        # Применить фильтр по категории только если нет поискового запроса
            queryset = queryset.filter(Q(category__name="Panties") | Q(color="Синий"))
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by()

        if search_query:
            # Filter the queryset to match the search query by article and name
            queryset = queryset.filter(
                Q(article__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        is_new_key = self.request.GET.get('is_new_key')
        if is_new_key:
            filters['is_in_new_key'] = is_new_key

        queryset = queryset.exclude(name__icontains="Шаблон")

        # Исключить продукты с is_in_stock_key равным "Нет в наличии"
        filters['is_in_stock_key'] = 'Есть в наличии'

        color_exists = self.request.GET.getlist('color_exists')
        if color_exists:
            filters['color_exist__name__in'] = color_exists
        
        err_size = 'B,C'
        
        selected_sizes = self.request.GET.getlist('size[]')
        if selected_sizes:
            if err_size in selected_sizes:
                for i, size in enumerate(selected_sizes):
                    selected_sizes[i] = size.replace(', ', ',')
                filters['size__in'] = selected_sizes
            else:
                filters['size__in'] = selected_sizes

        is_sale = self.request.GET.get('is_sale')
        if is_sale:
            filters['is_sale'] = is_sale

        clear_filter = self.request.GET.get('clear_filter')
        if clear_filter:
            filters.clear()

        return queryset.filter(**filters).distinct()


class ProductListView2(ListView):
    model = Product
    template_name = 'product_list_2.html'
    context_object_name = 'products'
    ordering = 'price'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = ['C', 'B', 'D', 'B, C', 'NoneSize']

        # Добавить параметры фильтров и флаги активности в контекст
        context['is_new_key'] = self.request.GET.get('is_new_key', '')
        context['is_in_stock_key'] = self.request.GET.get('is_in_stock_key', '')
        context['color_exists'] = self.request.GET.getlist('color_exists')
        context['selected_sizes'] = self.request.GET.getlist('size[]')
        context['is_sale'] = self.request.GET.get('is_sale', '')

        # Добавить флаги активности фильтров в контекст
        context['is_new_key_active'] = bool(context['is_new_key'])
        context['is_in_stock_key_active'] = bool(context['is_in_stock_key'])
        context['color_exists_active'] = bool(context['color_exists'])
        context['is_sale_active'] = bool(context['is_sale'])
        
        sort = self.request.GET.get('sort')
        if sort is None or sort == '':
            context['products'] = context['products'].order_by('is_sale', '-last_in_stock_change')
        else:
            context['products'] = context['products']
        paginator = Paginator(context['products'], 24)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['title'] = "Home"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Применить фильтры, если они переданы в GET-параметрах
        filters = {}
        if not search_query:
        # Применить фильтр по категории только если нет поискового запроса
            queryset = queryset.filter(category__name="Home").exclude(color="Синий")
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by()

        if search_query:
            # Filter the queryset to match the search query by article and name
            queryset = queryset.filter(
                Q(article__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        is_new_key = self.request.GET.get('is_new_key')
        if is_new_key:
            filters['is_in_new_key'] = is_new_key

        queryset = queryset.exclude(name__icontains="Шаблон")

        # Исключить продукты с is_in_stock_key равным "Нет в наличии"
        filters['is_in_stock_key'] = 'Есть в наличии'

        color_exists = self.request.GET.getlist('color_exists')
        if color_exists:
            filters['color_exist__name__in'] = color_exists
        
        err_size = 'B,C'
        
        selected_sizes = self.request.GET.getlist('size[]')
        if selected_sizes:
            if err_size in selected_sizes:
                for i, size in enumerate(selected_sizes):
                    selected_sizes[i] = size.replace(', ', ',')
                filters['size__in'] = selected_sizes
            else:
                filters['size__in'] = selected_sizes

        is_sale = self.request.GET.get('is_sale')
        if is_sale:
            filters['is_sale'] = is_sale

        clear_filter = self.request.GET.get('clear_filter')
        if clear_filter:
            filters.clear()

        return queryset.filter(**filters).distinct()


class ProductListView3(ListView):
    model = Product
    template_name = 'product_list_3.html'
    context_object_name = 'products'
    ordering = 'price'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = ['C', 'B', 'D', 'B, C', 'NoneSize']

        # Добавить параметры фильтров и флаги активности в контекст
        context['is_new_key'] = self.request.GET.get('is_new_key', '')
        context['is_in_stock_key'] = self.request.GET.get('is_in_stock_key', '')
        context['color_exists'] = self.request.GET.getlist('color_exists')
        context['selected_sizes'] = self.request.GET.getlist('size[]')
        context['is_sale'] = self.request.GET.get('is_sale', '')

        # Добавить флаги активности фильтров в контекст
        context['is_new_key_active'] = bool(context['is_new_key'])
        context['is_in_stock_key_active'] = bool(context['is_in_stock_key'])
        context['color_exists_active'] = bool(context['color_exists'])
        context['is_sale_active'] = bool(context['is_sale'])

        sort = self.request.GET.get('sort')
        if sort is None or sort == '':
            context['products'] = context['products'].order_by('is_sale', '-last_in_stock_change')
        else:
            context['products'] = context['products']
        paginator = Paginator(context['products'], 24)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['title'] = "Accessories"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Применить фильтры, если они переданы в GET-параметрах
        filters = {}
        if not search_query:
        # Применить фильтр по категории только если нет поискового запроса
            queryset = queryset.filter(category__name="Accessories").exclude(color="Синий")
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by()

        if search_query:
            # Filter the queryset to match the search query by article and name
            queryset = queryset.filter(
                Q(article__icontains=search_query) |
                Q(name__icontains=search_query)
            )
            

        is_new_key = self.request.GET.get('is_new_key')
        if is_new_key:
            filters['is_in_new_key'] = is_new_key

        queryset = queryset.exclude(name__icontains="Шаблон")

        # Исключить продукты с is_in_stock_key равным "Нет в наличии"
        filters['is_in_stock_key'] = 'Есть в наличии'

        color_exists = self.request.GET.getlist('color_exists')
        if color_exists:
            filters['color_exist__name__in'] = color_exists
        
        err_size = 'B,C'
        
        selected_sizes = self.request.GET.getlist('size[]')
        if selected_sizes:
            if err_size in selected_sizes:
                for i, size in enumerate(selected_sizes):
                    selected_sizes[i] = size.replace(', ', ',')
                filters['size__in'] = selected_sizes
            else:
                filters['size__in'] = selected_sizes

        is_sale = self.request.GET.get('is_sale')
        if is_sale:
            filters['is_sale'] = is_sale

        clear_filter = self.request.GET.get('clear_filter')
        if clear_filter:
            filters.clear()

        return queryset.filter(**filters).distinct()


class ProductListView4(ListView):
    model = Product
    template_name = 'product_list_4.html'
    context_object_name = 'products'
    ordering = 'price'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = ['C', 'B', 'D', 'B, C', 'NoneSize']

        # Добавить параметры фильтров и флаги активности в контекст
        context['is_new_key'] = self.request.GET.get('is_new_key', '')
        context['is_in_stock_key'] = self.request.GET.get('is_in_stock_key', '')
        context['color_exists'] = self.request.GET.getlist('color_exists')
        context['selected_sizes'] = self.request.GET.getlist('size[]')
        context['is_sale'] = self.request.GET.get('is_sale', '')

        # Добавить флаги активности фильтров в контекст
        context['is_new_key_active'] = bool(context['is_new_key'])
        context['is_in_stock_key_active'] = bool(context['is_in_stock_key'])
        context['color_exists_active'] = bool(context['color_exists'])
        context['is_sale_active'] = bool(context['is_sale'])

        sort = self.request.GET.get('sort')
        if sort is None or sort == '':
            context['products'] = context['products'].order_by('is_sale', '-last_in_stock_change')
        else:
            context['products'] = context['products']
        paginator = Paginator(context['products'], 24)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['title'] = "Kaurs Laurel & Mandhari & Eva Lelari"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Применить фильтры, если они переданы в GET-параметрах
        filters = {}
        if not search_query:
        # Применить фильтр по категории только если нет поискового запроса
            queryset = queryset.filter(category__name="KME").exclude(color="Синий")
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by()

        if search_query:
            # Filter the queryset to match the search query by article and name
            queryset = queryset.filter(
                Q(article__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        is_new_key = self.request.GET.get('is_new_key')
        if is_new_key:
            filters['is_in_new_key'] = is_new_key

        queryset = queryset.exclude(name__icontains="Шаблон")

        # Исключить продукты с is_in_stock_key равным "Нет в наличии"
        filters['is_in_stock_key'] = 'Есть в наличии'

        color_exists = self.request.GET.getlist('color_exists')
        if color_exists:
            filters['color_exist__name__in'] = color_exists
        
        err_size = 'B,C'
        
        selected_sizes = self.request.GET.getlist('size[]')
        if selected_sizes:
            if err_size in selected_sizes:
                for i, size in enumerate(selected_sizes):
                    selected_sizes[i] = size.replace(', ', ',')
                filters['size__in'] = selected_sizes
            else:
                filters['size__in'] = selected_sizes

        is_sale = self.request.GET.get('is_sale')
        if is_sale:
            filters['is_sale'] = is_sale

        clear_filter = self.request.GET.get('clear_filter')
        if clear_filter:
            filters.clear()

        return queryset.filter(**filters).distinct()


class ProductListView5(ListView):
    model = Product
    template_name = 'product_list_5.html'
    context_object_name = 'products'
    ordering = 'price'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = ['C', 'B', 'D', 'B, C', 'NoneSize']

        # Добавить параметры фильтров и флаги активности в контекст
        context['is_new_key'] = self.request.GET.get('is_new_key', '')
        context['is_in_stock_key'] = self.request.GET.get('is_in_stock_key', '')
        context['color_exists'] = self.request.GET.getlist('color_exists')
        context['selected_sizes'] = self.request.GET.getlist('size[]')
        context['is_sale'] = self.request.GET.get('is_sale', '')

        # Добавить флаги активности фильтров в контекст
        context['is_new_key_active'] = bool(context['is_new_key'])
        context['is_in_stock_key_active'] = bool(context['is_in_stock_key'])
        context['color_exists_active'] = bool(context['color_exists'])
        context['is_sale_active'] = bool(context['is_sale'])

        sort = self.request.GET.get('sort')
        if sort is None or sort == '':
            context['products'] = context['products'].order_by('is_sale', '-last_in_stock_change')
        else:
            context['products'] = context['products']
        paginator = Paginator(context['products'], 24)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)

        context['page_obj'] = page_obj
        context['title'] = "Пляжная одежда"

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        # Применить фильтры, если они переданы в GET-параметрах
        filters = {}
        if not search_query:
        # Применить фильтр по категории только если нет поискового запроса
            queryset = queryset.filter(category__name="Beachwear").exclude(color="Синий")
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by()

        if search_query:
            # Filter the queryset to match the search query by article and name
            queryset = queryset.filter(
                Q(article__icontains=search_query) |
                Q(name__icontains=search_query)
            )

        is_new_key = self.request.GET.get('is_new_key')
        if is_new_key:
            filters['is_in_new_key'] = is_new_key

        queryset = queryset.exclude(name__icontains="Шаблон")

        # Исключить продукты с is_in_stock_key равным "Нет в наличии"
        filters['is_in_stock_key'] = 'Есть в наличии'

        color_exists = self.request.GET.getlist('color_exists')
        if color_exists:
            filters['color_exist__name__in'] = color_exists
        
        err_size = 'B,C'
        
        selected_sizes = self.request.GET.getlist('size[]')
        if selected_sizes:
            if err_size in selected_sizes:
                for i, size in enumerate(selected_sizes):
                    selected_sizes[i] = size.replace(', ', ',')
                filters['size__in'] = selected_sizes
            else:
                filters['size__in'] = selected_sizes

        is_sale = self.request.GET.get('is_sale')
        if is_sale:
            filters['is_sale'] = is_sale

        clear_filter = self.request.GET.get('clear_filter')
        if clear_filter:
            filters.clear()

        return queryset.filter(**filters).distinct()


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        size = request.POST.get('size')
        print(size)

        for choice in product.COLOR_CHOICES:
            color = choice[0]
            color_quantity = int(request.POST.get(f'quantity_{color}', 0))
            print(color_quantity)
            if color_quantity > 0:
                cart_item_key = f'{product_id}_{color}_{size}'
                cart_item = cart.get(cart_item_key, {'quantity': 0})
                cart_item['quantity'] += color_quantity
                cart[cart_item_key] = cart_item

        request.session['cart'] = cart
        return redirect('cart')

    return render(request, 'product_detail.html', {'product': product, 'mainimage': product.mainimage})


"""
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_quantity = 0
    total_price = 0

    for cart_item_key, item in cart.items():
        product_id, color = cart_item_key.split('_')
        product = get_object_or_404(Product, pk=int(product_id))
        quantity = item['quantity']
        price = product.price * quantity
        total_quantity += quantity
        total_price += price
        cart_items.append({
            'product': product,
            'color': color,
            'quantity': quantity,
            'price': price,
            'product_name_with_color': f"{product.name} ({color})"
        })

    if request.method == 'POST':
        updated_cart = {}
        for cart_item_key in request.POST:
            if cart_item_key.startswith('quantity_'):
                product_id, color = cart_item_key.split('_')[1:]
                new_quantity = int(request.POST[cart_item_key])
                if new_quantity > 0:
                    updated_cart[f"{product_id}_{color}"] = {
                        'quantity': new_quantity
                    }
        request.session['cart'] = updated_cart

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price
    })
"""


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_quantity = 0
    total_price = 0

    invalid_keys = []

    for cart_item_key, item in cart.items():
        product_id, color, size = cart_item_key.split('_')  # Разделяем ключ на product_id, color и size
        try:
            product = Product.objects.get(pk=int(product_id))
        except ObjectDoesNotExist:
            invalid_keys.append(cart_item_key)
            continue
        quantity = item['quantity']
        if size == 'None':
            price = product.price * quantity
            total_quantity += quantity
            total_price += price
            cart_items.append({
                'product': product,
                'color': color,
                'quantity': quantity,
                'price': price,
                'size': size,  # Добавляем размер в контекст
                'product_name_with_color': f"{product.name}\n({color})"
            })
        else:
            price = (product.price / product.num_of_products_in_packet) * quantity
            total_quantity += quantity
            total_price += price
            cart_items.append({
                'product': product,
                'color': color,
                'quantity': quantity,
                'price': price,
                'size': size,  # Добавляем размер в контекст
                'product_name_with_color': f"{product.name}\n({color},\n{size})"
            })
    # Удаляем из корзины несуществующие товары
    for invalid_key in invalid_keys:
        del cart[invalid_key]
    request.session['cart'] = cart

    if request.method == 'POST':
        updated_cart = {}
        for cart_item_key in request.POST:
            if cart_item_key.startswith('quantity_'):
                product_id, color, size = cart_item_key.split('_')[1:]
                new_quantity = int(request.POST[cart_item_key])
                if new_quantity > 0:
                    updated_cart[f"{product_id}_{color}_{size}"] = {
                        'quantity': new_quantity
                    }
        request.session['cart'] = updated_cart

    has_items_in_cart = len(cart) > 0  # Проверяем наличие товаров в корзине

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': int(total_price),
        'has_items_in_cart': has_items_in_cart,
        'title': "Корзина"
    })


@csrf_exempt
def remove_from_cart(request, product_id, color, size):
    product_id = str(product_id)
    cart = request.session.get('cart', {})
    color = urllib.parse.unquote(color)
    cart_item_key = f"{product_id}_{color}_{size}"  # Добавляем размер к ключу
    print(product_id, color, size)
    if cart_item_key in cart:
        del cart[cart_item_key]
        request.session['cart'] = cart
        return redirect('cart')
    else:
        # Обработка случая, когда товар не найден в корзине
        return HttpResponse(f'Товар с параметрами: product_id: {product_id}, color: {color}, size {size} не найден в корзине.',
                            status=400)


"""
@csrf_exempt
def update_cart(request, product_id):
    product_id = str(product_id)
    color = request.POST.get('color')
    cart = request.session.get('cart', {})
    cart_item_key = f"{product_id}_{color}"

    if cart_item_key in cart:
        cart_item = cart[cart_item_key]
        quantity = int(request.POST.get(f"quantity_{product_id}_{color}", cart_item['quantity']))
        if quantity > 0:
            cart_item['quantity'] = quantity
        else:
            del cart[cart_item_key]

    request.session['cart'] = cart

    return redirect('cart')


"""


@csrf_exempt
def update_cart(request, product_id, size):
    product_id = str(product_id)
    color = request.POST.get('color')
    size = str(size)
    print(size)
    cart = request.session.get('cart', {})
    cart_item_key = f"{product_id}_{color}_{size}"

    if cart_item_key in cart:
        cart_item = cart[cart_item_key]
        quantity = int(request.POST.get(f"quantity_{product_id}_{color}_{size}", cart_item['quantity']))
        if quantity > 0:
            cart_item['quantity'] = quantity
        else:
            del cart[cart_item_key]
    else:
        return HttpResponse('Товар не найден в корзине.', status=400)

    request.session['cart'] = cart

    return redirect('cart')


def get_cart_total_quantity(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())
    return total_quantity


"""
def update_cart_item(request, product_id, quantity):
    cart = request.session.get('cart', {})
    cart_item = cart.get(str(product_id), {'quantity': 0})
    if cart_item:
        cart_item['quantity'] = int(quantity)
        request.session['cart'] = cart
    return redirect('cart')
"""


def transfer_folders(request):
    if request.method == 'POST':
        folders = Folder.objects.all()
        for folder in folders:
            source_path = folder.source_path
            target_path = folder.target_path

            if os.path.exists(target_path):
                # Если папка уже существует, удаляем ее
                try:
                    shutil.rmtree(target_path)
                except Exception as e:
                    return render(request, 'not_success_delete.html')
                    pass

            try:
                shutil.copytree(source_path, target_path)
            except Exception as e:
                return render(request, 'not_success.html')
                pass

        return render(request, 'success.html')
    return render(request, 'base_site.html')


@transaction.atomic
def checkout(request):
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cart = request.session.get('cart', {})
        total_quantity = sum(item['quantity'] for item in cart.values())

        with transaction.atomic():
            # Обновление количества товара и сохранение информации о купленных товарах
            products = []
            product_quantities = []
            product_articles = []
            product_images = []
            product_prices = []
            product_sizes = []
            product_comment_sizes = []
            product_num_in_packets = []
            for cart_item_key, item in cart.items():
                product_id, color, size = cart_item_key.split('_')
                product = get_object_or_404(Product, pk=int(product_id))
                product_name = product.name
                product_size = product.size
                product_price = product.price
                product_article = product.article
                product_comment_size = size
                product_quantity = item['quantity']
                product_img = product.mainimage
                product_num_in_packet = product.num_of_products_in_packet
                product_prices.append(str(product_price))
                product_quantities.append(str(product_quantity))
                product_articles.append(str(product_article))
                product_images.append(str(product_img))
                product_sizes.append(str(product_size))
                product_comment_sizes.append(str(product_comment_size))
                product_num_in_packets.append(str(product_num_in_packet))

                # Проверка доступного количества товара каждого цвета
                try:
                    available_quantity = product.inventory.get(color=color).quantity
                    if product_quantity <= available_quantity:
                        product.inventory.filter(color=color).update(quantity=F('quantity') - product_quantity)
                        products.append(f"{product_name} (Цвет: {color})")
                    else:
                        return render(request, 'checkout_error.html',
                                      {'error_message': f'Недостаточное количество товара ({color})'})
                except Inventory.DoesNotExist:
                    return render(request, 'checkout_error.html',
                                  {'error_message': f'Нет доступного количества товара ({color})'})

            product_quantities_str = ', '.join(product_quantities)
            product_articles_str = ', '.join(product_articles)
            product_images_many = ', '.join(product_images)
            product_price_all = ', '.join(product_prices)
            product_size_str = ', '.join(product_sizes)
            product_comment_size_str = ', '.join(product_comment_sizes)
            product_num_in_packet_str = ', '.join(product_num_in_packets)

            total_price_temp = [int(num) for num in product_price_all.split(",")if num]
            total_quantity_temp = [int(num) for num in product_quantities_str.split(",")if num]
            temp_num_of_products_in_packet = [int(num) for num in product_num_in_packet_str.split(",")if num]

            total_price_result = []

            product_comment_parts = product_comment_size_str.split(', ')
            for num1, num2, num3, comment_part in zip(total_price_temp, total_quantity_temp,
                                                      temp_num_of_products_in_packet, product_comment_parts):
                if comment_part != 'None':
                    temp = (num1 / num3) * num2
                else:
                    temp = num1 * num2
                total_price_result.append(temp)

            total_price_result_end = sum(total_price_result)

            # Сохранение информации о заказе
            order = form.save(commit=False)
            order.product_name = ', '.join(products)
            order.product_quantity = product_quantities_str
            order.product_size = product_size_str
            order.total_quantity = total_quantity
            order.product_article = product_articles_str
            order.product_img = product_images_many
            order.product_price_total = total_price_result_end
            order.product_price_for_one = product_price_all
            order.product_comment_size = product_comment_size_str
            order.admin_email_address = 'balayi323161@mail.ru'
            print('Pre_error')
            order.save()
            # try:
            #     send_order_mail(order)
            #     send_order_mail_to_admin(order)
            #     request.session.pop('cart', None)
            #     print('Error')
            # except:
            #smtp = smtplib.SMTP('smtp.mail.ru', 2525)
            #smtp.set_debuglevel(1)
            send_order_mail(order)
            send_order_mail_to_admin(order)
            send_order_mail_to_admin_two(order)
            #smtp.quit()
            request.session.pop('cart', None)
                

        return redirect('checkout_success')

    return render(request, 'checkout.html', {'form': form, 'title': "Оформление заказа"})


def product_detail_page_404(request):
    return render(request, 'product_detail_page_404.html', {'title': 'Страница не найдена'})


def checkout_success(request):
    return render(request, 'checkout_success.html', {'title': "Успешно"})


def checkout_error(request):
    return render(request, 'checkout_error.html', {'title': "Ошибка"})


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('cart')
    
    
def update_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            # Здесь вы можете выполнить обновление продукта, например:
            # product.some_field = some_new_value
            product.save()  # Сохранение продукта

            # Перенаправление на страницу с товарами после успешного обновления
            return redirect('product_list_4')
        except Product.DoesNotExist:
            # Обработка случая, если продукт с указанным ID не существует
            pass

    # Если запрос не POST или произошла ошибка, перенаправьте на другую страницу или верните сообщение об ошибке
    return redirect('not_success')
