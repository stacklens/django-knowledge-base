from django.apps import AppConfig


class MysignalConfig(AppConfig):
    name = 'mySignal'

    def ready(self):
        import mySignal.handlers