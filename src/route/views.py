from django.db.models import Prefetch, OuterRef, Sum, Count, ExpressionWrapper, FloatField, IntegerField, F
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from place.models import Place, FeedBackPlace, Tag, TagPlace
from route.models import Route, FeedBackRoute
from route.serializers import RouteListSerializers, RetrieveRouteSerializers, AddedFeedbackRouteSerializer


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


class FeedbackRouteView(GenericAPIView):
    queryset = Route.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = AddedFeedbackRouteSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        route = self.get_object()
        user = self.request.user

        exists_user_feedback = FeedBackRoute.objects.filter(user=user, route=route).exists()
        if exists_user_feedback:
            return JsonResponse(
                {'detail': 'Вы уже оставляли комментарий.'},
                status=status.HTTP_409_CONFLICT
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=user, route=route)
        return Response(status=status.HTTP_201_CREATED)
