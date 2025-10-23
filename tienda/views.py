from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Videojuego, Carrito, ItemCarrito, Resena

# ==========================
# VISTA: Página principal
# ==========================
def index(request):
    videojuegos = Videojuego.objects.all()[:8]
    return render(request, 'tienda/index.html', {'videojuegos': videojuegos})


# ==========================
# VISTA: Listado de videojuegos
# ==========================
def productos(request):
    videojuegos = Videojuego.objects.all()
    return render(request, 'tienda/productos.html', {'videojuegos': videojuegos})


# ==========================
# VISTA: Detalle de videojuego
# ==========================
def detalle_videojuego(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    resenas = Resena.objects.filter(videojuego=videojuego)
    return render(request, 'tienda/detalle.html', {
        'videojuego': videojuego,
        'resenas': resenas,
    })


# ==========================
# VISTA: Carrito de compras
# ==========================
@login_required
def carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = carrito.total_carrito()
    return render(request, 'tienda/carrito.html', {'carrito': carrito, 'items': items, 'total': total})


# ==========================
# VISTA: Agregar al carrito
# ==========================
@login_required
def agregar_carrito(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, videojuego=videojuego)
    if not creado:
        item.cantidad += 1
    item.save()
    return redirect('carrito')


# ==========================
# VISTA: Contacto simple
# ==========================
def contacto(request):
    mensaje = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        msg = request.POST.get('mensaje')
        mensaje = f"Gracias, {nombre or 'usuario'}! Hemos recibido tu mensaje."
    return render(request, 'tienda/contacto.html', {'mensaje': mensaje})
