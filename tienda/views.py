from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse
from .models import Videojuego, Carrito, ItemCarrito, Compra, DetalleCompra, Resena
from .forms import RegisterForm, ResenaForm
from django.db import transaction


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
    form = ResenaForm()
    return render(request, 'tienda/detalle.html', {
        'videojuego': videojuego,
        'resenas': resenas,
        'form': form,
    })


# ==========================
# VISTA: Carrito de compras
# ==========================
@login_required(login_url='/accounts/login/')
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = carrito.total_carrito()
    return render(request, 'tienda/carrito.html', {'carrito': carrito, 'items': items, 'total': total})


# ==========================
# VISTA: Agregar al carrito (acumulativo + feedback)
# ==========================
@login_required(login_url='/accounts/login/')
def agregar_carrito(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, videojuego=videojuego)
    if not creado:
        item.cantidad += 1
    # Validación básica de stock
    if videojuego.stock and item.cantidad > videojuego.stock:
        item.cantidad = videojuego.stock
        messages.warning(request, "Cantidad limitada por stock disponible.")
    item.save()
    messages.success(request, f"{videojuego.nombre} agregado al carrito.")
    return redirect(request.GET.get('next') or 'productos')


# ==========================
# VISTA: Crear reseña (login requerido)
# ==========================
@login_required(login_url='/accounts/login/')
def crear_resena(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.usuario = request.user
            res.videojuego = videojuego
            res.save()
            messages.success(request, "Reseña publicada.")
            return redirect('detalle_videojuego', pk=pk)
        else:
            messages.error(request, "Error en el formulario de reseña.")
    return redirect('detalle_videojuego', pk=pk)


@login_required(login_url='/accounts/login/')
def disminuir_item(request, pk):
    item = get_object_or_404(ItemCarrito, pk=pk, carrito__usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('ver_carrito')


@login_required(login_url='/accounts/login/')
def eliminar_item(request, pk):
    item = get_object_or_404(ItemCarrito, pk=pk, carrito__usuario=request.user)
    item.delete()
    messages.info(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')


@login_required(login_url='/accounts/login/')
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.all().delete()
    messages.info(request, "Carrito vaciado.")
    return redirect('ver_carrito')


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


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada. Bienvenido/a.")
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/accounts/login/')
@transaction.atomic
def pagar(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = carrito.items.select_related('videojuego').all()
    total = carrito.total_carrito()

    if request.method == 'POST':
        compra = Compra.objects.create(usuario=request.user, total=total, estado='pagado')
        for it in items:
            DetalleCompra.objects.create(
                compra=compra,
                videojuego=it.videojuego,
                cantidad=it.cantidad,
                subtotal=it.subtotal()
            )
            if it.videojuego.stock is not None:
                it.videojuego.stock = max(0, it.videojuego.stock - it.cantidad)
                it.videojuego.save()
        carrito.items.all().delete()
        messages.success(request, "Pago realizado con éxito. Gracias por tu compra.")
        return redirect('index')

    return render(request, 'tienda/pagar.html', {'items': items, 'total': total})


@login_required(login_url='/accounts/login/')
def aumentar_item(request, pk):
    item = get_object_or_404(ItemCarrito, pk=pk, carrito__usuario=request.user)
    if item.videojuego.stock and item.cantidad >= item.videojuego.stock:
        messages.warning(request, "No hay más stock disponible.")
    else:
        item.cantidad += 1
        item.save()
    return redirect('ver_carrito')


# =========================
# Foro / Comunidad
# =========================
from .models import Foro

def comunidad(request):
    hilos = Foro.objects.all().order_by('-fecha')
    return render(request, 'tienda/comunidad.html', {'hilos': hilos})


@login_required(login_url='/accounts/login/')
def crear_hilo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        if titulo and contenido:
            Foro.objects.create(titulo=titulo, autor=request.user, contenido=contenido)
            messages.success(request, 'Hilo creado en Comunidad.')
            return redirect('comunidad')
    return render(request, 'tienda/crear_hilo.html')


def ver_hilo(request, pk):
    hilo = get_object_or_404(Foro, pk=pk)
    # No hay modelo Comentario en esta versión; mostramos sólo el hilo
    return render(request, 'tienda/ver_hilo.html', {'hilo': hilo})
