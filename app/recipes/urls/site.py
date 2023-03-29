from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from app.recipes import views

app_name = 'recipes'

recipe_api_v2_router = routers.SimpleRouter()
recipe_api_v2_router.register('recipes/api/v2', views.RecipeAPIv2ViewSet)

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

    path(
        'recipes/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'recipes/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'recipes/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'),
]

urlpatterns += recipe_api_v2_router.urls
