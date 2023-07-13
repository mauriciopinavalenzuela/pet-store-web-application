from django.contrib import messages

class Carrito():

    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto):
        encontrado = False
        for key, value in self.carrito.items():
            if value["producto_id"] == producto.codigo:
                value["cantidad"] = int(value["cantidad"]) + 1
                value["total"] = value["cantidad"] * producto.precio
                encontrado = True
                break
        if not encontrado:
            self.carrito[producto.codigo] = {
                "producto_id": producto.codigo,
                "nombre": producto.nombre,
                "marca": producto.marca,
                "stock": producto.stock,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "cantidad": 1,
                "total": producto.precio,
            }
        self.guardar_carrito()
        messages.success(self.request, "Producto agregado al carrito.")

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        for key, value in self.carrito.items():
            if value["producto_id"] == producto.codigo:
                del self.carrito[key]
                self.guardar_carrito()
                break
        messages.success(self.request, "Producto eliminado del carrito.")

    def restar(self, producto):
        for key, value in self.carrito.items():
            if value["producto_id"] == producto.codigo:
                value["cantidad"] = max(int(value["cantidad"]) - 1, 0)
                value["total"] = value["cantidad"] * producto.precio
                if value["cantidad"] == 0:
                    self.eliminar(producto)
                break
        self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
        messages.success(self.request, "Carrito limpiado.")



