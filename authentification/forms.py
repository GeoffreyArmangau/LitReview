from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")
