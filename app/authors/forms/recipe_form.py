from django import forms

from app.recipes.models import Recipe
from utils.django_forms import add_attrs


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attrs(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time',\
            'preparation_time_unite', 'servings', 'servings_unite',\
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unite': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unite': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas')
                )
            )
        }
