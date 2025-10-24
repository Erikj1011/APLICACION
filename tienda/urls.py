from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/', views.detalle_videojuego, name='detalle_videojuego'),
    path('producto/<int:pk>/resena/', views.crear_resena, name='crear_resena'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:pk>/', views.agregar_carrito, name='agregar_carrito'),
    path('aumentar/<int:pk>/', views.aumentar_item, name='aumentar_item'),
    path('disminuir/<int:pk>/', views.disminuir_item, name='disminuir_item'),
    path('eliminar/<int:pk>/', views.eliminar_item, name='eliminar_item'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('pagar/', views.pagar, name='pagar'),
    path('contacto/', views.contacto, name='contacto'),
    path('register/', views.register_view, name='register'),
    path('comunidad/', views.comunidad, name='comunidad'),
    path('comunidad/crear/', views.crear_hilo, name='crear_hilo'),
    path('comunidad/<int:pk>/', views.ver_hilo, name='ver_hilo'),
]
