from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from recipe.validators import hex_validator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единица измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='ingredient_unique_name')
        ]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название тега')
    color = models.CharField(max_length=7, unique=True, verbose_name='Цвет',
                             validators=[hex_validator])
    slug = models.SlugField(max_length=200, unique=True,
                            verbose_name='Уникальный адрес')

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe',
                                         related_name='recipes',
                                         verbose_name='Ингредиенты')
    image = models.FileField(upload_to='recipe_images/',
                             verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[MinValueValidator(
            limit_value=1,
            message='Время приготовления не может быть меньше 1')]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def get_ingredient(self):
        return "\n".join([f_name.name for f_name in self.ingredients.all()])

    def get_tag(self):
        return "\n".join([tag_name.name for tag_name in self.tags.all()])

    def __str__(self) -> str:
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorite',
                             verbose_name='Избранный автор')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorite',
                               verbose_name='Избранный рецепт')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_and_recipes'
            )
        ]

    def __str__(self):
        return self.user_id


class Subscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='уникальные имена')]

    def __str__(self):
        return self.author_id


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shoppingcart',
                             verbose_name='Создатель списка покупок')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shoppingcart',
                               verbose_name='Список покупок')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_user_and_recipes'
            )
        ]

    def __str__(self):
        return self.recipe_id


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient_recipe',
                                   verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredient_recipe',
                               verbose_name='Рецепт')
    amount = models.IntegerField(
        verbose_name='Колличество',
        validators=[MinValueValidator(
            limit_value=1,
            message='Колличество не может быть меньше 1')]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Колличество ингредиента'
        verbose_name_plural = 'Колличество ингредиентов'

    def __str__(self):
        return self.recipe_id
