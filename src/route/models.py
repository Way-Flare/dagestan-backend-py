from django.conf import settings
from django.db import models

from common.models import TimeMixinModel, FeedbackMixinModel, ImagesMixinModel, FeedbackEvaluate
from common.storage import OverwriteStorage


class Route(TimeMixinModel, FeedbackEvaluate):
    title = models.CharField('Название', max_length=255)
    short_description = models.TextField('Краткое описание', max_length=1000, blank=True, null=True)
    description = models.TextField('Описание', max_length=5000, null=True, blank=True)
    travel_time = models.TimeField('Время прохождения')
    distance = models.FloatField('Дистанция')
    is_visible = models.BooleanField('Видимость', default=False)

    places = models.ManyToManyField(
        verbose_name='Места',
        to='place.Place',
        through='RoutePlace',
        related_name='place_routes',
    )

    class Meta:
        db_table = 'route'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        abstract = False


class RoutePlace(models.Model):
    route = models.ForeignKey(
        verbose_name='Маршрут', to='Route', on_delete=models.CASCADE, related_name='m2m_route_places', db_index=True
    )
    place = models.ForeignKey(
        verbose_name='Место', to='place.Place', on_delete=models.CASCADE, related_name='m2m_place_routes', db_index=True
    )
    sequence = models.PositiveSmallIntegerField(verbose_name='Очередность места')

    class Meta:
        db_table = 'route_place'
        verbose_name = 'Связь маршрута-места'
        verbose_name_plural = 'Связь маршрутов-мест'


class RouteImages(ImagesMixinModel):
    file = models.ImageField(
        verbose_name='Изображение места',
        max_length=5000,
        storage=OverwriteStorage(),
        upload_to=settings.APP_MEDIA_PATH.format('route'),
    )
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Путь',
        db_index=True
    )

    class Meta:
        db_table = 'route_image'
        verbose_name = 'Изображение пути'
        abstract = False
        verbose_name_plural = 'Изображения путей'

    def __str__(self):
        return f'{self.name[:30]} - {self.route.title}'


class FeedBackRoute(FeedbackMixinModel):
    user = models.ForeignKey(
        verbose_name='Публицист',
        to='user.User',
        on_delete=models.CASCADE,
        related_name='user_feedbacks_route',
        db_index=True,
    )
    route = models.ForeignKey(
        verbose_name='Маршрут',
        to='Route',
        on_delete=models.CASCADE,
        related_name='route_feedbacks',
        db_index=True
    )

    class Meta:
        db_table = 'feedback_route'
        verbose_name = 'Отзыв маршрута'
        verbose_name_plural = 'Отзывы маршрутов'
        abstract = False


class FeedBackRouteImage(ImagesMixinModel):
    feedback_route = models.ForeignKey(
        verbose_name='Отзыв Маршрута',
        to='FeedBackRoute',
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True
    )
    is_main = None

    class Meta:
        db_table = 'feedback_route_image'
        verbose_name = 'Изображение отзыва маршрута'
        verbose_name_plural = 'Изображения отзывов маршрутов'
        abstract = False
