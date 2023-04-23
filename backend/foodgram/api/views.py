from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             TagSerializer, SubscribeSerializer,
                             RecipeWriteSerializer, RecipeSubscribeSerializer,
                             FollowOrShoppingCartSerializer, )
from recipe.models import (Recipe, Subscribe, Tag, Ingredient, Favorite,
                           ShoppingCart, IngredientRecipe)

User = get_user_model()


class UsersViewSet(UserViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubscribeViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'delete']
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        author = get_object_or_404(User, pk=self.kwargs.get('id'))
        serializer.save(user=user, author=author)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        author = get_object_or_404(User, pk=self.kwargs.get('id'))
        follow = get_object_or_404(Subscribe, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = FollowOrShoppingCartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user).exists()


class TagsViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = [AllowAny]
    serializer_class = TagSerializer
    pagination_class = None
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.GenericViewSet,
                         ListModelMixin, RetrieveModelMixin):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, ]
    # filterset_class = ...
    search_fields = (r'^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeReadSerializer
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend, ]
    # filterset_class = utils.RecipeFilter

    def get_serializer_class(self):

        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer

        return RecipeWriteSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(user=request.user,
                                           recipes=recipe.id).exists()

        if self.request.method == 'POST':
            if favorite:
                return Response({'errors': 'Рецепт уже есть в избранном'},
                                status=status.HTTP_400_BAD_REQUEST,)
            Favorite.objects.get_or_create(user=request.user, recipes=recipe)
            data = FollowOrShoppingCartSerializer(recipe).data
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            if favorite:
                follow = get_object_or_404(Favorite,
                                           user=request.user,
                                           recipes=recipe)
                follow.delete()
                return Response('Рецепт успешно удален из избранного',
                                status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Такого рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = ShoppingCart.objects.filter(user=request.user,
                                                    recipes=recipe.id).exists()

        if self.request.method == 'POST':
            if shopping_cart:
                return Response({'errors': 'Рецепт уже есть в списке покупок'},
                                status=status.HTTP_400_BAD_REQUEST,)
            ShoppingCart.objects.get_or_create(user=request.user,
                                               recipes=recipe)
            data = FollowOrShoppingCartSerializer(recipe).data
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            if shopping_cart:
                shopping_cart = get_object_or_404(ShoppingCart,
                                                  user=request.user,
                                                  recipes=recipe)
                shopping_cart.delete()
                return Response('Рецепт успешно удален из списка покупок',
                                status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Такого рецепта нет в списке покупок'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('GET', ),
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        if not request.user.shoppingcart.exists():
            return Response('В списке покупок нет рецептов',
                            status=status.HTTP_400_BAD_REQUEST)
        ingredients = (
            IngredientRecipe.objects
            .filter(recipe__shoppingcart__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit')
        )

        text = ''
        for ingredient in ingredients:
            text += '{} - {} {}. \n'.format(*ingredient)
        file = HttpResponse(f'Покупки:\n {text}', content_type='text/plain')
        file['Content-Disposition'] = (
            'attachment; filename=shopping_cart.txt'
        )
        return file
