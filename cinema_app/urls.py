from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    

    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    

    path('peliculas/', views.lista_peliculas, name='peliculas'),
    path('agregar-pelicula/', views.agregar_pelicula, name='agregar_pelicula'),
]