from rest_framework import serializers
from .models import Datos


class DatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datos
        fields = ('__all__')

    def create(self, validated_data):
        return Datos.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Humedad = validated_data.get('Humedad',instance.Humedad)
        instance.Temperatura = validated_data.get('Temperatura', instance.Temperatura)
        instance.Calor = validated_data.get('Calor', instance.Calor)
        instance.Concentracion = validated_data.get('Concentracion', instance.Concentracion)
        instance.Latitud = validated_data.get('Latitud', instance.Latitud)
        instance.Longitud = validated_data.get('Longitud', instance.Longitud)
        instance.SensorHumo = validated_data.get('SensorHumo', instance.SensorHumo)
        instance.SensorMetano = validated_data.get('SensorMetano', instance.SensorMetano)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.save()
        return instance