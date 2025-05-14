from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Cliente, Profesor

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'password1', 'password2', 'dni', 'direccion', 'genero','email']

# Formulario para Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['direccion', 'genero', 'dni']

# Formulario para Profesor
class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['puesto']
