from django.db.models import Prefetch, OuterRef, Sum, Count, ExpressionWrapper, FloatField, IntegerField, F
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView

from place.models import Place, FeedBackPlace, Tag, TagPlace
from route.models import Route, FeedBackRoute
from route.serializers import RouteListSerializers, RetrieveRouteSerializers


@extend_schema_view(
    get=extend_schema(
        tags=['Маршруты'],
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


@extend_schema_view(
    get=extend_schema(
        tags=['Маршруты'],
        methods=['GET'],
        description='Получение детали одного маршрута.',
        responses={
            200: OpenApiResponse(
                response=RetrieveRouteSerializers,
            ),
        }
    )
)
class RouteRetrieveView(RetrieveAPIView):
    serializer_class = RetrieveRouteSerializers

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        queryset = Route.objects.filter(**filter_kwargs).prefetch_related(
            'images'
        ).prefetch_related(
            Prefetch(
                'places',
                queryset=Place.objects.prefetch_related('images', 'm2m_place_routes').prefetch_related(
                    Prefetch(
                        'tags',
                        queryset=Tag.objects.filter(tag_places__is_main=True).distinct(),
                        to_attr='main_tag'
                    )
                ).annotate(sequence=F('m2m_place_routes__sequence')),
                to_attr='place_annotated'
            ),
            Prefetch(
                'route_feedbacks',
                queryset=FeedBackRoute.objects.only('stars', 'route_id'),
                to_attr='feedback'
            )
        )
        return queryset
