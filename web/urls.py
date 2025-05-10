from django.urls import path
from . import views

urlpatterns = [
    path('registro/cliente/', views.registrar_cliente, name='registro_cliente'),
    path('registro/profesor/', views.registrar_profesor, name='registro_profesor'),
    path('', views.home, name='home'),
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
]