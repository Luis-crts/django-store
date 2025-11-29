from django.shortcuts import render
from .models import Producto
from .models import Categoria

def tienda_view(request):
    productos = Producto.objects.all()
    return render(request, 'tienda.html', {'productos': productos})

def home(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    return render(request, 'home.html', context)