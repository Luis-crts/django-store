from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import OrdenViewSet, ProductoViewSet
from .api_reports import ReporteSistemaAPI

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='ordenes')
router.register(r'productos', ProductoViewSet, basename='productos')

# Combina las rutas del router con la nueva ruta 'reporte/'
urlpatterns = [
    path('reporte/', ReporteSistemaAPI.as_view(), name='reporte_sistema'),
]

urlpatterns += router.urls

