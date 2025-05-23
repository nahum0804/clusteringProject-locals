from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from rest_framework import viewsets
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
from .serializers import (
    ClienteSerializer,
    HistorialEnvioSerializer,
    HistorialPagoSerializer,
    VehiculoSerializer,
    ControlEnvioSerializer,
    RutaSerializer,
    DetalleRutaSerializer,
    NodoSerializer,
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=['get'], url_path='por-nodo')
    def por_nodo(self, request):
        ip_nodo = request.query_params.get('ip')
        envios = HistorialEnvio.objects.filter(ip_nodo__ip_nodo=ip_nodo)
        clientes = Cliente.objects.filter(id_cliente__in=envios.values_list('cliente', flat=True).distinct())
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)

class HistorialEnvioViewSet(viewsets.ModelViewSet):
    queryset = HistorialEnvio.objects.all()
    serializer_class = HistorialEnvioSerializer

class HistorialPagoViewSet(viewsets.ModelViewSet):
    queryset = HistorialPago.objects.all()
    serializer_class = HistorialPagoSerializer

class NodoViewSet(viewsets.ModelViewSet):
    queryset = Nodo.objects.all()
    serializer_class = NodoSerializer

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

class SincronizarEstadoView(APIView):
    def post(self, request):
        data = request.data  # Lista de paquetes con su nuevo estado
        for item in data:
            try:
                paquete = ControlEnvio.objects.get(id_paquete=item["id_paquete"])
                paquete.estado = item["estado"]
                paquete.save()
            except ControlEnvio.DoesNotExist:
                continue
        return Response({"status": "actualizado"}, status=status.HTTP_200_OK)