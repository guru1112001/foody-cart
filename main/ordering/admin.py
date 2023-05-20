from django.contrib import admin
from.models import Product,cart,order_info,Address


admin.site.register(Product)
admin.site.register(cart)
admin.site.register(order_info)
admin.site.register(Address)