from django.db import transaction
from rest_framework import serializers

from place.models import Tag, Place, PlaceImages
from route.models import Route, RouteImages, FeedBackRoute, FeedBackRouteImage


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


class AddedFeedbackRouteSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(max_length=1000000, allow_null=True, write_only=True))

    def create(self, validated_data):
        images_data = validated_data.pop('images')

        with transaction.atomic():
            feedback_route_object = FeedBackRoute.objects.create(**validated_data)

            feedbacks_images = list()
            for image_data in images_data:
                feedback_image_object = FeedBackRouteImage(file=image_data, feedback_route=feedback_route_object)
                feedbacks_images.append(feedback_image_object)

            FeedBackRouteImage.objects.bulk_create(feedbacks_images)

        return feedback_route_object

    class Meta:
        model = FeedBackRoute
        fields = ('stars', 'comment', 'images')
