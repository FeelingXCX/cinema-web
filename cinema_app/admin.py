from django.contrib import admin
from .models import Pelicula, PerfilUsuario

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'director', 'año', 'duracion', 'precio', 'activa', 'creada_por', 'fecha_creacion']
    list_filter = ['activa', 'año', 'creada_por']
    search_fields = ['titulo', 'director', 'sinopsis']
    list_per_page = 20
    date_hierarchy = 'fecha_creacion'
    
    # Campos que se muestran en el formulario de edición
    fields = ['titulo', 'director', 'año', 'duracion', 'sinopsis', 'precio', 'activa']
    
    def save_model(self, request, obj, form, change):
        """Asignar automáticamente el usuario que crea la película"""
        if not change:  # Solo cuando se crea (no cuando se edita)
            obj.creada_por = request.user
        super().save_model(request, obj, form, change)

    from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefono', 'fecha_nacimiento']
    search_fields = ['usuario__username', 'usuario__email', 'telefono']
    list_filter = ['fecha_nacimiento']