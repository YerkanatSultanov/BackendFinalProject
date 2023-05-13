from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    category = forms.ChoiceField(required=False,
                                 choices=(
                                     ("title", "Title"),
                                     ("contributor", "Contributor")
                                 ))
