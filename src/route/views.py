from django.db.models import Prefetch, OuterRef, Sum, Count, ExpressionWrapper, FloatField, IntegerField, F
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.generics import ListAPIView

from place.models import Place, FeedBackPlace, Tag, TagPlace
from route.models import Route, FeedBackRoute
from route.serializers import RouteListSerializers


@extend_schema_view(
    get=extend_schema(
        tags=['Маршруты.'],
        methods=['GET'],
        description='Получение всех маршрутов.',
        responses={
            200: OpenApiResponse(
                response=RouteListSerializers,
            ),
        }
    )
)
class RouteListView(ListAPIView):
    serializer_class = RouteListSerializers

    def get_queryset(self):
        queryset = Route.objects.prefetch_related('images').prefetch_related(
            Prefetch(
                'route_feedbacks',
                queryset=FeedBackRoute.objects.only('stars', 'route_id'),
                to_attr='feedback'
            )
        )
        return queryset
