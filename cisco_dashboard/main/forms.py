from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    api_key = forms.CharFeild()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]