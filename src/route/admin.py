from django.contrib import admin

from route.models import Route, RoutePlace, FeedBackRoute


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


@admin.register(RoutePlace)
class RoutePlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(FeedBackRoute)
class FeedbackRouteAdmin(admin.ModelAdmin):
    pass
