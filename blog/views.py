from django.shortcuts import render
from .models import *
from .form import *
from django.contrib.auth import authenticate, login,logout
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator




def home(request):
    p = Paginator(Post.objects.all().order_by('Published_Date'),5)
    page = request.GET.get('page')
    post = p.get_page(page)
    context = {
        'posts':post
        
    }
    return render(request,'home.html',context)


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

@login_required(login_url='login')
def posting(request):
    form = PostFrom()
    if request.method == 'POST':
        form = PostFrom(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Author = request.user
            instance.save()
            return redirect('home')

    else:
        form = PostFrom()

    return render(request,'newpost.html',{'form':form})

@login_required(login_url='login') 
def post_detail(request,slug):

    post = Post.objects.get(slug = slug)
    comment = Comment.objects.filter(Post = post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Post = post
            instance.Author = request.user
            instance.save()
            return redirect('post',post.slug)

    else:
        form = CommentForm()

    context = {
        'posts':post,
        'form':form,
        'comment':comment
    }
    return render(request,'post.html',context)

@login_required(login_url='login')
def profile(request,pk):
    user = CustomUser.objects.get(id = pk)
    user_profile = user.get_profile
    post = Post.objects.filter(Author = pk)
    context = {
        'posts':post,
        'users':user,
        'user_profile_details':user_profile
    }
    return render(request,'profile.html',context)

@login_required(login_url='login')
def UpdateProfile(request,pk):
    user = CustomUser.objects.get(id = pk) 
    profile = user.get_profile

    
    if request.method == 'POST':  
        user_form = CustomUserForm(request.POST, instance = user)
        profile_form = ProfileModelForm(request.POST, instance= profile )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('update-profile', pk=user.id) 
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        user_form = CustomUserForm(instance=user)
        profile_form = ProfileModelForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    } 
    return render(request, 'updateprofile.html', context)
