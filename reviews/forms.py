from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre de l’article'}),
            'description': forms.Textarea(attrs={'placeholder': 'Décris l’article'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre de la critique',
            'rating': 'Note',
            'body': 'Commentaire',
        }
        widgets = {
            'headline': forms.TextInput(attrs={'placeholder': 'Titre de la critique', 'autofocus': 'autofocus'}),
            'body': forms.Textarea(attrs={'placeholder': 'Votre commentaire'}),
        }
