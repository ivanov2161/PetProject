from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *


class Answer(forms.Form):
    answer = forms.CharField(max_length=128, label='', widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='USER NAME', widget=forms.TextInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))
    email = forms.EmailField(label='E-MAIL', widget=forms.EmailInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))
    password1 = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))
    password2 = forms.CharField(label='REPEAT PASSWORD', widget=forms.PasswordInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='USER NAME', widget=forms.TextInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))


class UploadBook(ModelForm):
    name = forms.CharField(label='TITLE', widget=forms.TextInput(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))
    wholeText = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'}))
    cover = forms.ImageField(label='cover')

    class Meta:
        model = Book
        fields = ['name', 'wholeText']
