import os
from pathlib import Path

from utils.environment import get_env_variable, parse_comma_sep_str_to_list

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: list[str] = parse_comma_sep_str_to_list(
    get_env_variable('ALLOWED_HOSTS'))

CSRF_TRUSTED_ORIGINS: list[str] = parse_comma_sep_str_to_list(
    get_env_variable('CSRF_TRUSTED_ORIGINS'))

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
