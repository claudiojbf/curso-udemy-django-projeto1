from rest_framework import serializers

from app.authors.validatora import AuthorRecipeValidator
from app.recipes.models import Recipe
from app.tag.models import Tag

# from .models import Category


class TagSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()
    class Meta:
        model = Tag
        fields = ['id', 'name',]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'public',
            'preparation',
            'category',
            'author',
            'tags',
            'tag_objects',
            'tag_links',
            'preparation_time',
            'preparation_time_unite',
            'servings',
            'servings_unite',
            'preparation_steps',
            'cover'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all()
    # )
    category = serializers.StringRelatedField(read_only=True,)
    # author = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all()
    # )
    # tags = serializers.PrimaryKeyRelatedField(
    #     queryset=Tag.objects.all(), many=True)
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # queryset=Tag.objects.all(),
        view_name='recipes:recipe_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unite}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(attrs, ErrorClass=serializers.ValidationError)
        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)
