from django.db import transaction
from rest_framework import serializers

from place.models import Place, PlaceImages, Tag, PlaceContact, FeedBackPlace, FeedBackPlaceImage, Way, WayImage
from route.serializers import RouteInPlaceSerializer
from user.serializers import UserFeedbackPlaceSerializer


class FeedbackPlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackPlaceImage
        fields = ('name', 'file')


class FeedbackPlaceSerializer(serializers.ModelSerializer):
    images = FeedbackPlaceImageSerializer(many=True)
    user = UserFeedbackPlaceSerializer()

    class Meta:
        model = FeedBackPlace
        exclude = ('place', )


class ContactsPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceContact
        exclude = ('place', )


class MainImagePlaceSerializers(serializers.ModelSerializer):

    class Meta:
        model = PlaceImages
        fields = ('name', 'file')


class TagsGetPlacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class TagDetailPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class ListPlacesSerializer(serializers.ModelSerializer):
    images = MainImagePlaceSerializers(many=True)
    rating = serializers.FloatField()
    feedback_count = serializers.IntegerField()
    tags = TagsGetPlacesSerializer(many=True)

    class Meta:
        model = Place
        fields = (
            'id',
            'longitude',
            'latitude',
            'name',
            'short_description',
            'images',
            'rating',
            'work_time',
            'tags',
            'feedback_count'
        )


class WayImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WayImage
        fields = ('name', 'file')


class WaySerializer(serializers.ModelSerializer):
    images = WayImagesSerializer(many=True)

    class Meta:
        model = Way
        fields = ('id', 'info', 'images')


class RetrievePlaceSerializer(serializers.ModelSerializer):
    contacts = ContactsPlaceSerializer(many=True)
    place_feedbacks = FeedbackPlaceSerializer(many=True)
    routes = RouteInPlaceSerializer(many=True)
    images = MainImagePlaceSerializers(many=True)
    tags = TagDetailPlaceSerializer(many=True)
    place_ways = WaySerializer(many=True)

    class Meta:
        model = Place
        fields = (
            'id',
            'longitude',
            'latitude',
            'name',
            'tags',
            'short_description',
            'description',
            'images',
            'work_time',
            'place_feedbacks',
            'rating',
            'place_ways',
            'contacts',
            'routes'
        )


class IncludeFeedbackImageAddedFeedbackPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBackPlaceImage
        fields = ('file', 'is_main', 'name')


class AddedFeedbackPlaceSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(max_length=1000000, allow_null=True, write_only=True))

    def create(self, validated_data):
        images_data = validated_data.pop('images')

        with transaction.atomic():
            feedback_place_object = FeedBackPlace.objects.create(**validated_data)

            feedbacks_images = list()
            for image_data in images_data:
                feedback_image_object = FeedBackPlaceImage(file=image_data, feedback_place=feedback_place_object)
                feedbacks_images.append(feedback_image_object)

            FeedBackPlaceImage.objects.bulk_create(feedbacks_images)

        return feedback_place_object

    class Meta:
        model = FeedBackPlace
        fields = ('stars', 'comment', 'images')
