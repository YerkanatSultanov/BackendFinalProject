from django import forms
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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "book", "rating", "slug", "creator"]
