from django.db import models

# Create your models here.
'''
class Ubicacion(models.Model):
     codigo = models.CharField(max_length=200)
     nombre_ciudad = models.CharField(max_length=200)
'''

class Datos(models.Model):
    #Ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    Humedad = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Temperatura = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Calor = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Concentracion = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Latitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    Longitud = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    SensorHumo = models.BooleanField(default=False)
    SensorMetano = models.BooleanField(default=False)
    fecha = models.DateTimeField('Fecha y hora')