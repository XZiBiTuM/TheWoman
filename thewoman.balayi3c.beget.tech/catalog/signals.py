from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import *


@receiver(pre_save, sender=Product)
def update_slug_field(sender, instance, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.slug_helper, allow_unicode=False)  # Предполагается, что вы хотите обновить slug на основе name

