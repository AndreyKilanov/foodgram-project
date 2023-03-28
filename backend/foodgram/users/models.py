from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(('first name'), max_length=150, blank=False)
    lastname = models.CharField(('last name'), max_length=150, blank=False)
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    password = models.CharField(('password'), max_length=50)

    # USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_follow'
            ),
        )
