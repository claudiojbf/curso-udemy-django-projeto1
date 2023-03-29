from collections import defaultdict

from django.core.exceptions import ValidationError

from utils.string import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        cd = self.data
        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to title')

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Title must have at list 5 chars.')

        return title

    def clean_preparation_time(self):
        preparation_time = self.data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self.errors['preparation_time'].append(
                'Must be a positive number')

        return preparation_time

    def clean_servings(self):
        servings = self.data.get('servings')

        if not is_positive_number(servings):
            self.errors['servings'].append('Must be a positive number')

        return servings
