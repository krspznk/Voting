from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Електронна пошта')
    first_name = forms.CharField(max_length=30, required=True, label="Ім’я")

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
