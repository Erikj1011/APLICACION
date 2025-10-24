from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/', views.detalle_videojuego, name='detalle_videojuego'),
    path('producto/<int:pk>/resena/', views.crear_resena, name='crear_resena'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:pk>/', views.agregar_carrito, name='agregar_carrito'),
    path('disminuir/<int:item_id>/', views.disminuir_item, name='disminuir_item'),
    path('eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('contacto/', views.contacto, name='contacto'),
]
