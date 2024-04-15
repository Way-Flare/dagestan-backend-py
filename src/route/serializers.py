from rest_framework import serializers

from route.models import Route, RouteImages


class RouteImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteImages
        fields = ('name', 'file')


class RouteInPlaceSerializer(serializers.ModelSerializer):
    images = RouteImagesSerializer(many=True)
    rating = serializers.FloatField()

    class Meta:
        model = Route
        fields = ('id', 'title', 'short_description', 'images', 'rating')