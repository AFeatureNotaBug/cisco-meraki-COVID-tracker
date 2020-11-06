from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    api_key = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "api_key", "email", "password1", "password2"]