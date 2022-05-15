from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class UserRoles:
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'
    USER_ROLES = (
        (ADMIN, ADMIN),
        (USER, USER),
        (MODERATOR, MODERATOR),
    )


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        blank=False,
        max_length=150,
        verbose_name='Логин пользователя',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
        verbose_name='Электронная почта',
    )
    role = models.CharField(
        max_length=77,
        choices=UserRoles.USER_ROLES,
        default=UserRoles.USER,
        blank=False,
        verbose_name='Роль',
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Код подтверждения',
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        verbose_name='О себе',
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        constraints = [
            UniqueConstraint(fields=['email', ], name='email'),
            UniqueConstraint(fields=['username', ], name='username')
        ]
        ordering = ['id']

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR
