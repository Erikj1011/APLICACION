// Pequeño script para manejo de imágenes y mejoras UI
document.addEventListener('DOMContentLoaded', function(){
  // placeholder ya definido en template; aquí podemos añadir efectos ligeros
  const imgs = document.querySelectorAll('.card-media img');
  imgs.forEach(img => {
    img.addEventListener('error', () => {
      img.src = img.dataset.placeholder || '/static/tienda/img/placeholder.svg';
    });
  });
});
