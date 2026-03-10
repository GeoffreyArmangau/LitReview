from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    """
    Modèle représentant un ticket de critique.
    Attributs :
    - user : utilisateur qui a créé le ticket
    - title : titre du ticket
    - description : description du ticket
    - image : image associée au ticket (optionnelle)
    - time_created : date et heure de création du ticket
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    title = models.CharField(
        max_length=128
    )
    description = models.TextField(
        max_length=2048,
        blank=True
    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )


class Review(models.Model):
    """
    Modèle représentant une critique d'un ticket.
    Attributs :
    - ticket : ticket auquel la critique est associée
    - user : utilisateur qui a créé la critique
    - rating : note de la critique (entre 0 et 5)
    - headline : titre de la critique
    - body : commentaire de la critique (optionnel)
    - time_created : date et heure de création de la critique
    """
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(
        max_length=128
    )
    body = models.TextField(
        max_length=8192,
        blank=True
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )
