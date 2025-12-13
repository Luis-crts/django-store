from django.urls import path
from rest_framework.routers import DefaultRouter
from .views_api import InsumoViewSet, PedidoRestrictedViewSet, filtrar_pedidos

router = DefaultRouter()
router.register(r'insumos', InsumoViewSet, basename='insumos')
router.register(r'pedidos', PedidoRestrictedViewSet, basename='pedidos')

urlpatterns = [
    path(
        'pedidos/filtrar/<str:inicio>/<str:fin>/<str:estado>/<int:limite>/',
        filtrar_pedidos,
        name='filtrar_pedidos'
    ),
]

urlpatterns += router.urls
