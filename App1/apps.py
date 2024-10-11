from django.apps import AppConfig


class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App1'


from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'

    def ready(self):
        import App1.signals