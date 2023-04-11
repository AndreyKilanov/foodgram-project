from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from djoser.views import UserViewSet
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from api.permissions import IsAdminPermission
from api.serializers import (IngredientsSerializer, RecipeReadSerializer,
                             TagSerializer, FavoriteSerializer,
                             ShopingCartSerializer, SubscribeSerializer,
                             RecipeWriteSerializer, CustomUserSerializer,
                             CustomUserCreateSerializer)
from recipe.models import Recipe


User = get_user_model()


class IngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer


class TagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeReadSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer


class ShopingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShopingCartSerializer


class UsersViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    # @action(methods=['patch', 'get', ], detail=False,
    #         permission_classes=[permissions.IsAuthenticated])
    # def me(self, request):
    #     if request.method == 'get':
    #         serializer = self.get_serializer(self.request.user, )
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     serializer = self.get_serializer(
    #         self.request.user,
    #         data=request.data,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def update(self, request, *args, **kwargs):
    #     if request.method == 'PUT':
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().update(request, *args, **kwargs)
