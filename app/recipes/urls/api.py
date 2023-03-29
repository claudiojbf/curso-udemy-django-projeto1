from django.urls import path

from app.recipes import views
from app.recipes.urls.site import urlpatterns

app_name = 'recipes'

# recipe_api_v2_router = routers.SimpleRouter()
# recipe_api_v2_router.register('recipe/api/v2', views.RecipeAPIv2ViewSet)


# urlpatterns.append(
#     path('recipes/api/v2/', views.RecipeAPIv2ViewSet.as_view({
#         'get': 'list',
#         'post': 'create'
#     }),
#         name='recipe_api_v2'))
# urlpatterns.append(
#     path('recipes/api/v2/<int:pk>/', views.RecipeAPIv2ViewSet.as_view({
#         'get': 'retrieve',
#         'patch': 'partial_update',
#         'delete': 'destroy'
#     }),
#         name='recipe_api_v2_detail')
# )
urlpatterns.append(
    path('recipes/api/v2/tag/<int:pk>/',
         views.recipe_api_tag, name='recipe_api_v2_tag')
)
