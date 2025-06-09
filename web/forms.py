from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Cliente, Profesor, Membresia

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

# Formulario membresia
class MembresiaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.select_related('user').all(),
        label="Cliente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Membresia
        fields = ['cliente', 'fecha_inscripcion', 'duracion_meses', 'tipo_membresia', 'monto']
        widgets = {
            'fecha_inscripcion': forms.DateInput(attrs={'type': 'date'}),
        }