from django.shortcuts import render
from .models import *
from .form import *
from django.contrib.auth import authenticate, login,logout
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


def register(request):
    form = RegisterFrom()
    if request.method == 'POST':
        form = RegisterFrom(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email = email , password = password)
            print(user)
            login(request,user)
            messages.success(request,"your are signed in successfully")
            return redirect("home")
    else:
        form = RegisterFrom()

    return render(request,'register.html',{'form':form})

def user_login(request):
    form = LoginForm()   
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = form.data['email']
        password = form.data['password']
        user = authenticate(request,email = email , password = password)
        if user is not None:
            print(user)
            login(request,user)
            messages.success(request,"your are logged in successfully")
            return redirect('home')
        else:
            form.add_error(None, _('invalid credentials'))
    return render(request,'login.html',{'form':form})


def signout(request):
    logout(request)
    messages.success(request,"you have been logged out")
    return redirect("home")