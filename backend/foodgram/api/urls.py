from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientsViewSet, RecipeViewSet, TagsViewSet,
                       FavoriteViewSet, ShopingCartViewSet, SubscribeViewSet)

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('favorites', FavoriteViewSet, basename='favorites')
router_v1.register('shopingcarts', ShopingCartViewSet, basename='shopingcarts')
router_v1.register('subscribes', SubscribeViewSet, basename='subscribes')

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('auth/token/', get_jwt_token, name='token'),
    # path('auth/signup/', signup),
]
