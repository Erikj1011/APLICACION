// Pequeño script para manejo de imágenes y autohide de mensajes
function imageFallback(img){
  try {
    img.onerror = null;
    img.src = '/static/tienda/img/placeholder.svg';
  } catch(e) {
    console.error('Fallback failed', e);
  }
}

// Mensajes autohide
document.addEventListener('DOMContentLoaded', function(){
  const msgs = document.querySelectorAll('.messages .msg');
  if(msgs.length){
    setTimeout(()=> {
      msgs.forEach(m => m.style.display = 'none');
    }, 4500);
  }

  // Image error fallback for imgs that may not have been caught
  const imgs = document.querySelectorAll('img');
  imgs.forEach(img => {
    img.addEventListener('error', () => imageFallback(img));
  });
    
  // Confirmaciones para links con class 'confirm'
  const confirmLinks = document.querySelectorAll('a.confirm');
  const modal = document.getElementById('gws-confirm-modal');
  const modalMsg = document.getElementById('gws-confirm-message');
  const modalOk = document.getElementById('gws-confirm-ok');
  const modalCancel = document.getElementById('gws-confirm-cancel');

  confirmLinks.forEach(link => {
    link.addEventListener('click', function(ev){
      ev.preventDefault();
      const href = this.getAttribute('href');
      const message = this.getAttribute('data-message') || '¿Confirmar acción?';
      showConfirm(message, () => { window.location.href = href; });
    });
  });

  function showConfirm(message, onConfirm){
    if(!modal) { if(onConfirm) onConfirm(); return; }
    modal.style.display = 'block';
    modal.setAttribute('aria-hidden','false');
    modalMsg.textContent = message;

    function clean(){
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden','true');
      modalOk.removeEventListener('click', okHandler);
      modalCancel.removeEventListener('click', cancelHandler);
    }
    function okHandler(){ clean(); if(onConfirm) onConfirm(); }
    function cancelHandler(){ clean(); }

    modalOk.addEventListener('click', okHandler);
    modalCancel.addEventListener('click', cancelHandler);
  }
});
