from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = VPNUser 
        fields = UserCreationForm.Meta.fields


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = VPNUser
        fields = ['image', 'first_name', 'last_name']


class CreateWebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['site_name', 'site_link']