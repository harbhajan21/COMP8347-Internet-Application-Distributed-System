from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Enter your last name.')
    id_or_photo = forms.ImageField(required=False, help_text='Upload a valid ID or photo.')

    class Meta:
        model = User  # Assuming your User model is named 'User'
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'id_or_photo',)
