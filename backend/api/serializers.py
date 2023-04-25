from drf_extra_fields.fields import Base64ImageField

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers

from recipe.models import (Ingredient, Recipe, Tag, Subscribe,
                           IngredientRecipe)

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


class FollowOrShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


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
    ingredients = IngredientsReadRecipeSerializer(source='ingredient_recipe',
                                                  many=True)
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
    amount = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = serializers.IntegerField(min_value=1, max_value=1000)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = IngredientsInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')
        read_only_fields = ('id', 'author', 'tags', )

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Какой-то ингредиент был выбран более 1 раза'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        recipe_create = [IngredientRecipe(
            recipe=recipe,
            amount=ingredient['amount'],
            ingredient=ingredient['ingredient']
            ) for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(recipe_create)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')

        ingredients_in_data = IngredientRecipe.objects.filter(
            recipe__id=instance.id)
        ingredients_in_data.delete()

        recipe_update = [IngredientRecipe(
            recipe=instance,
            amount=ingredient['amount'],
            ingredient=ingredient['ingredient']
        ) for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(recipe_update)

        return instance


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='author.id', read_only=True)
    email = serializers.CharField(source='author.email', read_only=True)
    username = serializers.CharField(source='author.username',
                                     read_only=True)
    first_name = serializers.CharField(source='author.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='author.last_name',
                                      read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='author.recipe.count', read_only=True
    )

    class Meta:
        model = Subscribe
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def validate(self, attrs):
        user = self.context['request'].user.id
        author = int(self.context['view'].kwargs['id'])

        if user == author:
            username = self.context['request'].user.username
            raise serializers.ValidationError(
                {'errors': f'{username}. На себя подписаться нельзя.'}
            )

        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                {'errors': 'Вы уже подписаны на этого пользователя.'}
            )

        return attrs

    def get_recipes(self, obj):
        queryset = obj.author.recipes.all()
        return FollowOrShoppingCartSerializer(queryset, many=True).data

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(author_id=obj.author_id,
                                        user_id=obj.user_id).exists()
