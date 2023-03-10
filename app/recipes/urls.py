from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListSearch.as_view(), name='search'),
    path('recipes/tags/<slug:slug>',
         views.RecipeListTag.as_view(), name='tag'),
    path('recipes/category/<int:category_id>/',
         views.RecipeListCategory.as_view(), name='category'),
    # flake8:noqa
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),

    path('recipes/api/v1/', views.RecipeListHomeApi.as_view(), name='recipes_api'),
    path('recipes/api/<int:pk>/', views.RecipeDetailApi.as_view(), name='recipe_api'),

    path('theory', views.theory, name='theory'),
]
