from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.authors'

    def ready(self, *args, **kwargs):
        import app.authors.signals  # noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
