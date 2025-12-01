from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('producto/<int:pk>/solicitar/', views.solicitar_producto, name='solicitar_producto'),
    path('pedido/<str:token>/', views.seguimiento_pedido, name='seguimiento_pedido'),
    path('seguimientos/', views.listar_seguimientos, name='listar_seguimientos'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
