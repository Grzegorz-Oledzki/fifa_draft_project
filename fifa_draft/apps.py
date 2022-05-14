from django.apps import AppConfig


class FifaDraftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fifa_draft'

    def ready(self):
        import fifa_draft.signals
