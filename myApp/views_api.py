from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date

from .models import Insumo, Orden
from .serializers import InsumoSerializer, OrdenSerializer


# ========= API 1 =========
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


# ========= API 2 =========
class PedidoRestrictedViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer


# ========= API 3 =========
@api_view(["GET"])
def filtrar_pedidos(request, inicio, fin, estado, limite):
    pedidos = Orden.objects.all()

    fecha_inicio = parse_date(f"{inicio[:4]}-{inicio[4:6]}-{inicio[6:]}")
    fecha_fin = parse_date(f"{fin[:4]}-{fin[4:6]}-{fin[6:]}")

    if fecha_inicio:
        pedidos = pedidos.filter(creado__date__gte=fecha_inicio)

    if fecha_fin:
        pedidos = pedidos.filter(creado__date__lte=fecha_fin)

    if estado.lower() != "todos":
        pedidos = pedidos.filter(estado=estado)

    pedidos = pedidos[:limite]

    serializer = OrdenSerializer(pedidos, many=True)
    return Response(serializer.data)

