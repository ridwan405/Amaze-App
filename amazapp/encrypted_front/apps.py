from django.apps import AppConfig


class EncryptedFrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'encrypted_front'

    def ready(self) -> None:
        import encrypted_front.signals.handlers