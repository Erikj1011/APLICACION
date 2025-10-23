from django.contrib import admin
from .models import Videojuego, Carrito, ItemCarrito, Compra, DetalleCompra, Resena, Foro

admin.site.register(Videojuego)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(Resena)
admin.site.register(Foro)
