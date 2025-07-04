from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import aauthenticate
from django import forms 
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # add more if needed

    # Optional: hide password input
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

