# Generated by Django 5.0.3 on 2024-04-08 15:50

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'Пользователь с таким username уже существует.'}, max_length=50, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Электронная почта')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Последняя авторизация')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='Телефон')),
                ('is_banned', models.BooleanField(default=False, verbose_name='Забанен')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Администратор')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('avatar', models.ImageField(upload_to='')),
                ('favorites_place', models.ManyToManyField(related_name='user_subscribers', to='place.place', verbose_name='Избранные посты')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'user',
                'ordering': ['created_at'],
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
