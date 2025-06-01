from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superuser', 'Superusuario'),
        ('profesor', 'Profesor'),
        ('cliente', 'Cliente'),
    ]
    dni = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255, default='Sin dirección')
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cliente')

    def is_profesor(self):
        return self.rol == 'profesor'

    def is_cliente(self):
        return self.rol == 'cliente'

    def is_superusuario(self):
        return self.rol == 'superuser'

class Profesor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=100)

    def __str__(self):
        return f"Profesor: {self.user.first_name} {self.user.last_name}"

class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, default='Sin dirección')
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    dni = models.CharField(max_length=20, default='00000000')
    

    def __str__(self):
        return f"Cliente: {self.user.first_name} {self.user.last_name}"