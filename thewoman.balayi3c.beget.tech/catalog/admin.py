from django.contrib import admin
from .models import *
from django.db import transaction
from random import randint
import random
import copy
import mysql.connector


def copy_selected_models(modeladmin, request, queryset):
    for obj in queryset:
        old_colors = obj.color_exist.all()  # Сохраняем старые цвета
        obj.pk = None
        obj.id = None
        obj.is_first = 0
        obj.save()

        # После сохранения копии объекта Product, создаем ManyToMany связи
        new_product = obj  # Сохраняем новый продукт, чтобы использовать его для создания связей
        product_model = obj.__class__  # Получаем класс модели продукта
        product_instance = product_model.objects.get(id=new_product.id)  # Получаем экземпляр модели с помощью менеджера объектов
        product_instance.color_exist.set(old_colors)  # Устанавливаем новые ManyToMany-связи
    
    
"""
def copy_selected_models(modeladmin, request, queryset):
    for obj in queryset:
        old_colors = obj.color_exist.all()  # Сохраняем старые цвета
        new_product = obj.copy(commit=False)  # Создаем копию объекта Product
        new_product.save()

        # После сохранения копии объекта Product, создаем ManyToMany связи
        new_product.color_exist.set(old_colors)  # Устанавливаем новые ManyToMany-связи

copy_selected_models.short_description = "Копировать выбранные модели"
"""

copy_selected_models.short_description = "Копировать выбранные модели"


@admin.register(Product)  # Замените YourModel на модель, которую хотите скопировать
class Product(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    actions = [copy_selected_models]
    search_fields = ['name', 'article']
    list_display = ('name', 'article', 'category', 'size')
    exclude = ['is_first', 'slug_helper', 'image9', 'image10']  # Сначала сделать шаблон, потом убрать поле!

    def category(self, obj):
        return obj.category.name

    category.short_description = 'Категория'


admin.site.register(Category)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'product_name', 'product_quantity', 'product_article', 'created_at', 'product_image_tag')
    readonly_fields = ('product_image_tag',)


admin.site.register(Inventory)
admin.site.register(Color)
#admin.site.register(Image)
admin.site.register(Type)
admin.site.register(Secondary)
admin.site.register(NameOfClothe)
admin.site.register(Advertisement)
admin.site.register(Folder)

# Автоматический слаг и ен_нейм V
# Убрать price_for_one_position V
# Придумать что то с автоматическим Inventory
# Добавить единный/1 шт. в product_detail V
# Добавить xxl/1 шт. в product_detail V
# Поробовать сделать папки v
# Есть в наличии сделать V
# Сделать создание папок=артикул и сохранения в них фоток V
# Сделать сжатие фоток до 310х465 при загрузке V
