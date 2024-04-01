from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from common.models import TimeMixinModel, ImagesMixinModel, CallCleanMixin, FeedbackMixinModel
from common.storage import OverwriteStorage


class Tag(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        db_table = 'category_place'
        verbose_name = 'Категория места'
        verbose_name_plural = 'Категории мест'


class TagPlace(models.Model):
    tag = models.ForeignKey(
        verbose_name='Тег',
        to='Tag',
        on_delete=models.SET_NULL,
        related_name='tag_places',
        db_index=True,
        null=True
    )
    place = models.ForeignKey(
        verbose_name='Место',
        to='Place',
        on_delete=models.CASCADE,
        related_name='place_tags',
        db_index=True
    )
    is_main = models.BooleanField('Главный тег', default=False)


class Place(TimeMixinModel):
    name = models.CharField('Название', max_length=255)
    category = models.ManyToManyField(
        verbose_name='Тег',
        to='Tag',
        through='TagPlace',
        db_index=True,
        related_name='places',
    )
    longitude = models.FloatField('Долгота')
    latitude = models.FloatField('Широта')
    description = models.TextField('Описание', max_length=5000, blank=True, null=True)
    short_description = models.TextField('Краткое описание', max_length=1000, blank=True, null=True)
    address = models.CharField('Адрес места', max_length=300, null=True, blank=True)
    work_time = models.CharField('Время работы', max_length=50)

    class Meta:
        db_table = 'place'
        verbose_name = 'Место'
        abstract = False
        verbose_name_plural = 'Места'


class PlaceImages(ImagesMixinModel):
    file = models.ImageField(
        verbose_name='Изображение места',
        max_length=5000,
        storage=OverwriteStorage(),
        upload_to=settings.APP_MEDIA_PATH.format('place'),
    )
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место',
        db_index=True
    )

    class Meta:
        db_table = 'place_image'
        verbose_name = 'Изображение места'
        abstract = False
        verbose_name_plural = 'Изображения мест'


class PlaceContact(CallCleanMixin, models.Model):
    phone_number = models.CharField('Номер телефона', max_length=16, blank=True, null=True)
    email = models.EmailField('Адрес электронной почты', blank=True, null=True)
    place = models.ForeignKey(verbose_name='Место', to='Place', on_delete=models.CASCADE, db_index=True)

    def clean(self):
        if not self.phone_number and not self.email:
            raise ValidationError('Одно из полей email или phone_number должно быть не пустым.')

    class Meta:
        db_table = 'place_contact'
        verbose_name = 'Контакт места'
        verbose_name_plural = 'Контакты мест'


class FeedBackPlace(FeedbackMixinModel):
    user = models.ForeignKey(
        verbose_name='Публицист',
        to='user.User',
        on_delete=models.CASCADE,
        related_name='user_feedbacks_places',
        db_index=True,
    )
    place = models.ForeignKey(
        verbose_name='Место',
        to='Place',
        on_delete=models.CASCADE,
        related_name='place_feedbacks',
        db_index=True
    )

    class Meta:
        db_table = 'feedback_place'
        verbose_name = 'Отзыв места'
        verbose_name_plural = 'Отзывы мест'
        abstract = False


class FeedBackPlaceImage(ImagesMixinModel):
    feedback_place = models.ForeignKey(
        verbose_name='Отзыв места',
        to='FeedBackPlace',
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True
    )
    is_main = None

    class Meta:
        db_table = 'feedback_place_image'
        verbose_name = 'Изображение отзыва места'
        verbose_name_plural = 'Изображения отзывов мест'
        abstract = False


class Way(models.Model):
    info = models.TextField('Описание', null=True, blank=True)
    place = models.ForeignKey(
        verbose_name='Место',
        to='Place',
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        db_table = 'way_place'
        verbose_name = 'Описание пути к месту'
        verbose_name_plural = 'Описания пути к местам'


class WayImage(ImagesMixinModel):
    way = models.ForeignKey(
        verbose_name='Путь к месту',
        to='Way',
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True
    )
    is_main = None

    class Meta:
        db_table = 'way_place_image'
        verbose_name = 'Изображение пути к месту'
        verbose_name_plural = 'Изображения пути к местам'
        abstract = False
