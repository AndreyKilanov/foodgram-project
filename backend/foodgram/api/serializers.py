import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipe.models import (Ingredient, Recipe, Tag, Favorite, ShoppingCart,
                           Subscribe, IngredientRecipe)

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user

        if user.is_authenticated:
            user = user.id
            author = obj.id
            return Subscribe.objects.filter(user=user, author=author).exists()

        return False


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientsReadRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsReadRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('id', 'tags', 'author', 'ingredients',
                            'is_favorited', 'is_in_shopping_cart', 'name',
                            'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user

        if user.is_authenticated:
            return obj.favorite.filter(user=user).exists()

        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user

        if user.is_authenticated:
            return obj.shoppingcart.filter(user=user).exists()

        return False


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientsInRecipeSerializer(source='ingredient_recipe',
                                                many=True)
    cooking_time = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
        read_only_fields = ('id', 'author', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_recipe')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        recipe_create = [IngredientRecipe(
            recipe=recipe,
            amount=ingredient['amount'],
            ingredient=ingredient['ingredient']
            ) for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(recipe_create)

        return recipe


class RecipeSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='following.id')
    email = serializers.CharField(source='following.email')
    username = serializers.CharField(source='following.username')
    first_name = serializers.CharField(source='following.first_name')
    last_name = serializers.CharField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='following.recipes.count'
    )
    recipes = RecipeSubscribeSerializer(
        source='following.recipes.count'
    )

    class Meta:
        model = Subscribe
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'password', 'recipes',
                            'recipes_count')

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        author_id = self.context['id']

        if user_id == author_id:
            raise serializers.ValidationError('На себя подписаться нельзя.')

        if Subscribe.objects.filter(user=user_id, author=author_id).exists():
            raise serializers.ValidationError('Уже подписаны на пользователя')

        return attrs

    def get_is_subscribed(self, obj):
        following_id = self.context['request'].user.id
        return Subscribe.objects.filter(following_id=following_id,
                                        user_id=obj.following_id).exists()

