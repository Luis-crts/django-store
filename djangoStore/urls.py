from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from myApp import views
from myApp.views_reports import vista_reporte, reporte_dashboard


urlpatterns = [
    path('admin/', admin.site.urls),

    # publicas
    path('', views.home, name='home'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('producto/<int:pk>/solicitar/', views.solicitar_producto, name='solicitar_producto'),
    path('seguimiento/', views.buscar_pedido, name='buscar_pedido'),
    path('pedido/<str:token>/', views.seguimiento_pedido, name='seguimiento_pedido'),

    # Admin
    path('seguimientos/', views.listar_seguimientos, name='listar_seguimientos'),
    path('reportes/', vista_reporte, name='vista_reporte'),
    path('dashboard/', reporte_dashboard, name='reporte_dashboard'),

    path('api/', include('myApp.api_urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
