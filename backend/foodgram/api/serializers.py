import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from recipe.models import (Ingredient, Recipe, Tag, Favorite, ShoppingCart,
                           Subscribe)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    ingredients = IngredientSerializer(many=True)
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
    ingredients = IngredientSerializer(many=True)
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
    resipes = RecipeReadSerializer

    class Meta:
        model = Favorite
        fields = ('user', 'recipes')


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('user', 'author')


class ShopingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous or user == obj:
            return False
        return Subscribe.objects.filter(user=user.username,
                                        author=obj.username).exist()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('id', )

    # def validate_email(self, email):
    #     regex = re.compile(r'^[\w.@+-]+$')
    #     if not re.fullmatch(regex, email):
    #         raise serializers.ValidationError('Проверьте email!')
    #     return email
    # def validate_username(self, username):
    #     if username.lower() == 'me':
    #         raise serializers.ValidationError(
    #             {'Выберите другой username.'})
    #     regex = re.compile(r'^[\w.@+-]+$')
    #     if not re.fullmatch(regex, username):
    #         raise serializers.ValidationError('Проверьте username!')
    #     return username


# class UserAccessTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)
#     # username = serializers.CharField(required=True)
#     # confirmation_code = serializers.CharField(required=True)
#
#     def validate(self, data):
#         # user = get_object_or_404(User, username=data['username'])
#         # if not default_token_generator.check_token(user,
#         #                                            data['confirmation_code']):
#         #     raise serializers.ValidationError(
#         #         {'confirmation_code': 'Неверный код подтверждения'})
#         email = get_object_or_404(User, email=data['email'])
#         print(f'12341556 ::: {email}')
#         password = get_object_or_404(User, password=data['password'])
#         print(f'12121313  ::: {str(password)}')
#         if not email or password:
#             raise serializers.ValidationError(
#                 {'email': 'не верный email или пароль'}
#             )
#         return data

    # def validate_token(self, username):
    #     user = get_object_or_404(User, username=username)
    #     token = AccessToken.for_user(user)
    #     if not default_token_generator.check_token(user, token):
    #         raise serializers.ValidationError({"token": "Не верный токен"})
    #
    # def validate_username(self, username):
    #     regex = re.compile(r'^[\w.@+-]+$')
    #     if not re.fullmatch(regex, username):
    #         raise serializers.ValidationError('Проверьте username!')
    #     return username

    # def validate_email(self, email):
    #     regex = re.compile(r'^[\w.@+-]+$')
    #     if not re.fullmatch(regex, email):
    #         raise serializers.ValidationError('Проверьте email!')
    #     return email
