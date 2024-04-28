from django.contrib import admin

from route.models import Route, FeedBackRoute, RouteImages, FeedBackRouteImage, RoutePlace


class RouteImagesInline(admin.StackedInline):
    model = RouteImages
    extra = 0


class PlaceInRouteInline(admin.StackedInline):
    model = RoutePlace
    extra = 0


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'title',
        'is_visible'
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_visible', )
    ordering = ('created_at', 'updated_at')
    search_fields = ('title', )
    readonly_fields = ('updated_at', 'created_at', 'id')

    fieldsets = (
            (
                'Главная информация',
                {
                    'fields': (
                        'id',
                        'title',
                        'description',
                        'short_description',
                        'travel_time',
                        'distance',
                        'is_visible',
                        'created_at',
                        'updated_at'
                    )
                },
            ),
        )
    inlines = (RouteImagesInline, PlaceInRouteInline)


class FeedBackRouteImagesInline(admin.StackedInline):
    model = FeedBackRouteImage
    extra = 0


@admin.register(FeedBackRoute)
class FeedBackRouteAdmin(admin.ModelAdmin):
    inlines = (FeedBackRouteImagesInline, )
    list_display = (
        "id",
        'comment'[:15],
        'stars',
        'user',
        'route'
    )
    list_display_links = ('id', 'comment')
