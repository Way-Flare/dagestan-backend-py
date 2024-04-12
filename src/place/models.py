from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

from common.models import TimeMixinModel, ImagesMixinModel, CallCleanMixin, FeedbackMixinModel, MultiplyImagesMixin
from common.storage import OverwriteStorage
from place.model_manager import CustomPlaceManager


class Tag(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        db_table = 'tag_place'
        verbose_name = 'Тег места'
        verbose_name_plural = 'Теги мест'

    def __str__(self):
        return self.name[:30]


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

    class Meta:
        db_table = 'tags_places'
        verbose_name = 'Тег места'
        abstract = False
        verbose_name_plural = 'Теги мест'

    def __str__(self):
        return f'{self.tag.name} - {self.place.name}'


class Place(TimeMixinModel, MultiplyImagesMixin):
    name = models.CharField('Название', max_length=255)
    tags = models.ManyToManyField(
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
    work_time = models.CharField('Время работы', max_length=50, null=True, blank=True)
    is_visible = models.BooleanField('Видимость', default=False)

    objects = CustomPlaceManager()

    class Meta:
        db_table = 'place'
        verbose_name = 'Место'
        abstract = False
        verbose_name_plural = 'Места'

    @property
    def feedbacks(self):
        return self.place_feedbacks.all()

    def __str__(self):
        return f'{self.name[:30]} - {self.description[:30]}'


class PlaceImages(ImagesMixinModel, MultiplyImagesMixin):
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

    def __str__(self):
        return f'{self.name[:30]} - {self.place.name}'


class PlaceContact(CallCleanMixin, models.Model):
    phone_number = models.CharField('Номер телефона', max_length=16, blank=True, null=True)
    email = models.EmailField('Адрес электронной почты', blank=True, null=True)
    place = models.ForeignKey(
        verbose_name='Место',
        to='Place',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='contacts'
    )

    def clean(self):
        if not self.phone_number and not self.email:
            raise ValidationError('Одно из полей email или phone_number должно быть не пустым.')

    class Meta:
        db_table = 'place_contact'
        verbose_name = 'Контакт места'
        verbose_name_plural = 'Контакты мест'

    def __str__(self):
        return f'{self.phone_number} - {self.email} - {self.place.name}'


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

    def __str__(self):
        return f'{self.stars} - {self.comment} - {self.place.name}'


class FeedBackPlaceImage(ImagesMixinModel):
    file = models.ImageField(
        verbose_name='Изображение отзыва',
        max_length=5000,
        storage=OverwriteStorage(),
        upload_to=settings.APP_MEDIA_PATH.format('feedback_place'),
    )
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

    def __str__(self):
        return f'{self.name[:30]} - {self.file}'


class Way(models.Model):
    info = models.TextField('Описание', null=True, blank=True)
    place = models.ForeignKey(
        verbose_name='Место',
        to='Place',
        on_delete=models.CASCADE,
        db_index=True,
        related_name='ways_place'
    )

    class Meta:
        db_table = 'way_place'
        verbose_name = 'Описание пути к месту'
        verbose_name_plural = 'Описания пути к местам'

    def __str__(self):
        return f'{self.info[:25]} - {self.place}'


class WayImage(ImagesMixinModel):
    file = models.ImageField(
        verbose_name='Изображение пути',
        max_length=5000,
        storage=OverwriteStorage(),
        upload_to=settings.APP_MEDIA_PATH.format('way'),
    )
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
