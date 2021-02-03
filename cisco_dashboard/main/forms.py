"""Django forms file
 *  - UserForm          - Used during signup to collect user information
 *  - UserProfileForm   - Used to update or collect user API key information
"""


from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile
from crispy_forms.helper import FormHelper
#from main.models import Network


class UserForm(forms.ModelForm):
    """UserForm form
     *  - username  - User's username
     *  - email     - User's email
     *  - password  - User's password
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        """Meta"""
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    """UserProfileForm form
     *  - apikey    - User's API key
    """
    class Meta:
        """Meta"""
        model = UserProfile
        fields = ('apikey',)
