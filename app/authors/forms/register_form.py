from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Jonh')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Your Password')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_.'
            'The lenght should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters'
        },
        min_length=4, max_length=150,

    )
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.'
    )

    first_name = forms.CharField(
        required=True,
        error_messages={'required': 'Write your first name'},
        label='First Name'
    )

    last_name = forms.CharField(
        required=True,
        error_messages={'required': 'Write your first name'},
        label='Last Name'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
        }),
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number. The length should be'
            ' least 8 characteres.'
        ),
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        }),
        error_messages={
            'required': 'Password must not be empty',
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude={}

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
                'class': 'input text_input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email)

        if exists:
            raise ValidationError(
                'User email is already in use', code='invalid')

        return email

    def clean_password(self):
        data = self.cleaned_data.get('password')
        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(pipoca)s no campo password',
                code='invalid',
                params={'pipoca': '"atenção"'}
            )
        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
