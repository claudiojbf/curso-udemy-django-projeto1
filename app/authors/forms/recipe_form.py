from collections import defaultdict

from django import forms

from app.recipes.models import Recipe
from utils.django_forms import add_attrs
from utils.string import is_positive_number


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
        cleaned_data = super_clean
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise forms.ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Title must have at list 5 chars.')

        return title

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Must be a positive number')

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self._my_errors['servings'].append('Must be a positive number')

        return servings
