from django.db.models import Sum
from rest_framework import serializers

from place.models import Place, PlaceImages, Tag


class MainImagePlaceSerializers(serializers.ModelSerializer):

    class Meta:
        model = PlaceImages
        fields = ('name', 'file')


class TagsGetPlacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class GetPlacesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    feedback_count = serializers.SerializerMethodField()
    tags = TagsGetPlacesSerializer(many=True)

    @staticmethod
    def get_image(obj: Place) -> PlaceImages:
        if obj.image:
            if not (main_image := list(filter(lambda x: x.is_main, obj.image))):
                main_image = obj.image
            return MainImagePlaceSerializers(main_image[0]).data

    @staticmethod
    def get_rating(obj: Place) -> float:
        feedbacks = obj.feedback
        count_feedbacks = len(feedbacks)
        if count_feedbacks == 0:
            return 0
        stars_feedbacks = sum([feedback.stars for feedback in feedbacks])
        return float(stars_feedbacks / count_feedbacks)

    @staticmethod
    def get_feedback_count(obj: Place) -> int:
        return len(obj.feedback)

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
