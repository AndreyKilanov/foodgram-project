from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from api.permissions import IsAdminPermission
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             TagSerializer, FavoriteSerializer,
                             ShopingCartSerializer, SubscribeSerializer,
                             RecipeWriteSerializer, CustomUserSerializer,
                             CustomUserCreateSerializer)
from recipe.models import Recipe, Subscribe, Tag, Ingredient, Favorite


User = get_user_model()


class UsersViewSet(UserViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()


class IngredientsViewSet(viewsets.GenericViewSet,
                         ListModelMixin, RetrieveModelMixin):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ...
    search_fields = (r'^name',)


class TagsViewSet(viewsets.GenericViewSet,
                  ListModelMixin, RetrieveModelMixin):
    permission_classes = [AllowAny]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class FavoriteViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeReadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ...
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def perform_update(self, serializer):
        author = self.request.user
        id = self.kwargs.get('pk')
        serializer.save(author=author, id=id)


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Subscribe.objects.all()


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShopingCartSerializer
