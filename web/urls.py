from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [

    path('registro/cliente/', views.registrar_cliente, name='registro_cliente'),
    path('registro/profesor/', views.registrar_profesor, name='registro_profesor'),
    path('cliente/editar/', views.editar_perfil_cliente, name='editar_perfil_cliente'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    
    path('login/', views.login, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home, name='home'),
    path('redirect/', views.home_redirect, name='home_redirect'),
    path('superusuario/', views.panel_superusuario, name='home_superusuario'),
    path('profesor/', views.panel_profesor, name='home_profesor'),
    path('cliente/', views.panel_cliente, name='home_cliente'),      
    
]