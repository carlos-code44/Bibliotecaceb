from django.db import models

# Create your models here.

from django.db import models

class Libro(models.Model):
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=50)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    fecha = models.CharField(max_length=200)
    numero_pags = models.CharField(max_length=200)
    numero_topografia = models.CharField(max_length=200)
    numero_ejemplar = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=1000)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo



from django.db import models
from django.contrib.auth.models import User

class Prestamo(models.Model):
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    estudiante_nombre = models.CharField(max_length=100)
    curso = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    comentarios = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.estudiante_nombre} - {self.libro.titulo}"



# modelo para roles de usuario

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username