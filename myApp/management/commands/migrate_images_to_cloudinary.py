from django.core.management.base import BaseCommand
from myApp.models import ProductoImagen, OrdenImagen, Insumo
from django.core.files import File
import os


class Command(BaseCommand):
    help = "Migra imágenes locales a Cloudinary"

    def handle(self, *args, **options):
        self.stdout.write("Migrando imágenes de productos...")
        self.migrar_producto_imagenes()

        self.stdout.write("Migrando imágenes de órdenes...")
        self.migrar_orden_imagenes()

        self.stdout.write("Migrando imágenes de insumos...")
        self.migrar_insumos()

        self.stdout.write(self.style.SUCCESS("Migración completada"))


    def migrar_producto_imagenes(self):
        for img in ProductoImagen.objects.all():
            if img.imagen and os.path.isfile(img.imagen.path):
                with open(img.imagen.path, 'rb') as f:
                    img.imagen.save(
                        os.path.basename(img.imagen.name),
                        File(f),
                        save=True
                    )


    def migrar_orden_imagenes(self):
        for img in OrdenImagen.objects.all():
            if img.imagen and os.path.isfile(img.imagen.path):
                with open(img.imagen.path, 'rb') as f:
                    img.imagen.save(
                        os.path.basename(img.imagen.name),
                        File(f),
                        save=True
                    )


    def migrar_insumos(self):
        for insumo in Insumo.objects.exclude(imagen=''):
            if insumo.imagen and os.path.isfile(insumo.imagen.path):
                with open(insumo.imagen.path, 'rb') as f:
                    insumo.imagen.save(
                        os.path.basename(insumo.imagen.name),
                        File(f),
                        save=True
                    )
