# Generated by Django 5.0.3 on 2024-04-01 10:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0002_initial'),
        ('route', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackroute',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_feedbacks_route', to=settings.AUTH_USER_MODEL, verbose_name='Публицист'),
        ),
        migrations.AddField(
            model_name='feedbackrouteimage',
            name='feedback_route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='route.feedbackroute', verbose_name='Отзыв Маршрута'),
        ),
        migrations.AddField(
            model_name='feedbackroute',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_feedbacks', to='route.route', verbose_name='Маршрут'),
        ),
        migrations.AddField(
            model_name='routeplace',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m2m_place_routes', to='place.place', verbose_name='Место'),
        ),
        migrations.AddField(
            model_name='routeplace',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m2m_route_places', to='route.route', verbose_name='Маршрут'),
        ),
        migrations.AddField(
            model_name='route',
            name='places',
            field=models.ManyToManyField(related_name='place_routes', through='route.RoutePlace', to='place.place', verbose_name='Места'),
        ),
    ]