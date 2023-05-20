from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    

    class Meta:
        model=User
        fields=['first_name','username','email','password1','password2']
        widgets = { 
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your Name '}),
            'username': forms.TextInput(attrs={'placeholder': ' Enter UserName'}),
            'email': forms.TextInput(attrs={'placeholder': ' Enter Email'}),
    
        }

    def __init__(self, *args, **kwargs): #contructor of a class 
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': ' Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': ' Confirm Password'})
