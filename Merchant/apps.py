from django.apps import AppConfig

class MerchantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Merchant'

    def ready(self):
        import Merchant.signals
