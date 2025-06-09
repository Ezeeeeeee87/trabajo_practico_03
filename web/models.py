from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    


class Membresia(models.Model):
    DURACION_CHOICES = [
        (1, '1 mes'),
        (3, '3 meses'),
        (6, '6 meses'),
    ]
    
    TIPO_CHOICES = [
        ('libre', 'Pase libre'),
        ('2xsemana', '2 veces por semana'),
        ('3xsemana', '3 veces por semana'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(default=timezone.now)
    duracion_meses = models.PositiveIntegerField(choices=DURACION_CHOICES)
    tipo_membresia = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=8, decimal_places=2)

    def fecha_vencimiento(self):
        return self.fecha_inscripcion + timezone.timedelta(days=30 * self.duracion_meses)

    def __str__(self):
        return f"{self.cliente} - {self.get_duracion_meses_display()} - {self.get_tipo_membresia_display()}"    