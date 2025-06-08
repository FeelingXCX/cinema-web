from django.db import models
from django.contrib.auth.models import User

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    director = models.CharField(max_length=100, verbose_name="Director")
    año = models.IntegerField(verbose_name="Año")
    duracion = models.IntegerField(help_text="Duración en minutos", verbose_name="Duración")
    sinopsis = models.TextField(verbose_name="Sinopsis")
    precio = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Precio")
    activa = models.BooleanField(default=True, verbose_name="Película Activa")
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creada por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    def __str__(self):
        return f"{self.titulo} ({self.año})"
    
    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-fecha_creacion']
        
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    preferencias_genero = models.CharField(max_length=100, blank=True, verbose_name="Géneros Favoritos")
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)