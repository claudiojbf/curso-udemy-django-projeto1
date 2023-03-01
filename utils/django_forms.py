import re

from django.core.exceptions import ValidationError


def add_attrs(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_vals):
    add_attrs(field, 'placeholder', placeholder_vals)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            (
                'Password must have at least one uppercase letter,'
                'one lowercase letter and one number. The length should be'
                ' least 8 characteres.'
            ),
            code='Invalid'
        )
