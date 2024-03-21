from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from .models import Request, Employee, RequestUpdate

#create a user

class CreateUserForm(UserCreationForm):
    fullName = forms.CharField(required=True)
    workEmail = forms.EmailField(required=True)
    lineManager = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, empty_label="Select Line Manager (if any)")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'fullName', 'workEmail', 'lineManager']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['lineManager'].queryset = Employee.objects.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create the employee profile
            employee = Employee.objects.create(
                user=user,
                fullName=self.cleaned_data['fullName'],
                workEmail=self.cleaned_data['workEmail'],
                lineManager=self.cleaned_data.get('lineManager')  # Get the lineManager if provided
            )
        return user
    

#login a user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class CreateRequest(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request', 'request_type']
        

class UpdateRequest(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request', 'request_type']

class RequestUpdateForm(forms.ModelForm):
    class Meta:
        model = RequestUpdate
        fields = ['update_text']