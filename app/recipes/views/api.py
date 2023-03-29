from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.recipes.permissions import IsOwner
from app.tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


def page_size(size):
    class RecipeAPIv2Pagination(PageNumberPagination):
        page_size = size

    return RecipeAPIv2Pagination


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = page_size(10)
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'options', 'head', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        seralizer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request, },
            partial=True
        )
        seralizer.is_valid(raise_exception=True)
        seralizer.save()
        return Response(
            seralizer.data,
        )


'''
class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = page_size(10)
'''

'''
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]
        serializers = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializers.data)

    def post(self, request):
        serializers = RecipeSerializer(
            context={'request': request}, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(
            author_id=1, category_id=1, tags=[1, 2])
        return Response(
            serializers.data,
            status=status.HTTP_201_CREATED)
    '''

'''
class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = page_size(10)
'''

'''
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            pk=pk
        )
        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializers = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializers.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializers = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    '''

'''
@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializers = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializers.data)
    elif request.method == 'POST':
        serializers = RecipeSerializer(
            context={'request': request}, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(
            author_id=1, category_id=1, tags=[1, 2])
        return Response(
            serializers.data,
            status=status.HTTP_201_CREATED)
'''

'''
@api_view(['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    if request.method == 'GET':
        serializers = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializers.data)
    elif request.method == 'PATCH':
        serializers = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializers = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializers.data)
    # return Response({
    #     'detail': 'Eita',
    # }, status=status.HTTP_404_NOT_FOUND)
'''


@api_view()
def recipe_api_tag(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializers = TagSerializer(instance=tag, many=False)
    return Response(serializers.data)
