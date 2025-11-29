from django.shortcuts import render
from .models import Producto
# Create your views here.

def tienda_view(request):
    productos = Producto.objects.all()
    return render(request, 'myapp/tienda.html', {'productos': productos})