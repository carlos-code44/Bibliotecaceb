document.addEventListener('DOMContentLoaded', function() {
    const botonBajar = document.getElementById('boton-bajar');
    const header = document.getElementById('miHeader');
  
    botonBajar.addEventListener('click', function() {
      scrollSuave(header);
    });
  
    function scrollSuave(elemento) {
      const inicioY = window.pageYOffset;
      const elementoY = elemento.getBoundingClientRect().top + inicioY;
      const distancia = elementoY - inicioY;
      const duracion = 1000; // Duración en milisegundos (ajusta este valor para hacerlo más lento o más rápido)
      let inicio;
  
      window.requestAnimationFrame(function paso(tiempoActual) {
        if (!inicio) inicio = tiempoActual;
        const tiempoPasado = tiempoActual - inicio;
        const porcentaje = Math.min(tiempoPasado / duracion, 1);
  
        window.scrollTo(0, inicioY + distancia * easeInOutCubic(porcentaje));
  
        if (porcentaje < 1) {
          window.requestAnimationFrame(paso);
        }
      });
    }
  
    // Función de aceleración para un movimiento más natural
    function easeInOutCubic(t) {
      return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
    }
  });