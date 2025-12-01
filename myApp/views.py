from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Producto, Categoria, Orden, OrdenImagen, OrdenItem
from django.db.models import Q
import secrets

def home(request):
    q = request.GET.get('q', '')  
    productos = Producto.objects.filter(activo=True, categoria__tipo='producto').order_by('-id')
    categorias = Categoria.objects.filter(tipo='producto', productos__activo=True).distinct()

    categoria_id = request.GET.get('categoria')
    categoria_seleccionada = None
    if categoria_id:
        categoria_seleccionada = get_object_or_404(Categoria, pk=categoria_id, tipo='producto')
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
    relacionados = Producto.objects.filter(categoria=producto.categoria).exclude(pk=pk)[:4]
    ctx = {
        'producto': producto,
        'relacionados': relacionados,
    }
    return render(request, 'detalle_producto.html', ctx)

def solicitar_producto(request, pk=None):
    producto = None
    if pk:
        producto = get_object_or_404(Producto, pk=pk, activo=True)

    error = None
    initial = {
        'nombre': '',
        'email': '',
        'contact_method': 'WhatsApp',
        'contact_value': '',
        'descripcion': '',
        'fecha_necesaria': '',
    }

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        contact_method = request.POST.get('contact_method', '').strip()
        contact_value = request.POST.get('contact_value', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha_necesaria = request.POST.get('fecha_necesaria') or None

        initial.update({
            'nombre': nombre,
            'email': email,
            'contact_method': contact_method,
            'contact_value': contact_value,
            'descripcion': descripcion,
            'fecha_necesaria': fecha_necesaria or '',
        })

        if not email:
            error = "El correo electrónico es obligatorio."
        else:
            contacto_parts = [f"email: {email}"]
            if contact_value:
                contacto_parts.append(f"{contact_method}: {contact_value}")
            else:
                contacto_parts.append(f"{contact_method}: -")
            contacto_text = " | ".join(contacto_parts)

            token = secrets.token_urlsafe(12)
            orden = Orden.objects.create(
                token=token,
                cliente_nombre=nombre or 'Cliente',
                contacto=contacto_text,
                producto_referencia=producto,
                descripcion=descripcion,
                fecha_necesaria=fecha_necesaria or None,
                plataforma='pagina web',
                estado='solicitado',
                estado_pago='pendiente',
            )

            # guardar imágenes si es que las hay
            files = request.FILES.getlist('imagenes')
            for f in files:
                OrdenImagen.objects.create(orden=orden, imagen=f)

            if producto:
                if producto.stock <= 0:
                    error = "Lo sentimos, este producto ya no tiene stock disponible."
                else:
                    OrdenItem.objects.create(
                        orden=orden,
                        producto=producto,
                        cantidad=1,
                        precio_unitario=getattr(producto, 'precio', None)
                    )
                    producto.stock -= 1
                    producto.save()
                    return redirect('seguimiento_pedido', token=orden.token)

    context = {
        'producto': producto,
        'error': error,
        'initial': initial,
    }
    return render(request, 'solicitar_producto.html', context)


def seguimiento_pedido(request, token):
    orden = get_object_or_404(Orden, token=token)
    context = {
        'orden': orden,
    }
    return render(request, 'seguimiento_pedido.html', context)