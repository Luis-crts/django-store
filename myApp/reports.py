from django.db.models import Count, Sum
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Orden, OrdenItem

def get_report_data(start_date=None, end_date=None):

    # convertir a datetime
    rango = {}
    if start_date:
        start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))

    if start_date and end_date:
        rango = {"creado__range": (start_date, end_date)}

    # 1. pedidos por estado
    pedidos_por_estado = (
        Orden.objects.filter(**rango)
        .values("estado")
        .annotate(total=Count("id"))
        .order_by()
    )

    # 2. pedidos por plataforma
    pedidos_por_plataforma = (
        Orden.objects.filter(**rango)
        .values("plataforma")
        .annotate(total=Count("id"))
        .order_by()
    )

    # 3. productos más vendidos
    productos_vendidos = (
        OrdenItem.objects.filter(orden__in=Orden.objects.filter(**rango))
        .values("producto__nombre")
        .annotate(total=Sum("cantidad"))
        .order_by("-total")
    )

    return {
        "pedidos_por_estado": list(pedidos_por_estado),
        "pedidos_por_plataforma": list(pedidos_por_plataforma),
        "productos_vendidos": list(productos_vendidos),
    }
