from . import views
from django.urls import path
from .views import OrderSummaryView



urlpatterns = [
    path("",views.homepage,name="home"),
    path("menu/",views.menu,name="menu"),
    path("dashboard/",views.Dashboard , name="dashboard"),
    path("add_product/",views.add_product,name="add_product"),
    path("view_product/",views.view_product,name="view_product"),
    path("update_product/<str:pk>",views.update_product,name="update_product"),
    path("customer/<str:pk_test>/",views.customer,name="customer"),
    path('delete_order/<int:pk>/<int:pk_test>/', views.delete_order, name="delete_order"),
    path("update_order/<int:pk_test>/",views.update_order,name="update_order"),
    path("breakfast/",views.breakfast,name="breakfast"),
    path("lunch/",views.lunch,name="lunch"),
    path("todayspl/",views.todayspl,name="todayspl"),
    path("Product/<int:id>/", views.ProductDetailView,name="Productdetail"),
    path('delete_product/<str:pk>', views.deleteProduct, name="delete_product"),
    path('add-to-cart/<int:pk>/',views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart, name='remove-from-cart'),
    # path("order-summary/",views.order_summary,name="order-summary"),
    path("order-summary/",OrderSummaryView.as_view(),name="order-summary"),
    path('remove-item-cart/<int:pk>/',views.remove_single_from_cart, name='remove_single_from_cart'),
    path("checkout/",views.checkoutview,name="checkout"),
    path("success/<int:id>/",views.success,name="success"),





    
]