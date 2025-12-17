from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Producto, Categoria, Orden, OrdenImagen, OrdenItem
from django.db.models import Count, Q, Sum
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required

import secrets


def home(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.filter(
        activo=True,
        categoria__tipo='producto'
    ).order_by('-id')

    categorias = Categoria.objects.filter(
        tipo='producto',
        productos__activo=True
    ).distinct()

    categoria_id = request.GET.get('categoria')
    categoria_seleccionada = None

    if categoria_id:
        categoria_seleccionada = get_object_or_404(
            Categoria,
            pk=categoria_id,
            tipo='producto'
        )
        productos = productos.filter(categoria_id=categoria_id)

    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )

    paginator = Paginator(productos, 9)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'q': q,
    }
    return render(request, 'home.html', context)


def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(pk=pk)[:4]

    return render(request, 'detalle_producto.html', {
        'producto': producto,
        'relacionados': relacionados,
    })


def solicitar_producto(request, pk=None):
    producto = None
    if pk:
        producto = get_object_or_404(Producto, pk=pk, activo=True)

    error = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        contacto_tipo = request.POST.get('contact_method', '').lower().strip()
        contacto_valor = request.POST.get('contact_value', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha_necesaria = request.POST.get('fecha_necesaria') or None

        if not email:
            error = "El correo electrónico es obligatorio."

        elif not contacto_tipo:
            error = "Debe seleccionar un medio de contacto."

        else:
            token = secrets.token_urlsafe(12)

            orden = Orden.objects.create(
                token=token,
                cliente_nombre=nombre or 'Cliente',
                contacto_tipo=contacto_tipo,
                contacto_valor=contacto_valor,
                producto_referencia=producto,
                descripcion=descripcion,
                fecha_necesaria=fecha_necesaria,
                plataforma='pagina web',
                estado='solicitado',
                estado_pago='pendiente',
            )

            # Guardar imágenes si existen
            for f in request.FILES.getlist('imagenes'):
                OrdenImagen.objects.create(
                    orden=orden,
                    imagen=f
                )

            if producto:
                if producto.stock <= 0:
                    error = "Lo sentimos, este producto no tiene stock."
                else:
                    OrdenItem.objects.create(
                        orden=orden,
                        producto=producto,
                        cantidad=1,
                        precio_unitario=producto.precio
                    )
                    producto.stock -= 1
                    producto.save()

                    return redirect(
                        'seguimiento_pedido',
                        token=orden.token
                    )

    return render(request, 'solicitar_producto.html', {
        'producto': producto,
        'error': error,
    })


def seguimiento_pedido(request, token):
    orden = get_object_or_404(Orden, token=token)
    return render(request, 'seguimiento_pedido.html', {'orden': orden})


@staff_member_required
def listar_seguimientos(request):
    ordenes = Orden.objects.all().order_by('-creado')

    estado = request.GET.get('estado')
    if estado:
        ordenes = ordenes.filter(estado=estado)

    paginator = Paginator(ordenes, 10)
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)

    context = {
        'ordenes': ordenes,
        'estados': Orden.ESTADO_CHOICES,
        'estado_filtro': estado,
    }
    return render(request, 'listar_seguimientos.html', context)



def reportes(request):
    producto_mas_pedido = (
        OrdenItem.objects
        .filter(orden__estado_pago='pagado')
        .values('producto')
        .annotate(cantidad_pedidos=Count('id'))
        .order_by('-cantidad_pedidos')
        .first()
    )

    producto_data = None
    if producto_mas_pedido:
        producto = Producto.objects.get(
            pk=producto_mas_pedido['producto']
        )
        producto_data = {
            'producto': producto,
            'cantidad_pedidos': producto_mas_pedido['cantidad_pedidos'],
        }

    total_pedidos = Orden.objects.count()
    pedidos_pagados = Orden.objects.filter(
        estado_pago='pagado'
    ).count()
    pedidos_pendientes = Orden.objects.filter(
        estado_pago='pendiente'
    ).count()

    total_ingresos = (
        OrdenItem.objects
        .filter(orden__estado_pago='pagado')
        .aggregate(total=Sum('precio_unitario'))['total']
        or 0
    )

    return render(request, 'reportes.html', {
        'producto_mas_pedido': producto_data,
        'total_pedidos': total_pedidos,
        'pedidos_pagados': pedidos_pagados,
        'pedidos_pendientes': pedidos_pendientes,
        'total_ingresos': total_ingresos,
    })
