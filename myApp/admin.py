from django.contrib import admin
from .models import Categoria, Producto, Carrito, CarritoItem, Orden, OrdenItem


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'activo')
    ordering = ('categoria', 'nombre')


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'creado')
    search_fields = ('usuario__username',)
    ordering = ('creado',)


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'carrito', 'producto', 'cantidad')
    list_editable = ('cantidad',)
    search_fields = ('producto__nombre',)
    list_filter = ('producto',)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username',)
    list_editable = ('estado',)
    ordering = ('-fecha',)


@admin.register(OrdenItem)
class OrdenItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'producto', 'precio_unitario', 'cantidad')
    list_editable = ('precio_unitario', 'cantidad')
    list_filter = ('producto',)
    search_fields = ('producto__nombre',)


