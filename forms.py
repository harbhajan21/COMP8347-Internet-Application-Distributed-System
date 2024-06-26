from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class SigninForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
