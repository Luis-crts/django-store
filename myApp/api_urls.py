from django.urls import path
from rest_framework.routers import DefaultRouter

# APIs que ya tenías
from .api import OrdenViewSet, ProductoViewSet
from .api_reports import ReporteSistemaAPI

# APIs nuevas para el examen
from .views_api import (
    InsumoViewSet,
    PedidoRestrictedViewSet,
    filtrar_pedidos
)

router = DefaultRouter()

# APIs antiguas tuyas
router.register(r'ordenes', OrdenViewSet, basename='ordenes')
router.register(r'productos', ProductoViewSet, basename='productos')

# APIs nuevas (examen)
router.register(r'insumos', InsumoViewSet, basename='insumos')
router.register(r'pedidos', PedidoRestrictedViewSet, basename='pedidos')


urlpatterns = [
    # API Reporte que ya tenías
    path('reporte/', ReporteSistemaAPI.as_view(), name='reporte_sistema'),

    # API 3 – filtrado de pedidos
    path('pedidos/filtrar/', filtrar_pedidos, name='filtrar_pedidos'),
]

urlpatterns += router.urls
