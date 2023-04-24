from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(verbose_name='Никнейм',
                                max_length=150, unique=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=150, blank=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150,
                                 blank=False)
    email = models.EmailField(verbose_name='Почта', max_length=254,
                              unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=150)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(fields=('username', 'email'),
                                    name='unique_follow'),
        )

    def __str__(self):
        return self.username
