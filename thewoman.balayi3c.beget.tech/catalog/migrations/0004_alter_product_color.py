# Generated by Django 4.2.1 on 2023-12-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_product_num_of_size_65_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('Белый', 'White'), ('Бело-красный', 'White-Red'), ('Бело-розовый', 'White-Rose'), ('Бордовый', 'Vinous'), ('Голубой', 'Blue-W'), ('Капучино', 'Coffee'), ('Красный', 'Red'), ('Леопард', 'Leopard'), ('Молочный', 'Milk'), ('Розовый', 'Rose'), ('Синий', 'Blue'), ('Черный', 'Black'), ('Шампань', 'Champagne'), ('Черно-розовый', 'Black-and-Pink'), ('Черно-красный', 'Black-and-Red'), ('Черно-золотой', 'Black-and-Gold'), ('Черно-белый', 'Black-and-White'), ('Черно-бежевый', 'Black-and-Beige'), ('Фуксия', 'Fuchsia'), ('Фиолетовый', 'Purple'), ('Темно-зеленый', 'Dark-Green'), ('Телесный', 'Flesh'), ('Слива', 'Plum'), ('Сине-бежевый', 'Blue-and-Beige'), ('Серый', 'Gray'), ('Салатовый', 'Salad'), ('Розы', 'Rose-flowers'), ('Пудра', 'Powder'), ('Персик', 'Peach'), ('Пенка', 'Foam'), ('Оранжевый', 'Orange'), ('Оливковый', 'Olive'), ('Нефрит', 'Jade'), ('Мята', 'Mint'), ('Красно-бежевый', 'Red-and-Beige'), ('Кофе', 'Coffee-ex'), ('Изумрудный', 'Emerald'), ('Желтый', 'Yellow'), ('Джинсовый', 'Denim'), ('Бордово-бежевый', 'Burgundy-beige'), ('Бело-бежевый', 'White-and-beige'), ('Бежевый', 'Beige'), ('Бежево-розовый', 'Beige-and-Rose'), ('Пастель', 'Pastel'), ('Принт', 'Print'), ('Терракот', 'Terracot'), ('Хаки', 'Khaki'), ('Темно-серый', 'Dark-gray'), ('Графит', 'Graphite'), ('Принт кофе', 'Print-coffee'), ('Принт зеленый', 'Pring-green'), ('Серо-белый', 'Gray-white'), ('Бежевый леопард', 'Beige-leopard'), ('Серый леопард', 'Gray-leopard'), ('Карамель', 'Caramel'), ('Стразы', 'Srtaz'), ('Сердца', 'Hearts'), ('Дождь', 'Rain'), ('Крылья', 'Wings'), ('Корона', 'Crown'), ('Алмаз', 'Diamond'), ('Пчела', 'Bee'), ('Глаз', 'Eye'), ('Стрекоза', 'Dragonfly'), ('Очки', 'Glasses'), ('Бирюзовый', 'Turquoise'), ('Ярко-розовый', 'Bright-pink')], default='Черный', max_length=50, verbose_name='Выберите основной цвет товара'),
        ),
    ]
