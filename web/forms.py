from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Cliente, Profesor

class CustomUserCreationForm(UserCreationForm):
    dni = forms.CharField(max_length=20)
    direccion = forms.CharField(max_length=255)
    genero = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'direccion', 'genero', 'password1', 'password2')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = []

class ProfesorForm(forms.ModelForm):
    puesto = forms.CharField(max_length=100)

    class Meta:
        model = Profesor
        fields = ['puesto']