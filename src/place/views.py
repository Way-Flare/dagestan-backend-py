from django.db.models import Prefetch, When, Case, Exists, Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.generics import ListAPIView

from place.models import Place, PlaceImages, FeedBackPlace
from place.serializers import GetPlacesSerializer


@extend_schema_view(
    get=extend_schema(
        tags=['Пользователи'],
        methods=['GET'],
        description='Получение всех мест (объектов)',
        responses={
            200: OpenApiResponse(
                response=GetPlacesSerializer,
            ),
        }
    )
)
class PlaceListView(ListAPIView):
    serializer_class = GetPlacesSerializer

    def get_queryset(self):
        queryset = Place.objects.prefetch_related('tags').prefetch_related(
            Prefetch(
                'images',
                queryset=PlaceImages.objects.all(),
                to_attr='image'
            ),
            Prefetch(
                'place_feedbacks',
                queryset=FeedBackPlace.objects.all(),
                to_attr='feedback'
            )
        )
        return queryset
