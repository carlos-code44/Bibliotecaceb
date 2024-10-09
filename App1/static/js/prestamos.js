const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

menu.addEventListener("click",()=>{
    barraLateral.classList.toggle("max-barra-lateral");
    if(barraLateral.classList.contains("max-barra-lateral")){
        menu.children[0].style.display = "none";
        menu.children[1].style.display = "block";
    }
    else{
        menu.children[0].style.display = "block";
        menu.children[1].style.display = "none";
    }
    if(window.innerWidth<=320){
        barraLateral.classList.add("mini-barra-lateral");
        main.classList.add("min-main");
        spans.forEach((span)=>{
            span.classList.add("oculto");
        })
    }
});

palanca.addEventListener("click",()=>{
    let body = document.body;
    body.classList.toggle("dark-mode");
    body.classList.toggle("");
});

palanca.addEventListener("click", () => {
    let circulo = document.querySelector(".circulo");
    circulo.classList.toggle("prendido");
  });

cloud.addEventListener("click",()=>{
    barraLateral.classList.toggle("mini-barra-lateral");
    main.classList.toggle("min-main");
    spans.forEach((span)=>{
        span.classList.toggle("oculto");
    });
});

cloud.addEventListener("click", () => {
    const principal = document.querySelector(".contenedorprincipal");
    principal.classList.toggle("mini-barra");
  });



  // modal para opciones de perfil

const modal4 = document.querySelector('#modal4');

const openOptionsModal = (event) => {
    event.preventDefault();
    modal4.style.display = 'flex';
  }

const closeOptionsModal = () => {
    modal4.style.display = 'none';
}


// modal para editar perfil

const modal5 = document.querySelector('#modal5');

const openEditPerfilModal = (event) => {
    event.preventDefault(); 
    modal5.style.display = 'flex';
  }

const closeEditPerfilModal = () => {
    modal5.style.display = 'none';
}


// modal para editar perfil(usuario)

const modalCambioUsuario = document.querySelector('#modal-cambio-usario');

const openCambioUsuarioModal = (event) => {
    event.preventDefault();     
    modalCambioUsuario.style.display = 'flex';
  }

const closeCambioUsuarioModal = () => {
    modalCambioUsuario.style.display = 'none';
}


// modal para editar perfil(correo)

const modalCambioCorreo = document.querySelector('#modal-cambio-correo');

const openCambioCorreoModal = (event) => {
    event.preventDefault();     
    modalCambioCorreo.style.display = 'flex';
  }

const closeCambioCorreoModal = () => {
    modalCambioCorreo.style.display = 'none';
}


// modal para editar perfil(contraseña)

const modalCambioContraseña = document.querySelector('#modal-cambio-contraseña');

const openCambioContraseñaModal = (event) => {
    event.preventDefault();     
    modalCambioContraseña.style.display = 'flex';
  }

const closeCambioContraseñaModal = () => {
    modalCambioContraseña.style.display = 'none';
}


// modal para editar perfil(imagen-perfil)

const modalEditImagenPerfil = document.querySelector('#modal-edit-imagen');

const openEditImagenPerfilModal = (event) => {
    event.preventDefault();     
    modalEditImagenPerfil.style.display = 'flex';
  }

const closeEditImagenPerfilModal = () => {
    modalEditImagenPerfil.style.display = 'none';
}








// modal para elegir libro de prestamos

// Abrir el modal
function abrirModal() {
    document.getElementById("modal-seleccionar-libro").style.display = "flex";
    cargarLibros();
}

// Cerrar el modal
function cerrarModal() {
    document.getElementById("modal-seleccionar-libro").style.display = "none";
}



// prevenir la recarga de la pagina para buscar el libro en el modal

let currentSearchTerm = '';

function cargarLibros(url = '/App1/prestamos/') {
    // Si la URL no incluye el término de búsqueda, añádelo
    if (!url.includes('txtbuscar2=') && currentSearchTerm) {
        url += (url.includes('?') ? '&' : '?') + 'txtbuscar2=' + encodeURIComponent(currentSearchTerm);
    }

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.libros').innerHTML = data.html;
        setupPaginationLinks();
    })
    .catch(error => console.error('Error al cargar libros:', error));
}

function setupPaginationLinks() {
    const paginationLinks = document.querySelectorAll('.pagination-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            let url = this.getAttribute('href');
            
            // Añadir el término de búsqueda actual a la URL de paginación
            if (currentSearchTerm) {
                url += (url.includes('?') ? '&' : '?') + 'txtbuscar2=' + encodeURIComponent(currentSearchTerm);
            }
            
            cargarLibros(url);
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-busqueda');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        currentSearchTerm = formData.get('txtbuscar2');
        const query = new URLSearchParams(formData).toString();

        cargarLibros(`/App1/prestamos/?${query}`);
    });

    // Configurar los enlaces de paginación iniciales
    setupPaginationLinks();
});

