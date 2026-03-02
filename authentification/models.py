from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
	ROLE_USER = 'USER'
	ROLE_DEVELOPER = 'DEVELOPER'

	ROLE_CHOICES = [
		(ROLE_USER, 'Utilisateur'),
		(ROLE_DEVELOPER, 'Développeur'),
	]

	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
	is_developer = models.BooleanField(default=False, editable=False)

	def save(self, *args, **kwargs):
		self.is_developer = self.role == self.ROLE_DEVELOPER
		super().save(*args, **kwargs)

		target_group_name = 'developers' if self.is_developer else 'users'
		target_group, _ = Group.objects.get_or_create(name=target_group_name)
		opposite_group_name = 'users' if self.is_developer else 'developers'
		opposite_group = Group.objects.filter(name=opposite_group_name).first()

		if opposite_group:
			self.groups.remove(opposite_group)
		self.groups.add(target_group)

class UserFollows(models.Model):
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
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"
