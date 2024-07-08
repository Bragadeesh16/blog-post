from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterFrom(UserCreationForm):
    email=forms.EmailField(widget = forms.EmailInput (attrs={"placeholder": "Enter email-address", "class": "form-control"}),max_length=100,label='Email',required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput (attrs={"placeholder": "Confirm password", "class": "form-control"}))
    class Meta:
        model = CustomUser
        fields = ['email','password1','password2']


class LoginForm(forms.Form):
    email=forms.EmailField(widget = forms.EmailInput(attrs={"placeholder": "Enter email-address", "class": "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "class": "form-control"}))

class PostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['Title','Content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-textarea'}),}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['Content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-textarea'}),}

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['bio']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'custom-textarea'}),}

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']