from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# création de modèles personnalisés pour les utilisateurs
# avec des rôles et des relations de suivi


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec des rôles et des relations de suivi.
    Attributs :
        - role : champ de choix pour différencier les rôles d'utilisateur
          (USER ou DEVELOPER)
        - is_developer : champ booléen indiquant si l'utilisateur
          est un développeur ou non.
    Méthodes :
        - save : gère les groupes d'utilisateurs en fonction du rôle
    """
    ROLE_USER = 'USER'
    ROLE_DEVELOPER = 'DEVELOPER'
    ROLE_CHOICES = [
        (ROLE_USER, 'Utilisateur'),
        (ROLE_DEVELOPER, 'Développeur'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    is_developer = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Gérer les groupes d'utilisateurs en fonction du rôle.
        - Si le rôle est DEVELOPER, l'utilisateur
          est ajouté au groupe "developers".
        - Si le rôle est USER, l'utilisateur
          est ajouté au groupe "users".
        """
        self.is_developer = self.role == self.ROLE_DEVELOPER
        super().save(*args, **kwargs)

        target_group_name = 'developers' if self.is_developer else 'users'
        target_group, _ = Group.objects.get_or_create(name=target_group_name)
        opposite_group_name = 'users' if self.is_developer else 'developers'
        opposite_group = Group.objects.filter(name=opposite_group_name).first()

        if opposite_group:
            self.groups.remove(opposite_group)
        self.groups.add(target_group)

# création de modèle pour les relations de suivi entre les utilisateurs


class UserFollows(models.Model):
    """
    Modèle pour représenter les relations de suivi entre les utilisateurs.
    Attributs :
        - user : utilisateur qui suit
        - followed_user : utilisateur suivi
    """
    user = models.ForeignKey(
        CustomUser,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        CustomUser,
        related_name='followed_by',
        on_delete=models.CASCADE
    )

    class Meta:
        """
        Contraintes d'unicité pour éviter les doublons de suivi.
        """
        unique_together = ('user', 'followed_user')

    def __str__(self):
        """
        Représentation en chaîne de la relation de suivi.
        """
        return f"{self.user.username} suit {self.followed_user.username}"
