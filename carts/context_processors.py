from .views import _cart_id
from .models import CartItem, Cart


def counter(request):
    cart_count = 0
    if "admin" in request.path:
        return {}
    else:
        try:
            cart = _cart_id(request)
            cart_items = CartItem.objects.all().filter(cart__cart_id=cart)
            # cart = Cart.filter(_cart_id)
            # cart_items = CartItem.objects.all().filter(cart=cart[:1]) 

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except CartItem.DoesNotExist:
            cart_count = 0
    
    return {"cart_count": cart_count}