from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

def generate_token():
    return uuid.uuid4().hex

class Categoria(models.Model):
    TIPO_CHOICES = (
        ('producto', 'Producto'),
        ('insumo', 'Insumo'),
    )
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='producto')

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
def producto_imagen_path(instance, filename):
    categoria = slugify(instance.producto.categoria.nombre) 
    return f"productos/{categoria}/{filename}"
    
class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to= producto_imagen_path)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
class Orden(models.Model):
    ESTADO_CHOICES = (
        ('solicitado', 'Solicitado'),
        ('en_proceso', 'En proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    PAGO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    )

    token = models.CharField(max_length=48, unique=True, editable=False, default=generate_token)
    cliente_nombre = models.CharField(max_length=200, default='', blank=True)
    contacto = models.CharField(max_length=200, help_text="Email / teléfono / red social", default='', blank=True)
    producto_referencia = models.ForeignKey('Producto', null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.TextField(blank=True)
    plataforma = models.CharField(max_length=100, default='pagina web')
    fecha_necesaria = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='solicitado')
    estado_pago = models.CharField(max_length=20, choices=PAGO_CHOICES, default='pendiente')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden {self.token} - {self.cliente_nombre}"

class OrdenImagen(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='ordenes/%Y/%m/%d/')

    def __str__(self):
        return f"Imagen orden {self.orden.token}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad}x {self.producto} ({self.orden.token})"
    
class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=20, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.cantidad}{self.unidad or ''}"