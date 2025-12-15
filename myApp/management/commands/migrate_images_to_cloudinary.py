from django.core.management.base import BaseCommand
from django.conf import settings
from myApp.models import ProductoImagen, OrdenImagen, Insumo
from django.core.files import File
import os

class Command(BaseCommand):
    help = "Migra imágenes locales desde MEDIA_ROOT a Cloudinary"

    def handle(self, *args, **options):
        self.stdout.write("📦 Migrando imágenes de productos...")
        self.migrar_producto_imagenes()

        self.stdout.write("📦 Migrando imágenes de órdenes...")
        self.migrar_orden_imagenes()

        self.stdout.write("📦 Migrando imágenes de insumos...")
        self.migrar_insumos()

        self.stdout.write(self.style.SUCCESS("✅ Migración completada"))


    def migrar_producto_imagenes(self):
        for img in ProductoImagen.objects.all():
            self._migrar_archivo(img, "productos")

    def migrar_orden_imagenes(self):
        for img in OrdenImagen.objects.all():
            self._migrar_archivo(img, "ordenes")

    def migrar_insumos(self):
        for insumo in Insumo.objects.exclude(imagen=""):
            self._migrar_archivo(insumo, "insumos")

    def _migrar_archivo(self, instancia, carpeta):
    # Si no hay imagen, saltar
        if not instancia.imagen:
            return

        nombre = instancia.imagen.name

    # Si ya es cloudinary, saltar
        if nombre.startswith("http") or "cloudinary" in nombre:
            return

        ruta_local = os.path.join(settings.BASE_DIR, "media", nombre)

        if not os.path.exists(ruta_local):
            self.stdout.write(f"⚠️ No existe: {ruta_local}")
            return

        with open(ruta_local, "rb") as f:
            instancia.imagen.save(
                os.path.basename(nombre),
                File(f),
                save=True
            )

        self.stdout.write(f"☁️ Subida: {nombre}")

