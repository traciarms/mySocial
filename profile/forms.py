from django.forms import ModelForm
from profile.models import Profile

__author__ = 'traciarms'
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileCreationForm(UserCreationForm):
    dob = forms.CharField(max_length=10)
    gender = forms.CharField(max_length=1)
    phone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'dob',
                  'gender', 'phone')


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    dob = forms.CharField(max_length=10)
    gender = forms.CharField(max_length=1)
    phone = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'dob', 'gender', 'phone')

