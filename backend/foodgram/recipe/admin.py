from django.contrib import admin

from recipe.models import (Ingredient, Recipe, Tag, Favorite,
                           Subscribe, ShopingCart)


class IngredientsField(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'text', 'tags', 'cooking_time',
                    'get_ingredient')
    list_filter = ('name', 'author', 'tags',)
    list_editable = ('text', 'tags')
    inlines = [IngredientsField, ]
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    list_editable = ('name', 'color', 'slug',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes',)
    list_editable = ('user',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes',)
    list_editable = ('user',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(ShopingCart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('recipes',)
    list_max_show_all = 15
    empty_value_display = '-пусто-'
