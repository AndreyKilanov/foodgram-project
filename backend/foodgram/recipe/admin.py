from django.contrib import admin

from recipe.models import (Ingredient, Recipe, Tag, Favorite,
                           ShoppingCart, Subscribe)


class IngredientsField(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class TagsFields(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'text', 'get_tag', 'cooking_time',
                    'get_ingredient')
    list_filter = ('name', 'author', )
    list_editable = ('text', )
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
    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('id', 'name', 'color', 'slug',)
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
    list_display = ('user', 'author',)
    list_editable = ('user',)
    list_display_links = None
    list_max_show_all = 15
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipes',)
    list_max_show_all = 15
    empty_value_display = '-пусто-'
