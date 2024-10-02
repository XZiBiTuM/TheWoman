import shutil
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
import random
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.dispatch import receiver
import os
from uuid import uuid4
from PIL import Image, ExifTags
from django.core.files import File
import string
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'


class Type(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название типа товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тип товара'


class Secondary(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название типа товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тип второй товара (если комплект)'


class NameOfClothe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название типа товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Название товара'


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Цвет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Цвета'


def generate_unique_folder_name(instance, filename):
    _, ext = os.path.splitext(filename)
    folder_name = f"{instance.article}_{instance.size}_{uuid4().hex}{ext}"
    return folder_name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(blank=True, unique=False, allow_unicode=False,
                            verbose_name='URL (не менять)', max_length=100)  # Удалите unique=True из поля slug
    article = models.CharField(unique=False, max_length=30, verbose_name='Артикул')
    description = models.TextField(verbose_name='Описание товара')
    is_one_to_one = models.BooleanField(default=False, verbose_name='Возможность купить товар поштучно (поставить галочку, если можно купить товар поштучно')
    mainimage = models.ImageField(verbose_name='Главное изображение', upload_to=generate_unique_folder_name)
    color_image1 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image2 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image3 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image4 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image5 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image6 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image7 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image8 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image9 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                     upload_to=generate_unique_folder_name)
    color_image10 = models.ImageField(blank=True, verbose_name='Изображение для главной страницы',
                                      upload_to=generate_unique_folder_name)
    image1 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image2 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image3 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image4 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image5 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image6 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image7 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image8 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image9 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                               upload_to=generate_unique_folder_name)
    image10 = models.ImageField(blank=True, verbose_name='Изображение для страницы с товаром',
                                upload_to=generate_unique_folder_name)
    # images = models.ManyToManyField('Image')
    # group = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена товара (если есть скидка, то указать с учетом скидки)')
    # price_for_one_position = models.DecimalField(max_digits=10, decimal_places=0) #убрать
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара из Каталога')
    name_of_clothe = models.ForeignKey(NameOfClothe, on_delete=models.CASCADE, blank=True,
                                       verbose_name='Название типа одежды (все пункты с таким названием должны совпадать, кроме того случая, когда это комплект), если товар-комплект, то выбрать "Комплект"')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True,
                             verbose_name='Название типа одежды (все пункты с таким названием должны совпадать, кроме того случая, когда это комплект), если товар-комплект, то выбрать название верхней части одежды')
    secondary = models.ForeignKey(Secondary, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Название типа одежды-2 (можно оставить пустым, если это не комплект), если товар-комплект, то выбрать название нижней части одежды')
    num_of_colors = models.PositiveIntegerField(default=1, verbose_name='Количество цветов у товара')
    num_of_products_in_packet = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке')
    is_set = models.BooleanField(default=False, verbose_name='Комплект')
    size_70 = models.CharField(default="70", verbose_name='Название размера в первой ячейке (верхняя часть комплекта или, если не комплект, то просто размер одежды)',
                               max_length=15)
    size_75 = models.CharField(default="75", verbose_name='Название размера во второй ячейке (верхняя часть комплекта или, если не комплект, то просто размер одежды)',
                               max_length=15, blank=True)
    size_80 = models.CharField(default="80", verbose_name='Название размера в третьй ячейке (верхняя часть комплекта или, если не комплект, то просто размер одежды)',
                               max_length=15, blank=True)
    size_85 = models.CharField(default="85", verbose_name='Название размера в четвертой ячейке (верхняя часть комплекта или, если не комплект, то просто размер одежды)',
                               max_length=15, blank=True)
    size_90 = models.CharField(default="90", verbose_name='Название размера в пятой ячейке (верхняя часть комплекта или, если не комплект, то просто размер одежды)',
                               max_length=15, blank=True)
    num_of_size_70 = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (1-я ячейка/вехняя часть комплекта или, если не комплект, то просто размер одежды)')
    num_of_size_75 = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (2-я ячейка/вехняя часть комплекта или, если не комплект, то просто размер одежды)')
    num_of_size_80 = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (3-я ячейка/вехняя часть комплекта или, если не комплект, то просто размер одежды)')
    num_of_size_85 = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (4-я ячейка/вехняя часть комплекта или, если не комплект, то просто размер одежды)')
    num_of_size_90 = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (5-я ячейка/вехняя часть комплекта или, если не комплект, то просто размер одежды)')
    size_xs = models.CharField(default="XS", verbose_name='Название размера в первой ячейке (нижняя часть комплекта)',
                               max_length=15, blank=True)
    size_s = models.CharField(default="S", verbose_name='Название размера во второй ячейке (нижняя часть комплекта)',
                              max_length=15, blank=True)
    size_m = models.CharField(default="M", verbose_name='Название размера в третьй ячейке (нижняя часть комплекта)',
                              max_length=15, blank=True)
    size_l = models.CharField(default="L", verbose_name='Название размера в четвертой ячейке (нижняя часть комплекта)',
                              max_length=15, blank=True)
    size_xl = models.CharField(default="XL", verbose_name='Название размера в пятой ячейке (нижняя часть комплекта)',
                               max_length=15, blank=True)
    num_of_size_xs = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (1-я ячейка/нижняя часть комплекта)')
    num_of_size_s = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (2-я ячейка/нижняя часть комплекта)')
    num_of_size_m = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (3-я ячейка/нижняя часть комплекта)')
    num_of_size_l = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (4-я ячейка/нижняя часть комплекта)')
    num_of_size_xl = models.PositiveIntegerField(default=1, verbose_name='Количество товара в упаковке (5-я ячейка/нижняя часть комплекта)')
    color_exist = models.ManyToManyField('Color', verbose_name='Выберите цвета, которые есть у этого товара')
    COLOR_CHOICES = [
        ('Белый', 'White'),
        ('Бело-красный', 'White-Red'),
        ('Бело-розовый', 'White-Rose'),
        ('Бордовый', 'Vinous'),
        ('Голубой', 'Blue-W'),
        ('Капучино', 'Coffee'),
        ('Красный', 'Red'),
        ('Леопард', 'Leopard'),
        ('Молочный', 'Milk'),
        ('Розовый', 'Rose'),
        ('Синий', 'Blue'),
        ('Черный', 'Black'),
        ('Шампань', 'Champagne'),
        ('Черно-розовый', 'Black-and-Pink'),
        ('Черно-красный', 'Black-and-Red'),
        ('Черно-золотой', 'Black-and-Gold'),
        ('Черно-белый', 'Black-and-White'),
        ('Черно-бежевый', 'Black-and-Beige'),
        ('Фуксия', 'Fuchsia'),
        ('Фиолетовый', 'Purple'),
        ('Темно-зеленый', 'Dark-Green'),
        ('Телесный', 'Flesh'),
        ('Слива', 'Plum'),
        ('Сине-бежевый', 'Blue-and-Beige'),
        ('Серый', 'Gray'),
        ('Салатовый', 'Salad'),
        ('Розы', 'Rose-flowers'),
        ('Пудра', 'Powder'),
        ('Персик', 'Peach'),
        ('Пенка', 'Foam'),
        ('Оранжевый', 'Orange'),
        ('Оливковый', 'Olive'),
        ('Нефрит', 'Jade'),
        ('Мята', 'Mint'),
        ('Красно-бежевый', 'Red-and-Beige'),
        ('Кофе', 'Coffee-ex'),
        ('Изумрудный', 'Emerald'),
        ('Желтый', 'Yellow'),
        ('Джинсовый', 'Denim'),
        ('Бордово-бежевый', 'Burgundy-beige'),
        ('Бело-бежевый', 'White-and-beige'),
        ('Бежевый', 'Beige'),
        ('Бежево-розовый', 'Beige-and-Rose'),
        ('Пастель', 'Pastel'),
        ('Принт', 'Print'),
        ('Терракот', 'Terracot'),
        ('Хаки', 'Khaki'),
        ('Темно-серый', 'Dark-gray'),
        ('Графит', 'Graphite'),
        ('Принт кофе', 'Print-coffee'),
        ('Принт зеленый', 'Pring-green'),
        ('Серо-белый', 'Gray-white'),
        ('Бежевый леопард', 'Beige-leopard'),
        ('Серый леопард', 'Gray-leopard'),
        ('Карамель', 'Caramel'),
        ('Стразы', 'Srtaz'),
        ('Сердца', 'Hearts'),
        ('Дождь', 'Rain'),
        ('Крылья', 'Wings'),
        ('Корона', 'Crown'),
        ('Алмаз', 'Diamond'),
        ('Пчела', 'Bee'),
        ('Глаз', 'Eye'),
        ('Стрекоза', 'Dragonfly'),
        ('Очки', 'Glasses'),
        ('Бирюзовый', 'Turquoise'),
        ('Ярко-розовый', 'Bright-pink'),
        ('Бежево-фисташковый', 'Beige-pistachio'),
        ('Бежево-фуксия', 'Beige-fuchsia'),
        #  Принт и Пастель стили сделать
    ]
    color = models.CharField(max_length=50, choices=COLOR_CHOICES, default='Черный',
                             verbose_name='Выберите основной цвет товара')
    SIZE = (
        ('NoneSize', 'NoneSize'),
        ('A', 'A'),
        ('B', 'B'),
        ('B,C', 'B,C'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    )
    size = models.CharField(max_length=15, choices=SIZE, default='NoneSize', verbose_name="Размер чашки", blank=True)
    IS_IN_STOCK_KEY = (
        ('Есть в наличии', 'Есть в наличии'),
        ('Нет в наличии', 'Нет в наличии'),
    )
    is_in_stock_key = models.CharField(max_length=50, choices=IS_IN_STOCK_KEY, default='Есть в наличии',
                                       verbose_name="Наличие")
    IS_NEW_KEY = (
        ('Новинка', 'Новинка'),
        ('Не новинка', 'Не новинка'),
    )
    is_in_new_key = models.CharField(max_length=30, choices=IS_NEW_KEY, default='Новинка',
                                     verbose_name="Новинка")
    IS_SALE = (
        ('Скидка', 'Скидка'),
        ('Нет скидки', 'Нет скидки'),
    )
    is_sale = models.CharField(max_length=30, choices=IS_SALE, default='Нет скидки',
                               verbose_name="Скидка")
    sale_price = models.DecimalField(max_digits=10, decimal_places=0, default=0,
                                     verbose_name='Если товар продается по скидке, то указать старую цену')
    # en_name = models.CharField(blank=True, max_length=200, verbose_name='URL-2 (не менять)')
    last_in_stock_change = models.DateTimeField(default=timezone.now,
                                                verbose_name='Время последнего редактирования товара (не менять)')  # ===========СНОСИМ
    is_first = models.IntegerField(default=0, verbose_name='Приоритет')
    slug_helper = models.CharField(default='Пусто', max_length=10)
    objects = models.Manager()


    def formatted_description(self):
        return mark_safe(self.description)


    def get_is_in_stock(self):
        return "Есть в наличии" if self.is_in_stock else "Нет в наличии"

    def get_is_new(self):
        return "Новинка" if self.is_new else "Не новинка"

    def get_is_sale(self):
        return "Скидка" if self.is_sale else "Нет скидки"

    class Meta:
        verbose_name_plural = 'Нижнее белье'
        # ordering = ['category', 'name']
        ordering = ['-is_first', '-last_in_stock_change', 'category', 'name']  # ===========СНОСИМ

    def __str__(self):
        return f'{self.name} ({self.article}, {self.size})'

    def get_absolute_url(self):  
        if self.slug and self.article and self.size:
            size = self.size   
            if self.category.name == 'Erotica':
                return reverse('product_detail', args=[self.slug, self.article, size])
            elif self.category.name == 'Panties':
                return reverse('product_detail1', args=[self.slug, self.article, size])
            elif self.category.name == 'Home':
                return reverse('product_detail2', args=[self.slug, self.article, size])
            elif self.category.name == 'Accessories':
                return reverse('product_detail3', args=[self.slug, self.article, size])
            elif self.category.name == 'KME':
                return reverse('product_detail4', args=[self.slug, self.article, size])
            elif self.category.name == 'Beachwear':
                return reverse('product_detail5', args=[self.slug, self.article, size])
        else:
            return None

    def save(self, *args, **kwargs):
        # slug_base = slugify(self.en_name)
        # slug = slug_base
        # counter = 1

        # Проверяем, существует ли комбинация slug и size
        # while Product.objects.filter(slug=slug, article=self.article, size=self.size).exists():
        # slug = f"{slug_base}-{counter}"
        # counter += 1

        # self.slug = slug
        self.last_in_stock_change = timezone.now()
        super(Product, self).save(*args, **kwargs)

        folder_name = f"{self.article}_{self.size}".replace(', ', '')
        folder_path = os.path.join("media", "product_images", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Переместим фотографии из временной директории в созданную папку
        for field in ['mainimage', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8',
                      'image9',
                      'image10',
                      'color_image1', 'color_image2', 'color_image3', 'color_image4', 'color_image5', 'color_image6',
                      'color_image7', 'color_image8', 'color_image9', 'color_image10']:
            image_field = getattr(self, field)
            if image_field:
                image_path = os.path.join("media", str(image_field))
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    if hasattr(img, '_getexif'):
                        exif = img._getexif()
                        if exif is not None:
                            for tag, value in exif.items():
                                tag_name = ExifTags.TAGS.get(tag, tag)
                                if tag_name == 'Orientation':
                                    if value == 3:
                                        img = img.rotate(180, expand=True)
                                    elif value == 6:
                                        img = img.rotate(270, expand=True)
                                    elif value == 8:
                                        img = img.rotate(90, expand=True)

                    width, height = img.size
                    desired_ratio = 3 / 4

                    current_ratio = width / height

                    if current_ratio != desired_ratio:
                        # Рассчитываем новые размеры, чтобы сохранить соотношение 3:4
                        if current_ratio > desired_ratio:
                            new_width = int(height * desired_ratio)
                            left = (width - new_width) // 2
                            right = width - left
                            img = img.crop((left, 0, right, height))
                        else:
                            new_height = int(width / desired_ratio)
                            top = (height - new_height) // 2
                            bottom = height - top
                            img = img.crop((0, top, width, bottom))

                    # Resize the image to 300x400 without losing quality
                    img = img.resize((525, 700), Image.Resampling.LANCZOS)

                    # Save the resized image
                    img.save(image_path)
                    new_image_path = os.path.join(folder_path, os.path.basename(image_field.name))
                    # shutil.move(new_image_path, ex_new_image_path)
                    if not os.path.exists(new_image_path):
                        os.rename(image_path, new_image_path)
                    else:
                        print('Файлы уже созданы')
                    setattr(self, field, new_image_path)

        super(Product, self).save(*args, **kwargs)


class Folder(models.Model):
    name = models.CharField(max_length=100)
    source_path = models.CharField(max_length=200)
    target_path = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Папки (не трогать!)'


"""
    def copy(self, commit=True):
        # Создаем копию объекта Product
        copied_product = Product()
        copied_product.__dict__.update(self.__dict__)
        copied_product.pk = None  # Сбрасываем pk, чтобы создалась новая запись в базе данных
        copied_product.id = None  # Сбрасываем id

        if commit:
            copied_product.save()

        return copied_product
"""


# class Image(models.Model):
# image = models.ImageField(upload_to='product_images')
#
# def __str__(self):
# return self.image.name


class Advertisement(models.Model):
    name = models.CharField(verbose_name='Название рекламы', max_length=200, default='Реклама')  # Удали дефолт
    add = models.ImageField(verbose_name='Изображение релкамы')
    is_active = models.BooleanField(verbose_name='Отображать рекламу')
    url_add = models.URLField(verbose_name='Ссылка на событие', default='example.com')

    class Meta:
        verbose_name_plural = 'Реклама'

    def __str__(self):
        return self.name


class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartItem')
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for session: {self.session.session_key}'

    class Meta:
        verbose_name_plural = 'Корзина'


class Inventory(models.Model):
    product = models.ForeignKey(Product, related_name='inventory', on_delete=models.CASCADE,
                                verbose_name='Название товара')
    color = models.CharField(max_length=50, default='Черный', verbose_name='Цвет товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товара с таким цветом')

    def __str__(self):
        return f'Название: {self.product.name}, (Артикул: {self.product.article}, Размер: {self.product.size}, (Цвет: {self.color}), Кол-во: {self.quantity})'

    def has_stock(self):
        return self.quantity > 0

    class Meta:
        verbose_name_plural = 'Цвета товара (количество)'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=100, default=' ')
    session_id = models.CharField(max_length=32)
    color = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart'

    class Meta:
        verbose_name_plural = 'Товары в корзине'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эл. почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.TextField(max_length=200, verbose_name='Адрес')
    product_name = models.CharField(max_length=1000, verbose_name='Название товара')
    product_size = models.CharField(max_length=1000, verbose_name='Размера чашки', default='')
    product_quantity = models.CharField(max_length=2000, verbose_name='Количество товара')
    product_num_in_packet = models.PositiveIntegerField(verbose_name="Количество товара в упаковке", default=1)
    product_article = models.CharField(max_length=2000,
                                       verbose_name='Артикул товара')  # Измените максимальную длину на IntegerField
    product_comment_size = models.CharField(verbose_name='Размер товара поштучно', default='None', max_length=100)
    created_at = models.DateTimeField(null=True, verbose_name='Время создания заказа')
    product_price_total = models.PositiveIntegerField(verbose_name='Общая сумма заказа', default=100)
    product_img = models.CharField(max_length=2000, null=True, verbose_name='Изображение товара')
    product_price_for_one = models.CharField(null=True, verbose_name='Цена за упаковку', max_length=30)
    admin_email_address = models.EmailField(verbose_name='Эл. почта магазина',
                                            default='sales@optombelie.ru')  # Поменять на нужную почту

    def product_image_tag(self):
        if self.product_img:
            return format_html('<img src="{}" width="30px" height="40px">', self.product_img)
        return ''

    product_image_tag.short_description = 'Изображение товара'

    def save(self, *args, **kwargs):
        if not self.product_article:
            # Генерация уникального значения для product_article при сохранении
            self.product_article = self.generate_unique_article()
        if not self.pk:  # начиная с этой строки, сносим все, если что
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def generate_unique_article(self):
        # Логика генерации уникального значения для product_article
        # Возможно, вам потребуется внести соответствующие изменения с учетом требований вашего приложения
        return random.randint(10000, 99999)

    def __str__(self):
        return f"{self.first_name}: {self.product_name}, {self.product_article}, {self.created_at}"

    class Meta:
        verbose_name_plural = 'Заказы (в заказах ничего не менять)'


@receiver(post_save, sender=Product)
def create_inventory(sender, instance, created, **kwargs):
    if created:
        colors = Color.objects.all()
        for color in colors:
            Inventory.objects.create(product=instance, color=color.name, quantity=5000)
