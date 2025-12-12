from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum
from django.utils.dateparse import parse_date
from myApp.models import Orden, OrdenItem

@staff_member_required
def vista_reporte(request):
    start = request.GET.get("start")
    end = request.GET.get("end")

    data = {
        "start": start,
        "end": end
    }

    return render(request, "reporte.html", data)


@login_required
def reporte_dashboard(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    ordenes = Orden.objects.all()

    # FILTROS DE FECHA
    if start_date:
        ordenes = ordenes.filter(creado__date__gte=parse_date(start_date))

    if end_date:
        ordenes = ordenes.filter(creado__date__lte=parse_date(end_date))

    # MÉTRICAS PRINCIPALES
    total_pedidos = ordenes.count()
    pedidos_pagados = ordenes.filter(estado_pago="pagado").count()
    pedidos_pendientes = ordenes.exclude(estado="completado").count()

    total_ingresos = (
        OrdenItem.objects.filter(orden__in=ordenes, orden__estado_pago="pagado")
        .aggregate(total=Sum("precio_unitario"))["total"]
        or 0
    )

    # GRÁFICOS
    pedidos_por_estado = (
        ordenes.values("estado")
        .annotate(total=Count("id"))
        .order_by("estado")
    )

    pedidos_por_plataforma = (
        ordenes.values("plataforma")
        .annotate(total=Count("id"))
        .order_by("plataforma")
    )

    productos_vendidos = (
        OrdenItem.objects.filter(orden__in=ordenes, orden__estado_pago="pagado")
        .values("producto__nombre")
        .annotate(total=Sum("cantidad"))
        .order_by("-total")
    )

    datos = {
        "total_pedidos": total_pedidos,
        "pedidos_pagados": pedidos_pagados,
        "pedidos_pendientes": pedidos_pendientes,
        "total_ingresos": float(total_ingresos),
        "pedidos_por_estado": list(pedidos_por_estado),
        "pedidos_por_plataforma": list(pedidos_por_plataforma),
        "productos_vendidos": list(productos_vendidos),
    }

    return render(request, "reportes/dashboard.html", {"datos": datos})


