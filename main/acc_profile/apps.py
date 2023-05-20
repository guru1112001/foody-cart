from django.apps import AppConfig


class AccProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acc_profile'

    def ready(self):
        import acc_profile.signals
