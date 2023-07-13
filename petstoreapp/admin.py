from django.contrib import admin
from .models import Producto, Categoria, Boleta, detalle_boleta, SeguimientoOrden

# Register your models here.

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Boleta)
admin.site.register(detalle_boleta)
admin.site.register(SeguimientoOrden)
