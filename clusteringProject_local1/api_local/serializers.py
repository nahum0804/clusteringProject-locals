from rest_framework import serializers
from .models import (
    Cliente,
    HistorialEnvio,
    HistorialPago,
    Vehiculo,
    ControlEnvio,
    Ruta,
    DetalleRuta,
    Nodo,
)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class HistorialEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEnvio
        fields = '__all__'

class HistorialPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPago
        fields = '__all__'

class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ControlEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlEnvio
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class DetalleRutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleRuta
        fields = '__all__'