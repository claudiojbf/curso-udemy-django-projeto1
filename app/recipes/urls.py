from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListHome.as_view(), name='home'),
    path('recipes/search/', views.RecipeListSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/',
         views.RecipeListCategory.as_view(), name='category'),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
]
