from django.contrib import admin
from django.utils.html import format_html
from .models import (Categoria,Producto,ProductoImagen,Orden,OrdenItem,OrdenImagen,Insumo)


# CATEGORÍAS
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


# PRODUCTOS
class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    max_num = 3


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('imagen_preview', 'nombre', 'precio', 'stock', 'activo', 'categoria')
    list_display_links = ('nombre',)
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre',)
    inlines = [ProductoImagenInline]

    def imagen_preview(self, obj):
        imagen = obj.imagenes.first()
        if imagen and imagen.imagen:
            return format_html(
                '<img src="{}" style="max-width:150px; max-height:150px;" />',
                imagen.imagen.url
            )
        return 'Sin imagen'

    imagen_preview.short_description = 'Vista previa'



# INSUMOS
@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = (
        'imagen_preview', 'nombre', 'categoria', 'tipo',
        'cantidad', 'unidad', 'marca', 'color'
    )
    list_filter = ('categoria', 'marca')
    search_fields = ('nombre',)
    list_editable = ('cantidad',)

    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'categoria', 'tipo', 'marca', 'color', 'imagen')
        }),
        ('Inventario', {
            'fields': ('cantidad', 'unidad')
        }),
    )

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-width:300px; max-height:300px;" />',
                obj.imagen.url
            )
        return 'Sin imagen'

    imagen_preview.short_description = 'Vista previa'



# ORDENES

class OrdenItemInline(admin.TabularInline):
    model = OrdenItem
    extra = 0
    fields = ('producto', 'cantidad', 'precio_unitario')


class OrdenImagenInline(admin.TabularInline):
    model = OrdenImagen
    extra = 0
    readonly_fields = ('imagen_tag',)

    def imagen_tag(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height:100px;" />',
                obj.imagen.url
            )
        return ''

    imagen_tag.short_description = 'Imagen'


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'cliente_nombre',
        'estado',
        'estado_pago',
        'producto_referencia',
        'creado'
    )
    list_filter = ('estado', 'estado_pago', 'creado')
    list_editable = ('estado', 'estado_pago')
    search_fields = ('token', 'cliente_nombre', 'contacto')
    ordering = ('-creado',)
    readonly_fields = ('token', 'creado', 'actualizado')
    inlines = (OrdenItemInline, OrdenImagenInline)

    fieldsets = (
        ('Información del pedido', {
            'fields': ('token', 'cliente_nombre', 'contacto', 'creado', 'actualizado')
        }),
        ('Producto y detalles', {
            'fields': (
                'producto_referencia',
                'descripcion',
                'fecha_necesaria',
                'plataforma'
            )
        }),
        ('Estado', {
            'fields': ('estado', 'estado_pago'),
            'classes': ('wide',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Regla de negocio:
        Si el pedido está PAGADO, automáticamente queda COMPLETADO
        """
        if obj.estado_pago == 'pagado':
            obj.estado = 'completado'

        super().save_model(request, obj, form, change)


@admin.register(OrdenImagen)
class OrdenImagenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'imagen')


@admin.register(OrdenItem)
class OrdenItemAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad', 'precio_unitario')
    list_editable = ('cantidad',)
    search_fields = ('orden__token', 'producto__nombre')

