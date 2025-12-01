from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Producto, Categoria
from django.db.models import Q


def home(request):
    productos = Producto.objects.filter(activo=True).order_by('-id')  # Ordena por ID descendente
    categorias = Categoria.objects.all()
    
    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    categoria_seleccionada = None
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
        categoria_seleccionada = get_object_or_404(Categoria, pk=categoria_id)
    
    # Buscador
    q = request.GET.get('q')
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q)
        )
    
    # se ven 9 productos por página 
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

def solicitar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'solicitar_producto.html', {'producto': producto})

def seguimiento_pedido(request, token):
    return render(request, 'seguimiento_pedido.html', {'token': token})