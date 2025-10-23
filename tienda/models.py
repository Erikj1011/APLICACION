from django.db import models
from django.contrib.auth.models import User

# ==========================
# MODELO: Videojuego
# ==========================
class Videojuego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='videojuegos/', null=True, blank=True)
    categoria = models.CharField(max_length=50)
    fecha_lanzamiento = models.DateField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


# ==========================
# MODELO: Carrito
# ==========================
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total_carrito(self):
        total = sum(item.subtotal() for item in self.items.all())
        return total


# ==========================
# MODELO: Item del Carrito
# ==========================
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.videojuego.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.videojuego.nombre}"


# ==========================
# MODELO: Compra
# ==========================
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ], default='pendiente')

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"


# ==========================
# MODELO: Detalle de Compra
# ==========================
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='detalles', on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.videojuego.nombre}"


# ==========================
# MODELO: Reseña
# ==========================
class Resena(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField(default=5)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario.username} sobre {self.videojuego.nombre}"


# ==========================
# MODELO: Foro
# ==========================
class Foro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
