from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipe.models import (Ingredient, Recipe, Tag, Favorite,
                           Subscribe, ShopingCart)

User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe


class ShopingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopingCart
