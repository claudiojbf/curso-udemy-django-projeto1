from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from app.authors.validatora import AuthorRecipeValidator
from app.recipes.models import Recipe
from utils.django_forms import add_attrs


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attrs(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time',\
            'preparation_time_unite', 'servings', 'servings_unite',\
            'preparation_steps', 'category', 'cover'
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
            ),
            'category': forms.Select(
                attrs={
                    'class': 'span-2',
                }
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
