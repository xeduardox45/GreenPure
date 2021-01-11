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

class CaracteristicasSerializer(serializers.Serializer):
    latitud = serializers.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitud = serializers.DecimalField(max_digits=10, decimal_places=7, default=0)
    calidad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    hora = serializers.TimeField()
    humedad = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperatura = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    calor = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    concentracion = serializers.DecimalField(max_digits=6, decimal_places=2, default=0)
    sensorHumo = serializers.BooleanField()
    sensorMetano = serializers.BooleanField()

class ElementosSerializer(serializers.Serializer):
    distrito = serializers.CharField(max_length=100)
    datos = serializers.ListField(
        child=CaracteristicasSerializer()
    )

class DatosResumenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fecha = serializers.DateField()
    pais = serializers.CharField(max_length=100)
    ciudad = serializers.CharField(max_length=100)
    calidadAVG = serializers.IntegerField()
    ubicaciones = serializers.ListField(
        child=ElementosSerializer()
    )