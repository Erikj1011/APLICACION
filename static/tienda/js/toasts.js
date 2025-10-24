// Muestra los mensajes Django (renderizados en HTML) como toasts animados.
// El script espera que el backend despliegue mensajes como elementos <div data-gws-message="level">text</div>

document.addEventListener('DOMContentLoaded', function(){
  const container = document.getElementById('gws-toasts');
  if(!container) return;

  // Buscar elementos generados por Django (si los hay)
  const serverMsgs = document.querySelectorAll('[data-gws-message]');
  serverMsgs.forEach(node => {
    const level = node.getAttribute('data-gws-message') || 'info';
    const text = node.textContent.trim();
    if(!text) return;
    showToast(text, level);
    // eliminar nodo original para evitar doble visualización
    node.remove();
  });

  function showToast(text, level='info', timeout=4500){
    const el = document.createElement('div');
    el.className = `gws-toast ${level}`;
    el.innerHTML = `<span class="msg">${text}</span><span class="close">&times;</span>`;
    container.appendChild(el);
    // force reflow para animar
    void el.offsetWidth;
    el.classList.add('show');

    const closer = el.querySelector('.close');
    closer.addEventListener('click', () => hide(el));

    const t = setTimeout(() => hide(el), timeout);

    function hide(node){
      node.classList.remove('show');
      setTimeout(() => node.remove(), 260);
      clearTimeout(t);
    }
  }

});
