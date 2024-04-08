from django.contrib import admin

from place.models import Place, Tag, TagPlace, PlaceImages, PlaceContact, FeedBackPlace, FeedBackPlaceImage, Way, \
    WayImage


class TagPlaceInline(admin.TabularInline):
    model = TagPlace
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = (TagPlaceInline, )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceImages)
class PlaceImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(PlaceContact)
class PlaceContactAdmin(admin.ModelAdmin):
    pass


@admin.register(FeedBackPlace)
class FeedBackPlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(FeedBackPlaceImage)
class FeedBackPlaceImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Way)
class WayAdmin(admin.ModelAdmin):
    pass


@admin.register(WayImage)
class WayImageAdmin(admin.ModelAdmin):
    pass
