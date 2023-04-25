import io

from reportlab.pdfgen import canvas

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin,
                                   CreateModelMixin, DestroyModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.response import Response

from api.filters import RecipeFilter, IngredientFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, SubscribeSerializer,
                             TagSerializer, FollowOrShoppingCartSerializer, )
from recipe.models import (Recipe, Subscribe, Tag, Ingredient, Favorite,
                           ShoppingCart, IngredientRecipe)

User = get_user_model()


class UsersViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubscribeViewSet(viewsets.GenericViewSet, CreateModelMixin,
                       DestroyModelMixin):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

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


class SubscriptionsViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Subscribe.objects.filter(user=self.request.user)


class TagsViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.GenericViewSet,
                         ListModelMixin, RetrieveModelMixin):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    search_fields = (r'^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeReadSerializer
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer

        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(user=request.user,
                                           recipe=recipe.id).exists()

        if self.request.method == 'POST':
            if favorite:
                return Response({'errors': 'Рецепт уже есть в избранном'},
                                status=status.HTTP_400_BAD_REQUEST,)
            Favorite.objects.get_or_create(user=request.user, recipe=recipe)
            data = FollowOrShoppingCartSerializer(recipe).data
            return Response(data, status=status.HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if favorite:
                follow = get_object_or_404(Favorite,
                                           user=request.user,
                                           recipe=recipe)
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Такого рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('POST', 'DELETE'),
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = ShoppingCart.objects.filter(user=request.user,
                                                    recipe=recipe.id).exists()

        if self.request.method == 'POST':
            if shopping_cart:
                return Response({'errors': 'Рецепт уже есть в списке покупок'},
                                status=status.HTTP_400_BAD_REQUEST,)
            ShoppingCart.objects.get_or_create(user=request.user,
                                               recipe=recipe)
            data = FollowOrShoppingCartSerializer(recipe).data
            return Response(data, status=status.HTTP_201_CREATED)

        elif self.request.method == 'DELETE':
            if shopping_cart:
                shopping_cart = get_object_or_404(ShoppingCart,
                                                  user=request.user,
                                                  recipe=recipe)
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
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
            text += '* {} - {} {}. \n'.format(*ingredient)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(x=100, y=100, text=f'Список покупок: \n {text}')
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False,
                            filename='shopping_cart.pdf')
