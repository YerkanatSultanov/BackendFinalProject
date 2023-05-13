from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
