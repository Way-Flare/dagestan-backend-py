# Generated by Django 5.0.3 on 2024-06-20 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_avatar_alter_user_favorites_place'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='users',
        ),
    ]