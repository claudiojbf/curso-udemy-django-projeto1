from django.db.models.aggregates import Count
from django.shortcuts import render

from app.recipes.models import Recipe


def theory(request, *args, **kwagrs):
    recipes = Recipe.object.get_published()
    number_of_recipes = recipes.aggregate(number=Count('id'))
    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number'],
    }
    return render(
        request,
        'recipes/pages/theory.html',
        context=context,
    )
