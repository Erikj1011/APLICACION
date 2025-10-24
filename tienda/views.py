from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Videojuego, Carrito, ItemCarrito, Resena
from .forms import ResenaForm


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
    resenas = Resena.objects.filter(videojuego=videojuego).order_by('-fecha')
    # incluir formulario vacío para poder mostrarlo inline en la plantilla
    form = ResenaForm()
    return render(request, 'tienda/detalle.html', {
        'videojuego': videojuego,
        'resenas': resenas,
        'form': form,
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
# VISTA: Agregar al carrito (acumulativo + feedback)
# ==========================
@login_required(login_url='/login/')
def agregar_carrito(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, videojuego=videojuego)
    # Validación de stock: no permitir cantidad mayor al stock disponible
    current_qty = item.cantidad if not creado else 0
    if videojuego.stock <= current_qty:
        messages.error(request, f"No hay suficiente stock de {videojuego.nombre}.")
        return redirect(request.META.get('HTTP_REFERER') or reverse('productos'))

    if not creado:
        item.cantidad += 1
    else:
        item.cantidad = 1
    item.save()
    messages.success(request, f"{videojuego.nombre} agregado al carrito ✅")
    # Volver a la página anterior (referer) para que el usuario siga navegando
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('productos'))


# ==========================
# VISTA: Crear reseña (login requerido)
# ==========================
@login_required(login_url='/login/')
def crear_resena(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.usuario = request.user
            resena.videojuego = videojuego
            resena.save()
            messages.success(request, 'Reseña publicada ✅')
            return redirect('detalle_videojuego', pk=pk)
    else:
        form = ResenaForm()
    return render(request, 'tienda/crear_resena.html', {'form': form, 'videojuego': videojuego})


@login_required
def disminuir_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
        messages.info(request, f'Cantidad reducida: {item.videojuego.nombre}')
    else:
        item.delete()
        messages.info(request, f'Item eliminado: {item.videojuego.nombre}')
    return redirect('carrito')


@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    nombre = item.videojuego.nombre
    item.delete()
    messages.success(request, f'Eliminado: {nombre}')
    return redirect('carrito')


@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.all().delete()
    messages.success(request, 'Carrito vaciado.')
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
