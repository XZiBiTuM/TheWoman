from .models import Cart, CartItem


def cart_items(request):
    cart = request.session.get('cart', {})
    cart_items_count = len(cart)  # Получаем количество элементов в корзине

    return {'cart_items': cart_items_count}
