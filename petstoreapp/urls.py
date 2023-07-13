from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='index'),
    path('nosotros/', nosotros, name='nosotros'),
    path('formulario/', formulario, name='formulario'),
    path('api/', api, name='api'),
    path('lista_productos', lista_productos, name='lista_productos'),
    path('crear/', crear_producto, name='crear_producto'),
    path('modificar/<id>', modificar_producto, name='modificar_producto'),
    path('eliminar<id>', eliminar_producto, name='eliminar_producto'),
    path('registro/', registro_usuario, name='registro'),
    path('tienda/', tienda, name='tienda'),
    path('generarBoleta/', generarBoleta,name="generarBoleta"),
    path('agregar/<id>', agregar_producto, name="agregar"),
    path('eliminar/<id>', eliminar_producto, name="eliminar"),
    path('restar/<id>', restar_producto, name="restar"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
    path('seguimiento/', ver_seguimiento, name="seguimiento"),
    path('lista_ordenes/', lista_ordenes, name="lista_ordenes"),
    path('cambiar_estado/<int:orden_id>', cambiar_estado, name='cambiar_estado'),
    path('guardar_estado/<int:orden_id>', guardar_estado, name='guardar_estado'),
    path('historial', historial_compras, name='historial')
]