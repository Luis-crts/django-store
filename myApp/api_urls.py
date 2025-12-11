from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import OrdenViewSet, ProductoViewSet

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='ordenes')
router.register(r'productos', ProductoViewSet, basename='productos')

urlpatterns = router.urls
