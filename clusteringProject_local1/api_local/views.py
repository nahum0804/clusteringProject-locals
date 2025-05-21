from rest_framework import viewsets
from .models import (
    Cliente,
    HistorialEnvio,
    HistorialPago,
    Vehiculo,
    ControlEnvio,
    Ruta,
    DetalleRuta
)
from .serializers import (
    ClienteSerializer,
    HistorialEnvioSerializer,
    HistorialPagoSerializer,
    VehiculoSerializer,
    ControlEnvioSerializer,
    RutaSerializer,
    DetalleRutaSerializer
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class HistorialEnvioViewSet(viewsets.ModelViewSet):
    queryset = HistorialEnvio.objects.all()
    serializer_class = HistorialEnvioSerializer

class HistorialPagoViewSet(viewsets.ModelViewSet):
    queryset = HistorialPago.objects.all()
    serializer_class = HistorialPagoSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ControlEnvioViewSet(viewsets.ModelViewSet):
    queryset = ControlEnvio.objects.all()
    serializer_class = ControlEnvioSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class DetalleRutaViewSet(viewsets.ModelViewSet):
    queryset = DetalleRuta.objects.all()
    serializer_class = DetalleRutaSerializer