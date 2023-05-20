from .models import Product,cart,Address
from django.forms import ModelForm 
from django import forms

class add_productform(ModelForm):
    class Meta:
        model=Product
        fields= "__all__"

    def __init__(self,*args,**kwargs):
        super(add_productform, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields['name'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['price'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['category'].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields["description"].widget.attrs.update({
                    "class":"form-control"
            })
            self.fields['image'].widget.attrs.update({
                'class': 'form-control'
            })

class cartform(ModelForm):
    class Meta():
        model=cart
        fields="__all__"

sem_choice=(
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("6","6")
    )

course_choice={
    ("bca","bca"),
    ("bba","bba"),
    ("bcom","bcom")
}
class checkoutform(ModelForm):
    
    class Meta:
        model=Address
        fields="__all__"
        exclude=["customer"]


