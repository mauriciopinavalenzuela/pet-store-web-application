from django.db import models
from distutils.command.upload import upload
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    codigo_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
   
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def reducir_stock(self, cantidad):
        self.stock -= cantidad
        self.save()

    def __str__(self):
        return self.nombre

class Boleta(models.Model):
    id_boleta=models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False, null=False, default= datetime.datetime.now)
    impuesto = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def calcular_total_con_impuesto(self):
        return self.total + (self.total * 0.19)

    def __str__(self):
        return str(self.id_boleta)
    
class detalle_boleta(models.Model):
    id_boleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)

class SeguimientoOrden(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
