from django.apps import AppConfig

class CinemaAppConfig(AppConfig):  # Cambiar nombre si era XdxdConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cinema_app'  
    verbose_name = 'Sistema de Cine'