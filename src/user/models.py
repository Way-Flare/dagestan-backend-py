from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from common.models import TimeMixinModel
from user.user_manager import CustomUserManager


class User(TimeMixinModel, AbstractUser):
    first_name = None
    last_name = None
    data_joined = None

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'username',
        max_length=50,
        null=True,
        blank=True,
        validators=[username_validator],
    )
    email = models.EmailField('Электронная почта', blank=True, null=True)
    last_login = models.DateTimeField('Последняя авторизация', auto_now_add=True)
    phone = models.CharField('Телефон', max_length=11, unique=True)
    is_banned = models.BooleanField('Забанен', default=False)
    is_staff = models.BooleanField('Администратор', default=False)
    is_active = models.BooleanField('Активный', default=True)
    avatar = models.ImageField(null=True, blank=True)
    favorites_place = models.ManyToManyField(
        verbose_name='Избранные посты',
        to='place.Place',
        related_name='user_subscribers',
        blank=True
    )

    USERNAME_FIELD = "phone"

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        abstract = False
        db_table = "users"
        ordering = ["created_at"]
