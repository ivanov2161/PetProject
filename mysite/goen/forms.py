from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Book

CSS_CLASS = 'form-input u-radius-6 u-border-1 u-border-grey-30 u-input u-input-rectangle'


class Answer(forms.Form):
    answer = forms.CharField(max_length=128, label='',
                             widget=forms.TextInput(attrs={'autofocus': True, 'class': CSS_CLASS}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='USER NAME', widget=forms.TextInput(attrs={'class': CSS_CLASS}))
    email = forms.EmailField(label='E-MAIL', widget=forms.EmailInput(attrs={'class': CSS_CLASS}))
    password1 = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': CSS_CLASS}))
    password2 = forms.CharField(label='REPEAT PASSWORD', widget=forms.PasswordInput(attrs={'class': CSS_CLASS}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='USER NAME', widget=forms.TextInput(attrs={'class': CSS_CLASS}))
    password = forms.CharField(label='PASSWORD', widget=forms.PasswordInput(attrs={'class': CSS_CLASS}))


class UploadBook(ModelForm):
    name = forms.CharField(label='TITLE', widget=forms.TextInput(attrs={'class': CSS_CLASS}))
    wholeText = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': CSS_CLASS}))
    cover = forms.ImageField(label='cover', widget=forms.ClearableFileInput)

    class Meta:
        model = Book
        fields = ['name', 'wholeText']
