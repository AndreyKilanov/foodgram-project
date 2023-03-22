from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model


class Ingredients(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название тега')
    color = models.CharField(max_length=7, verbose_name='Цвет')
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name='Уникальный адрес')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор Рецепта'
    )
    ingredients = models.ManyToManyField(Ingredients,
                                         through='IngredientsRecipe')
    image = models.ImageField()
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(verbose_name='Время приготовления',
                                       validators=MinValueValidator(1))
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='favorite',
        verbose_name='Избранный автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        related_name='favorite',
        verbose_name='Избранный рецепт'
    )


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscribe',
        verbose_name='Подписки на автора'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscribe',
        verbose_name='Избранный рецепт'
    )


class ShopingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        related_name='subscribe',
        verbose_name='Список покупок'
    )


class IngredientsRecipe(models.Model):
    ingredients_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Сумма')
