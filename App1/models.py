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

    def __str__(self):
        return self.titulo

