from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Електронна пошта',
        error_messages={
            'required': 'Будь ласка, введіть вашу електронну пошту.',
            'invalid': 'Введіть коректну електронну пошту.'
        }
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Ім’я",
        error_messages={
            'required': 'Будь ласка, введіть ваше ім’я.'
        }
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Логін',
        error_messages={
            'required': 'Будь ласка, введіть логін.',
            'unique': 'Користувач із таким логіном вже існує.'
        }
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Будь ласка, введіть пароль.'
        }
    )
    password2 = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Будь ласка, підтвердіть пароль.'
        }
    )

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Перекладаємо стандартні help_text-и пароля
        self.fields['password1'].help_text = (
            "Ваш пароль має містити щонайменше 8 символів і не бути занадто простим."
        )
        self.fields['password2'].help_text = "Введіть той самий пароль для перевірки."
