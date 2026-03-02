from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
