from django.http import Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from .models import Producto, Boleta, SeguimientoOrden, detalle_boleta
from .forms import ProductoForm, RegistroForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from petstoreapp.compra import Carrito
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.files.storage import default_storage

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def nosotros(request):
    return render(request, 'sobre nosotros.html')

def tienda(request):
    productos = Producto.objects.all()
    carrito = Carrito(request)

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 4)
        productos = paginator.page(page)
    except:
        raise Http404

    if request.method == 'POST' and 'agregar' in request.POST:
        producto_codigo = request.POST.get('codigo')
        try:
            producto = Producto.objects.get(codigo=producto_codigo)
        except Producto.DoesNotExist:
            mensaje_error = "El producto seleccionado no existe."
            return render(request, 'error.html', {'mensaje': mensaje_error})

        if producto.stock > 0:
            carrito.agregar(producto)
            producto.reducir_stock(1)  # Reducir el stock del producto en 1
        else:
            mensaje_error = f"El producto {producto.nombre} está agotado."
            return render(request, 'error.html', {'mensaje': mensaje_error})
        
    # Calcular el total de los productos en el carrito
    precio_total = sum([int(value['precio']) * int(value['cantidad']) for value in request.session['carrito'].values()])

    # Calcular el total con envío sumando el valor del envío
    total_con_envio = precio_total + 2000


    data = {
        'entity': productos,
        'valor_envio': 2000,
        'total_con_envio': total_con_envio,
        'paginator': paginator

    }
    return render(request, 'tienda.html', data)




def formulario(request):
    return render(request, 'formulario.html')

def api(request):
    return render(request, 'api.html')

@login_required
def lista_productos(request):
    producto = Producto.objects.all().order_by('codigo')

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(producto, 5)
        producto = paginator.page(page)
    except:
        raise Http404

    context = {
        'entity' : producto,
        'paginator': paginator
    }
    return render(request, 'lista-productos.html', context)

@login_required
def crear_producto(request):
    context = {
        'form': ProductoForm
    }
    if request.method=='POST':
        productos_form = ProductoForm(data=request.POST, files=request.FILES)
        if productos_form.is_valid():
            productos_form.save()
            return redirect(to="lista_productos")
        else:
            context['form'] = productos_form
    
    return render(request, 'crear-producto.html', context)

@login_required
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, codigo=id)
    datos = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            eliminar_imagen = formulario.cleaned_data.get('eliminar_imagen', False)
            if eliminar_imagen:
                # Eliminar la imagen existente
                producto.imagen.delete()

            formulario.save()
            return redirect(to="lista_productos")
        datos["form"] = formulario

    return render(request, 'modificar-producto.html', datos)

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, codigo=id)
    producto.delete()
    return redirect(to="lista_productos") 

#Autenticación
def registro_usuario(request):
    data = {
        'form' : RegistroForm()        
    }
    if request.method=="POST":
        formulario = RegistroForm(data = request.POST)  
        if formulario.is_valid():
            formulario.save()
            user= authenticate(username=formulario.cleaned_data["username"],
                  password=formulario.cleaned_data["password1"])
            login(request,user)   
            return redirect('index')
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

#Métodos del carrito de compras
def agregar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.agregar(producto=producto)
    return redirect('tienda')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('tienda')

def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(codigo=id)
    carrito_compra.restar(producto=producto)
    return redirect('tienda')
    
def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')

def generarBoleta(request):
    precio_total = 0
    for key, value in request.session['carrito'].items():
        precio_total += int(value['precio']) * int(value['cantidad'])

    # Verificar el stock antes de generar la boleta
    for key, value in request.session['carrito'].items():
        producto = Producto.objects.get(codigo=value['producto_id'])
        if value['cantidad'] > producto.stock:
            mensaje_error = f"No hay suficiente stock para el producto {producto.nombre}."
            return render(request, 'error.html', {'mensaje': mensaje_error})

    # Calcular el impuesto
    impuestos = int(precio_total * 0.19)

    # Calcular el valor del envío (fijo)
    valor_envio = 2000

    # Calcular el total con impuestos y envío
    total_con_impuestos_envio = precio_total + impuestos + valor_envio

    usuario = request.user

    if not usuario.is_authenticated:
        return redirect("/accounts/login")
    
    # Restar el stock y generar la boleta
    boleta = Boleta(total=precio_total, impuesto=impuestos, usuario=usuario)
    boleta.save()

    productos = []
    for key, value in request.session['carrito'].items():
        producto = Producto.objects.get(codigo=value['producto_id'])
        cantidad = value['cantidad']
        subtotal = cantidad * int(value['precio'])

        # Reducir el stock del producto
        producto.reducir_stock(cantidad)

        detalle = detalle_boleta(id_boleta=boleta, id_producto=producto, cantidad=cantidad, subtotal=subtotal)
        detalle.save()
        productos.append(detalle)

    datos = {
        'total_sin_impuestos': precio_total,
        'impuestos': impuestos,
        'total_con_impuestos': total_con_impuestos_envio,
        'productos': productos,
        'fecha': boleta.fechaCompra,
        'valor_envio': valor_envio,
    }

    seguimiento = SeguimientoOrden(boleta=boleta, estado=False)
    seguimiento.save()

    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()

    return render(request, 'detallecarrito.html', datos)

def lista_ordenes(request):
    ordenes = SeguimientoOrden.objects.select_related('boleta__usuario').all()
    return render(request, 'lista-ordenes.html', {'ordenes': ordenes})

def cambiar_estado(request, orden_id):
    if request.method == 'POST':
        estado = request.POST.get('estado')
        orden = SeguimientoOrden.objects.get(boleta_id=orden_id)  # Cambio aquí
        orden.estado = estado
        orden.save()
        return redirect('lista_ordenes')
    else:
        return render(request, 'cambiar-estado.html', {'orden_id': orden_id})

    

def guardar_estado(request, orden_id):
    try:
        orden = SeguimientoOrden.objects.get(boleta_id=orden_id)
    except SeguimientoOrden.DoesNotExist:
        return HttpResponseNotFound("La orden de seguimiento no existe.")

    if request.method == 'POST':
        estado = request.POST.get('estado')
        orden.estado = estado
        orden.save()
    
    return redirect('lista_ordenes')


    




@login_required
def ver_seguimiento(request):
    usuario = request.user
    boleta = Boleta.objects.filter(usuario=usuario).first()

    if boleta:
        seguimientos = SeguimientoOrden.objects.filter(boleta=boleta)

        productos = []
        for seguimiento in seguimientos:
            detalles = detalle_boleta.objects.filter(id_boleta=boleta)
            for detalle in detalles:
                producto = detalle.id_producto
                productos.append(producto)

        return render(request, 'ver-seguimiento.html', {'seguimientos': seguimientos, 'productos': productos})
    else:
        # Si no existe una boleta asociada al usuario, muestra un mensaje o redirige a otra página según tu necesidad
        mensaje = "No se encontró ninguna boleta asociada al usuario."
        return render(request, 'ver-seguimiento.html', {'mensaje': mensaje})
    
@login_required
def historial_compras(request):
    usuario = request.user
    boletas = Boleta.objects.filter(usuario=usuario, seguimientoorden__estado=True)

    return render(request, 'historial.html', {'boletas': boletas})
