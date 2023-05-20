from django import template    
from ordering.models import cart,order_info
from acc_profile.models import Customer

register = template.Library()

@register.filter(name="cart_products")
def cart_products(user):
    if user.is_authenticated:
        customer_obj = Customer.objects.get(user=user)
        qs = order_info.objects.filter(customer=customer_obj, complete=False)
        # return {'total_cart': order_info.objects.filter(user=customer_obj,complete=False).count}
        if qs.exists():
            return qs[0].products.count()
    return 0
    # # return {'total_cart': cart.objects.filter(user=customer_obj,complete=False).count}

