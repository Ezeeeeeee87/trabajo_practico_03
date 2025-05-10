from . import views
from django.urls import path

urlpatterns = [

    path('registro/cliente/', views.registrar_cliente, name='registro_cliente'),
    path('registro/profesor/', views.registrar_profesor, name='registro_profesor'),
    
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    
    path('accounts/login/', views.login, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home_redirect, name='home'),
    path('superusuario/', views.panel_superusuario, name='home_superusuario'),
    path('profesor/', views.panel_profesor, name='home_profesor'),
    path('cliente/', views.panel_cliente, name='home_cliente'),        

]