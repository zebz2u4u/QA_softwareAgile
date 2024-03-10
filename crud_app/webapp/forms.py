from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from . models import Request

#create a user

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

#login a user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class CreateRequest(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['fullName', 'workEmail', 'lineManager',
                  'request', 'request_type']
        

class UpdateRequest(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['fullName', 'workEmail', 'lineManager',
                  'request', 'request_type']