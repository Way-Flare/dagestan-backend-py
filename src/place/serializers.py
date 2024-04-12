from django.db.models import Sum
from rest_framework import serializers

from place.models import Place, PlaceImages, Tag, PlaceContact
from route.serializers import RouteSerializer


class ContactsPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceContact
        fields = '__all__'


class MainImagePlaceSerializers(serializers.ModelSerializer):

    class Meta:
        model = PlaceImages
        fields = ('name', 'file')


class TagsGetPlacesSerializer(serializers.ModelSerializer):

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


class RetrievePlaceSerializer(serializers.ModelSerializer):
    contacts = ContactsPlaceSerializer(many=True)
    place_routes = RouteSerializer(many=True, label='routes')

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
            'place_routes'
        )
