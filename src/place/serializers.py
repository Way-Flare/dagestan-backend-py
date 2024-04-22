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


class MainTagPlaceInListRoutesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class ListPlacesSerializer(serializers.ModelSerializer):
    image = MainImagePlaceSerializers(source='main_image')
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
            'image',
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
