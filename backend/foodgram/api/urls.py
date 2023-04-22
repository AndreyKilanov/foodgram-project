from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientsViewSet, RecipeViewSet, TagsViewSet,
                       FavoriteViewSet, SubscribeViewSet, UsersViewSet)

router_v1 = DefaultRouter()


router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')

router_v1.register(
    'users/subscriptions', FavoriteViewSet, basename='subscriptions'
)
router_v1.register(
    r'users/(?P<id>\d+)/subscribe', SubscribeViewSet, basename='subscribe'
)
router_v1.register('users', UsersViewSet, basename='users')


urlpatterns = [re_path(r'^auth/', include('djoser.urls.authtoken')), ]
urlpatterns += router_v1.urls
