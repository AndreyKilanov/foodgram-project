from django.contrib import admin

from reviews.models import (Ingredients, Recipe, Tags, Favorite,
                            Subscribe, ShopingCart)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'get_ingredients',
                    'text', 'tags', 'cooking_time',)
    list_filter = ('name', 'author', 'tags',)
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    list_editable = ('name', 'color', 'slug',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_editable = ('user',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_editable = ('user',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(ShopingCart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe',)
    list_max_show_all = 15
    empty_value_display = '-пусто-'
