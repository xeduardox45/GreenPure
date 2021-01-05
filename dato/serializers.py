from rest_framework import serializers
from .models import Datos


class DatosSerializer(serializers.ModelSerializer):
    Lugar = serializers.CharField(source='Ubicacion.nombre_ciudad')
    class Meta:        
        model = Datos
        fields = ('Ubicacion', 'Lugar', 'Humedad', 'Temperatura', 'Calor', 'Concentracion', 'SensorHumo', 'SensorMetano', 'fecha')
    """
    def create(self, validated_data):
        
        Create and return a new `Serie` instance, given the validated data.
        
        return Serie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        Update and return an existing `Serie` instance, given the validated data.
        
        instance.Ubicacion = validated_data.get('Ubicacion', instance.Ubicacion)
        instance.Temperatura = validated_data.get('Temperatura', instance.Temperatura)
        instance.Calor = validated_data.get('Calor', instance.Calor)
        instance.Concentracion = validated_data.get('Concentracion', instance.Concentracion)
        instance.SensorHumo = validated_data.get('SensorHumo', instance.SensorHumo)
        instance.SensorMetano = validated_data.get('SensorMetano', instance.SensorMetano)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.save()
        return instance
    """