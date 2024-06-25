from django.db import models
from django.utils.functional import cached_property


class TimeMixinModel(models.Model):
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class ImagesMixinModel(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=5000,
        blank=True,
        null=True
    )
    file = models.ImageField(
        verbose_name='Изображение',
        max_length=5000,
        blank=True,
    )
    is_main = models.BooleanField('Главное изображение', default=False)
    _file_format = models.CharField(
        verbose_name='Формат изображения', max_length=70,
        editable=False, blank=True, null=True,
        default=None, db_index=True,
    )
    _file_width = models.PositiveIntegerField(
        verbose_name='Ширина изображения', blank=True, null=True,
        editable=False, default=None, db_index=True)
    _file_height = models.PositiveIntegerField(
        verbose_name='Высота изображения', blank=True, null=True,
        editable=False, default=None, db_index=True)

    def __str__(self):
        return f'#{self.id} {self.name}'

    class Meta:
        abstract = True


class FeedbackMixinModel(models.Model):
    stars = models.PositiveIntegerField()
    comment = models.TextField(max_length=5000, null=True, blank=True)
    created_at = models.DateField(
        'Дата создания',
        auto_now_add=True,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class MultiplyImagesMixin:

    @property
    def main_image(self):
        if self.image:
            if not (main_image := list(filter(lambda x: x.is_main, self.image))):
                main_image = self.image
            return main_image[0]

    @property
    def main_image_url(self):
        """Возвращает ссылку на главное изображение."""
        if not self.main_image:
            return ''
        return self.main_image.file.url


class FeedbackEvaluate:

    @property
    def rating(self) -> float:
        feedbacks = self.feedback
        count_feedbacks = len(feedbacks)
        if count_feedbacks == 0:
            return 0
        stars_feedbacks = sum([feedback.stars for feedback in feedbacks])
        return round(stars_feedbacks / count_feedbacks, 2)

    @property
    def feedback_count(self) -> int:
        return len(self.feedback)


class CallCleanMixin:

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)