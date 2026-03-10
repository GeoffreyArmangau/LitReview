from django import forms
from .models import Ticket, Review

 

class FollowUserForm(forms.Form):
    """
    Formulaire pour suivre un utilisateur.
    Attributs :
    - username : champ de texte pour saisir le nom d'utilisateur à suivre
    """
    username = forms.CharField(
        label="Nom d'utilisateur à suivre",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"})
    )

 

class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer un ticket.
    Attributs :
    - title : champ de texte pour le titre du ticket
    - description : champ de texte pour la description du ticket
    - image : champ de téléchargement pour une image associée au ticket
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Titre de l’article'}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': 'Décris l’article'}
            ),
            'image': forms.ClearableFileInput(
                attrs={'class': 'custom-file-input'}
            ),
        }

 

class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer une critique.
    Attributs :
    - headline : champ de texte pour le titre de la critique
    - rating : champ de sélection pour la note de la critique
    - body : champ de texte pour le commentaire de la critique
    """
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {
            'headline': 'Titre de la critique',
            'rating': 'Note',
            'body': 'Commentaire',
        }
        widgets = {
            'headline': forms.TextInput(
                attrs={'placeholder': 'Titre de la critique'}
            ),
            'body': forms.Textarea(
                attrs={'placeholder': 'Votre commentaire'}
            ),
        }
