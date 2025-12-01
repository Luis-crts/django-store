from django.contrib import admin
from django.utils.html import format_html
from .models import (Categoria, Producto, ProductoImagen, Orden, OrdenItem, OrdenImagen, Insumo)

# -------- CATEGORIA --------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# -------- PRODUCTO IMÁGENES INLINE --------
class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    max_num = 3


# -------- PRODUCTOS --------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'activo')
    ordering = ('categoria', 'nombre')
    inlines = [ProductoImagenInline]


# Apartado de ordenes
class OrdenImagenInline(admin.TabularInline):
    model = OrdenImagen
    extra = 0
    readonly_fields = ('imagen_tag',)

    def imagen_tag(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.imagen.url)
        return ''
    imagen_tag.short_description = 'Imagen'

class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('token', 'cliente_nombre', 'contacto', 'producto_referencia', 'get_estado_display', 'get_estado_pago_display', 'creado')
    list_filter = ('estado', 'estado_pago', 'creado')
    search_fields = ('token', 'cliente_nombre', 'contacto', 'descripcion')
    ordering = ('-creado',)
    readonly_fields = ('token', 'creado', 'actualizado')
    inlines = (OrdenItemInline, OrdenImagenInline)

@admin.register(OrdenImagen)
class OrdenImagenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'imagen')

@admin.register(OrdenItem)
class OrdenItemAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad', 'precio_unitario')


# -------- INSUMOS (inventario) --------
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'cantidad', 'unidad', 'marca', 'color')
    search_fields = ('nombre', 'tipo', 'marca', 'color')
    list_filter = ('tipo', 'marca', 'color')

