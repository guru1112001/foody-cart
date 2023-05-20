from django.shortcuts import render,redirect
from .models import Customer
from .forms import CreateUserForm
from django.contrib import messages

def RegisterPage(request):
    form=CreateUserForm()
    if request.method == "POST":
        form= CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            messages.info(request,f"Your Account has been created! you are now able to log-in",username)
            return redirect("login")
    
    else:
        form=CreateUserForm()
    return render(request,"acc_profile/register.html",{"form":form})


