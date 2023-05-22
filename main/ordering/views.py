from django.shortcuts import render

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from .models import cart, order_info, Product, Address
from acc_profile.models import Customer
from .decorators import admin_only, user_only
from .forms import add_productform, cartform, checkoutform
from django. contrib import messages
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import datetime




@user_only
def homepage(request):
    return render(request, "ordering/home.html")


@user_only
def menu(request):
    return render(request, "ordering/menu.html")


@login_required
def breakfast(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "ordering/breakfast.html", context)


@login_required
def lunch(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "ordering/lunch.html", context)


@login_required
def todayspl(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "ordering/todayspl.html", context)


def ProductDetailView(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {"product": product}
    return render(request, "ordering/ProductDetailView.html", context)


def add_to_cart(request, pk):
    customer_obj = Customer.objects.get(user=request.user)
    product = Product.objects.get(id=pk)
    order_item, created = cart.objects.get_or_create(
        product=product, user=customer_obj, complete=False)
    order_qs = order_info.objects.filter(customer=customer_obj, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__id=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        order = order_info.objects.create(customer=customer_obj)
        order.products.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")
    # customer_obj = Customer.objects.get(user=request.user)
    # product=get_object_or_404(Product,id=pk)
    # order_item,created=cart.objects.get_or_create(product=product,user=customer_obj,complete=False)
    # order_qs=order_info.objects.get_or_create(customer=customer_obj,complete=False)
    # print("order qs : ", order_qs)
    # if order_qs:
    #     order=order_qs[0]
    #     # print("order info product : ", order_qs.product.all())
    #     if order_info.objects.filter(product=product).exists():
    #     # if order.product.filter(product__pk=product.pk).exists():
    #         order_item.quantity+=1
    #         order_item.save()
    #         messages.info(request, "This item quantity was updated.")
    #         return redirect("Productdetail", id=product.pk)
    #     else:
    #      order.product.add(order_item)
    #      messages.info(request, "This item was added to your cart.")
    #     return redirect("Productdetail", id=product.pk)
    # else:
    #     order=order_info.objects.create(customer=customer_obj)
    #     order.product.add(order_item)
    #     messages.info(request, "This item was added to your cart.")
    #     return redirect("Productdetail", id=product.pk)


def remove_from_cart(request, pk):
    customer_obj = Customer.objects.get(user=request.user)
    product = Product.objects.get(id=pk)
    # order_item, created = cart.objects.get_or_create(product=product, user=customer_obj, complete=False)
    order_qs = order_info.objects.filter(customer=customer_obj, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item = cart.objects.filter(
                product=product,
                user=customer_obj,
                complete=False
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary")

    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary")


def remove_single_from_cart(request, pk):
    customer_obj = Customer.objects.get(user=request.user)
    product = Product.objects.get(id=pk)
    # order_item, created = cart.objects.get_or_create(product=product, user=customer_obj, complete=False)
    order_qs = order_info.objects.filter(customer=customer_obj, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item = cart.objects.filter(
                product=product,
                user=customer_obj,
                complete=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item was update from .")
                return redirect("order-summary")
            else:
                order.products.remove(order_item)
                return redirect("Productdetail", id=product.pk)

        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary")

    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary")

# def order_summary(request):
#     customer_obj = Customer.objects.get(user=request.user)
#     orders=order_info.objects.get(customer=customer_obj,complete=False)
#     context={"orders":orders}
#     return render(request,"ordering/order_summary.html",context)


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        customer_obj = Customer.objects.get(user=self.request.user)
        try:
            order = order_info.objects.get(
                customer=customer_obj, complete=False)
            context = {
                'object': order
            }
            return render(self.request, 'ordering/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("menu")


# def checkoutview(request):
#     customer_obj = Customer.objects.get(user=request.user)
#     form=checkoutform()
#     if request.method == "POST":
#         form= checkoutform(request.POST)
#         if form.is_valid():
#             # form.save()
#             orders = order_info.objects.filter(customer=customer_obj, complete=False)[0]
#             print("orders : ", orders)
#             orders.take_away = True
#             orders.complete = True
#             orders.save()
#             clean_data = form.cleaned_data
#             obj = Address.objects.create(**clean_data)
#             obj.customer = customer_obj
#             obj.save()
#             # cart_obj = cart.objects.filter(user=customer_obj)
#             # cart_obj.delete()
#             return redirect("menu")

#     else:
#         form=checkoutform()
#     return render(request,"ordering/checkout.html",{"form":form, "customer":customer_obj})

def checkoutview(request):
    unique_number = str(round(datetime.datetime.now().timestamp()))
    slic = slice(6)
    transaction_id = unique_number[slic]
    customer_obj = Customer.objects.get(user=request.user)
    order = order_info.objects.get(customer=customer_obj, complete=False)

    form = checkoutform()
    if request.method == "POST":
        form = checkoutform(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            obj = Address.objects.create(**clean_data)
            obj.customer = customer_obj
            obj.save()
            # todo return redirect to payment view
            order_items = order.products.all()
            order_items.update(complete=True)
            for item in order_items:
                item.save()

            order.complete = True
            order.take_away = True
            order.transaction_id = transaction_id
            # print(transaction_id)
            order.save()

            messages.info(
                request, "your order has been placed and your transaction id is"+str(transaction_id))

        return redirect("success", id=order.id)
    return render(request, "ordering/checkout.html", {"form": form, "customer": customer_obj, "order": order})


def success(request, id):

    customer_obj = Customer.objects.get(user=request.user)
    order = order_info.objects.get(customer=customer_obj, id=id)
    address_obj = Address.objects.filter(customer=customer_obj).latest("id")
    customer_email = customer_obj.email
    customer_name = customer_obj.name

    t_id = order.transaction_id
    rollment_no = address_obj.Enrollment_no
    sem = address_obj.Semester
    course = address_obj.course


   
    context = {'customer_email': customer_email, 'customer_name': customer_name,
               't_id': t_id, 'rollment_no': rollment_no, 'sem': sem, 'course': course, 'order': order}
    template=render_to_string("ordering/email_template.html",context)
    email=EmailMessage(
       "Thank you for your purchase",
       template,
       settings.EMAIL_HOST_USER,
       [customer_email],
   )
    email.fail_silently=False
    email.content_subtype = 'html'
    email.send()
    return render(request, 'ordering/success.html', context)



@admin_only
def Dashboard(request):
    orders_info = order_info.objects.all()
    print(orders_info)
    carts = cart.objects.all()
    print(carts)
    products = Product.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_order = orders_info.count()
    take_away = orders_info.filter(take_away="True").count()
    payment = orders_info.filter(complete="True").count()

    context = {"orders_info": orders_info, "carts": carts, "products": products, "customers": customers,
               "total_customer": total_customer, "total_order": total_order, "take_away": take_away, "payment": payment}

    return render(request, "ordering/dashboard.html", context)


@admin_only
def add_product(request):
    form = add_productform()
    if request.POST:
        form = add_productform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {"form": form}
    return render(request, "ordering/add_product.html", context)


@admin_only
def view_product(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "ordering/view_product.html", context)


@admin_only
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = add_productform(instance=product)

    if request.POST:
        form = add_productform(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {"form": form}
    return render(request, "ordering/update_product.html", context)


@admin_only
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('view_product')

    context = {'product': product}
    return render(request, 'ordering/delete_product.html', context)


@admin_only
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.customer_order.all()
    order_count = orders.count()
    carts = cart.objects.all()

    context = {"customer": customer, "orders": orders,
               "order_count": order_count, "carts": carts}
    return render(request, "ordering/customer.html", context)


@admin_only
def delete_order(request, pk, pk_test):
    orders = order_info.objects.get(id=pk)
    carts = cart.objects.get(id=pk_test)
    if request.POST:
        carts.delete()
        if request.POST.get("confirm"):
            return redirect("dashboard")
    context = {"orders": orders, "carts": carts}
    return render(request, "ordering/delete_order.html", context)


@admin_only
def update_order(request, pk_test):
    order = cart.objects.get(id=pk_test)
    form = cartform(instance=order)
    if request.method == "POST":
        form = cartform(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    context = {"form": form}
    return render(request, "ordering/update_order.html", context)
