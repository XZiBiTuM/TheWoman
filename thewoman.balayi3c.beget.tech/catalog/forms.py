from django import forms
from .models import Order, Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

    def clean_product_quantity(self):
        product_quantity = self.cleaned_data['product_quantity']
        product_id = self.initial.get('product_id')

        if product_id:
            product = Product.objects.filter(pk=product_id).first()
            if product_quantity > product.quantity:
                raise forms.ValidationError("Количество товара превышает доступное количество.")

        return product_quantity

    def save(self, commit=True):
        order = super().save(commit=False)
        # Дополнительные действия, если необходимо
        if commit:
            order.save()
        return order
