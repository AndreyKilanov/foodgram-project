from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=150, unique=True)
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    email = models.EmailField(db_index=True, max_length=254, unique=True)
    password = models.CharField('password', max_length=50)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(fields=('username', 'email'),
                                    name='unique_follow'),
        )

    def __str__(self) -> str:
        return f'email: {self.email} - username: {self.username}'
