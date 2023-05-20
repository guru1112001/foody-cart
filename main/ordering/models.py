from django.db import models
from acc_profile.models import Customer
from django.shortcuts import reverse

# Create your models here.

class Product(models.Model):
    options=(("Breakfast","Breakfast"),
    ("Lunch","Lunch"),
    ("Todayspl","Todayspl"),)
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=7,decimal_places=2)
    category=models.CharField(max_length=10,choices=options)
    description=models.TextField(max_length=500)
    image=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    

    
class cart(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=1)
    complete=models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
    @property
    def get_total(self):

        total=self.quantity*self.product.price
        return total
        
class order_info(models.Model):
    
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True,related_name="customer_order")
    date_ordered=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=10)
    products=models.ManyToManyField(cart)
    take_away=models.BooleanField(default=False)

    def __str__(self):
        return self.customer.name
    

    
    @property
    def get_cart_total(self):
        carts = self.products.all()
        total = sum([item.get_total for item in carts])
        return total

    @property
    def get_cart_items(self):
        carts = self.cart_set.all()
        total = sum([item.quantity for item in carts])
        return total
    
course_choice={
    ("bca","bca"),
    ("bba","bba"),
    ("bcom","bcom")
}
sem_choice=(
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("6","6")
    )
class Address(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    Enrollment_no=models.CharField(max_length=15)
    course=models.CharField(max_length=20,choices=course_choice)
    Semester=models.CharField(max_length=20,choices=sem_choice)

    def __str__(self):
        return self.Enrollment_no

