# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
from . import BASE_DIR

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
