from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    genero = models.CharField(max_length=10, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ])

    def __str__(self):
        return self.username
    
class Profesor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=100)

    def __str__(self):
        return f"Profesor: {self.user.first_name} {self.user.last_name}"
    
class Cliente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cliente: {self.user.first_name} {self.user.last_name}"