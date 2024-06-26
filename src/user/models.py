from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from common.models import TimeMixinModel


class User(TimeMixinModel, AbstractUser):
    first_name = None
    last_name = None
    data_joined = None

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        validators=[username_validator],
        error_messages={
            "unique": 'Пользователь с таким username уже существует.',
        },
    )
    email = models.EmailField('Электронная почта', blank=True, null=True, unique=True)
    last_login = models.DateTimeField('Последняя авторизация', blank=True, null=True)
    phone = models.CharField('Телефон', max_length=11, unique=True)
    is_banned = models.BooleanField('Забанен', default=False)
    is_staff = models.BooleanField('Администратор', default=False)
    is_active = models.BooleanField('Активный', default=True)
    avatar = models.ImageField()
    favorites_place = models.ManyToManyField(
        verbose_name='Избранные посты',
        to='place.Place',
        related_name='user_subscribers',
    )

    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        abstract = False
        db_table = "user"
        ordering = ["created_at"]
