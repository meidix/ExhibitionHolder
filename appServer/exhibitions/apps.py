from django.apps import AppConfig


class ExhibitionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exhibitions'

    def ready(self):
        from . import signals