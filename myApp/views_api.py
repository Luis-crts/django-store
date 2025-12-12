from rest_framework import viewsets
from .models import Insumo, Orden
from .serializers import InsumoSerializer, OrdenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from rest_framework import mixins, viewsets


# ========== API 1: CRUD COMPLETO INSUMOS ==========
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


class PedidoRestrictedViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer


@api_view(["GET"])
def filtrar_pedidos(request):
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    estado = request.GET.get("estado")
    limite = request.GET.get("limite")

    pedidos = Orden.objects.all()

    if fecha_inicio:
        pedidos = pedidos.filter(creado__date__gte=parse_date(fecha_inicio))

    if fecha_fin:
        pedidos = pedidos.filter(creado__date__lte=parse_date(fecha_fin))

    if estado:
        pedidos = pedidos.filter(estado=estado)

    if limite and limite.isdigit():
        pedidos = pedidos[:int(limite)]

    serializer = OrdenSerializer(pedidos, many=True)
    return Response(serializer.data)
