from django.contrib import admin
from django.utils.functional import cached_property

from place.models import Place, Tag, TagPlace, PlaceImages, PlaceContact, FeedBackPlace, FeedBackPlaceImage, Way, \
    WayImage


class PlaceContactInline(admin.StackedInline):
    model = PlaceContact
    extra = 0


class TagPlaceInline(admin.StackedInline):
    model = TagPlace
    extra = 0


class WayImagesInline(admin.StackedInline):
    model = WayImage
    extra = 0


@admin.register(Way)
class WayAdmin(admin.ModelAdmin):
    inlines = (WayImagesInline, )
    list_display = (
        "id",
        'info',
        'place'
    )
    list_display_links = ('id', 'info')


class PlaceImagesInline(admin.StackedInline):
    model = PlaceImages
    extra = 0


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'name',
        'is_visible'
    )
    list_display_links = ('id', 'name')
    list_filter = ('is_visible', )
    ordering = ('created_at', 'updated_at')
    search_fields = ('name', )
    readonly_fields = ('updated_at', 'created_at', 'id')

    fieldsets = (
            (
                'Главная информация',
                {
                    'fields': (
                        'id',
                        'name',
                        'longitude',
                        'latitude',
                        'description',
                        'short_description',
                        'address',
                        'work_time',
                        'is_visible',
                        'created_at',
                        'updated_at'
                    )
                },
            ),
        )
    inlines = (TagPlaceInline, PlaceImagesInline, PlaceContactInline)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'name'
    )
    list_display_links = ('id', 'name')


class FeedBackPlaceImagesInline(admin.StackedInline):
    model = FeedBackPlaceImage
    extra = 0


@admin.register(FeedBackPlace)
class FeedBackPlaceAdmin(admin.ModelAdmin):
    inlines = (FeedBackPlaceImagesInline, )
    list_display = (
        "id",
        'comment'[:15],
        'stars',
        'user',
        'place'
    )
    list_display_links = ('id', 'comment')
