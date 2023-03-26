from django.contrib.auth import get_user_model
from rest_framework import viewsets

from api.serializers import (IngredientsSerializer, RecipeSerializer,
                             TagsSerializer, FavoriteSerializer,
                             ShopingCartSerializer, SubscribeSerializer)

User = get_user_model()


class IngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer


class TagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer


class ShopingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShopingCartSerializer
