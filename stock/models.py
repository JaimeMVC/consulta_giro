from django.db import models

class Material(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
