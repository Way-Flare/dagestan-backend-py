from django.db.models import Prefetch
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from place.models import Place, FeedBackPlace
from place.serializers import ListPlacesSerializer, RetrievePlaceSerializer
from route.models import FeedBackRoute, Route


@extend_schema_view(
    get=extend_schema(
        tags=['Места (обьекты)'],
        methods=['GET'],
        description='Получение всех мест (объектов)',
        responses={
            200: OpenApiResponse(
                response=ListPlacesSerializer,
            ),
        }
    )
)
class PlaceListView(ListAPIView):
    serializer_class = ListPlacesSerializer

    def get_queryset(self):
        queryset = Place.objects.prefetch_related('tags', 'images').prefetch_related(
            Prefetch(
                'place_feedbacks',
                queryset=FeedBackPlace.objects.all(),
                to_attr='feedback'
            )
        )
        return queryset


@extend_schema_view(
    get=extend_schema(
        tags=['Места (обьекты)'],
        methods=['GET'],
        description='Получение детали одного места (объекта)',
        responses={
            200: OpenApiResponse(
                response=RetrievePlaceSerializer,
            ),
        }
    )
)
class PlaceRetrieveView(RetrieveAPIView):
    serializer_class = RetrievePlaceSerializer

    def get_queryset(self):
        lookup_url_kwarg = self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        instance = Place.objects.filter(**filter_kwargs).prefetch_related(
            'tags',
            'images',
            'contacts',
            'place_feedbacks__images',
            'place_feedbacks__user',
            'place_ways__images'
        ).prefetch_related(
            Prefetch(
                'place_feedbacks',
                queryset=FeedBackPlace.objects.all(),
                to_attr='feedback'
            )
        ).prefetch_related(
            Prefetch(
                'place_routes',
                queryset=Route.objects.prefetch_related('images').prefetch_related(
                    Prefetch(
                        'route_feedbacks',
                        queryset=FeedBackRoute.objects.all(),
                        to_attr='feedback'
                    )
                ),
                to_attr='routes'
            )
        )
        return instance


@extend_schema_view(
    post=extend_schema(
        tags=['Места (обьекты)'],
        methods=['POST'],
        description='Добавление в избранное места (объекта)',
        responses={
            201: OpenApiResponse(
                description='Добавлено в избранное.',
            ),
            204: OpenApiResponse(
                description='Удалено из избранного.',
            )
        }
    )
)
class SubscribeUnsubscribeToPlaceView(GenericAPIView):
    queryset = Place.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        place = self.get_object()
        user = self.request.user
        favorites_places_user = user.favorites_place.all()

        if place not in favorites_places_user:
            user.favorites_place.add(place)
            return Response(status=status.HTTP_201_CREATED)

        if place in favorites_places_user:
            user.favorites_place.remove(place)
            return Response(status=status.HTTP_204_NO_CONTENT)
