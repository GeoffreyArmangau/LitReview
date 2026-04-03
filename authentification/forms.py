from django import forms
from .models import CustomUser

class CustomSignupForm(forms.ModelForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom d’utilisateur',
        })
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe',
        })
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmer le mot de passe',
        })
    )

    class Meta:
        model = CustomUser
        fields = ("username",)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
