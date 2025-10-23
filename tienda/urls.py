from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/', views.detalle_videojuego, name='detalle_videojuego'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:pk>/', views.agregar_carrito, name='agregar_carrito'),
    path('contacto/', views.contacto, name='contacto'),
]
