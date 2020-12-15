from django.apps import AppConfig


class ModulebookConfig(AppConfig):
    name = 'modulebook'

    def ready(self):
        import modulebook.signals