from rest_framework import serializers

from place.models import Tag, Place, PlaceImages
from route.models import Route, RouteImages


class RouteImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteImages
        fields = ('id', 'name', 'file')


class ImagesInPlaceInRouteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlaceImages
        fields = ('id', 'name', 'file')


class RouteInPlaceSerializer(serializers.ModelSerializer):
    images = RouteImagesSerializer(many=True)
    rating = serializers.FloatField()

    class Meta:
        model = Route
        fields = ('id', 'title', 'short_description', 'images', 'rating')


class MainTagInPlaceInRouteRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PlaceInRouteRetrieveSerializers(serializers.ModelSerializer):
    main_tag = serializers.SerializerMethodField()
    images = ImagesInPlaceInRouteSerializers(many=True)
    sequence = serializers.IntegerField(allow_null=True)

    @staticmethod
    def get_main_tag(obj):
        main_tag = obj.main_tag
        if main_tag:
            return MainTagInPlaceInRouteRetrieveSerializers(main_tag[0]).data

    class Meta:
        model = Place
        fields = (
            'id',
            'images',
            'work_time',
            'main_tag',
            'sequence'
        )


class RouteListSerializers(serializers.ModelSerializer):
    images = RouteImagesSerializer(many=True)
    rating = serializers.FloatField()
    feedback_count = serializers.IntegerField()

    class Meta:
        model = Route
        fields = (
            'id',
            'title',
            'images',
            'short_description',
            'distance',
            'travel_time',
            'feedback_count',
            'rating'
        )


class RetrieveRouteSerializers(serializers.ModelSerializer):
    places = PlaceInRouteRetrieveSerializers(many=True, source='place_annotated')
    rating = serializers.FloatField()
    feedback_count = serializers.IntegerField()
    images = RouteImagesSerializer(many=True)

    class Meta:
        model = Route
        fields = (
            'id',
            'title',
            'images',
            'short_description',
            'description',
            'places',
            'distance',
            'travel_time',
            'feedback_count',
            'rating'
        )
