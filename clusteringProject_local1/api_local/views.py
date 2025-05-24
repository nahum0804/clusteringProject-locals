from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import requests
import socket
import json
from django.core.serializers.json import DjangoJSONEncoder
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

class SincronizarDatosView(APIView):
    def get(self, request):
        BASE_CENTRAL = "http://172.24.104.248:8000/api"

        endpoints = {
            "clientes": (Cliente, ClienteSerializer, "id_cliente"),
            "historial_envios": (HistorialEnvio, HistorialEnvioSerializer, "id_envio"),
            "historial_pagos": (HistorialPago, HistorialPagoSerializer, "id_pago"),
            "nodos": (Nodo, NodoSerializer, "ip_nodo"),
        }

        resultados = {}
        errores = []

        # --- Paso 1: Obtener datos desde la central y sincronizar localmente ---
        for endpoint, (Model, Serializer, pk_field) in endpoints.items():
            url = f"{BASE_CENTRAL}/{endpoint}/"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                for item in data:
                    try:
                        if endpoint == "historial_envios":
                            item["cliente"] = Cliente.objects.get(id_cliente=item["cliente"])
                            if item.get("ip_nodo"):
                                item["ip_nodo"] = Nodo.objects.get(ip_nodo=item["ip_nodo"])

                        elif endpoint == "historial_pagos":
                            item["cliente"] = Cliente.objects.get(id_cliente=item["cliente"])

                        obj, _ = Model.objects.update_or_create(
                            defaults=item, **{pk_field: item[pk_field]}
                        )
                    except Exception as e:
                        errores.append(f"{endpoint}: {e}")

                resultados[endpoint] = f"Sincronizados {len(data)} registros"
            except Exception as e:
                resultados[endpoint] = f"Error: {str(e)}"

        # --- Paso 2: Enviar datos locales hacia la central ---
        ip_local = socket.gethostbyname(socket.gethostname())

        for endpoint, (Model, Serializer, pk_field) in endpoints.items():
            try:
                objetos = Model.objects.all()
                serializer = Serializer(objetos, many=True)

                # Convertir datos a JSON válido (manejo de UUID, Decimal, etc.)
                payload = json.loads(json.dumps(serializer.data, cls=DjangoJSONEncoder))

                url_post = f"{BASE_CENTRAL}/{endpoint}/bulk_sync/"
                response = requests.post(url_post, json=payload)
                response.raise_for_status()
                resultados[f"{endpoint}_enviados"] = f"Enviados {len(payload)} registros desde nodo {ip_local}"
            except Exception as e:
                resultados[f"{endpoint}_enviados"] = f"Error al enviar: {e}"

        if errores:
            resultados["errores"] = errores

        return Response(resultados, status=status.HTTP_200_OK)
