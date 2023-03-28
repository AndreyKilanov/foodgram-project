import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from recipe.models import (Ingredient, Recipe, Tag, Favorite,
                           Subscribe, ShopingCart)

User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = IngredientsSerializer(many=True)
    is_favorited = ...
    is_in_shopping_cart = ...

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('author', 'pub_date', 'is_favorited',
                            'is_in_shopping_cart')


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = IngredientsSerializer(many=True)
    is_favorited = ...
    is_in_shopping_cart = ...

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('author', 'pub_date', 'is_favorited',
                            'is_in_shopping_cart')


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='favorite',
        read_only=True,
    )
    resipes = ...
    
    class Meta:
        model = Favorite
        fields = ('user', 'recipes')


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe


class ShopingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopingCart


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'role')

    def validate_username(self, username):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, username):
            raise serializers.ValidationError('Проверьте username!')
        return username


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username.'})
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, username):
            raise serializers.ValidationError('Проверьте username!')
        return username


class UserAccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(get_user_model(), username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data

    def validate_token(self, username):
        user = get_object_or_404(User, username=username)
        token = AccessToken.for_user(user)
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid token"})

    def validate_username(self, username):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, username):
            raise serializers.ValidationError('Проверьте username!')
        return username