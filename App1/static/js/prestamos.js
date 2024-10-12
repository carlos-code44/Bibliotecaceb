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


// seleccionar libro

function seleccionarLibro(libroId, titulo, autor) {
    document.getElementById('libro_id').value = libroId;
    document.getElementById('libro-seleccionado').innerHTML = `
        <p><strong>Libro seleccionado:</strong> ${titulo} por ${autor}</p>
    `;
    cerrarModal();
}




// prevenir la recarga de la pagina para buscar el libro en el modal

let currentSearchTerm = '';

function cargarLibros(url = '/App1/prestamos/') {
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
        updatePaginationLinks(data);
        setupLibroSeleccion();
    })
    .catch(error => console.error('Error al cargar libros:', error));
}

function updatePaginationLinks(data) {
    const paginationContainer = document.querySelector('.opcionesfinales');
    paginationContainer.innerHTML = '';

    if (data.has_previous) {
        const prevLink = createPaginationLink('Anterior', data.previous_page_number);
        paginationContainer.appendChild(prevLink);
    }

    if (data.has_next) {
        const nextLink = createPaginationLink('Siguiente', data.next_page_number);
        paginationContainer.appendChild(nextLink);
    }

    setupPaginationLinks();
}

function createPaginationLink(text, pageNumber) {
    const link = document.createElement('a');
    link.href = `?pagina=${pageNumber}`;
    link.className = 'pagination-link';
    link.textContent = text;
    return link;
}



function setupLibroSeleccion() {
    const libros = document.querySelectorAll('.libro');
    libros.forEach(libro => {
        libro.addEventListener('click', function() {
            const disponible = this.getAttribute('data-disponible') === 'true';
            if (!disponible) {
                alert('Este libro no está disponible para préstamo.');
                return;
            }
            const libroId = this.getAttribute('data-id');
            const titulo = this.querySelector('h4').textContent;
            const autor = this.querySelector('p:nth-child(3)').textContent.replace('Autor: ', '');
            seleccionarLibro(libroId, titulo, autor);
        });
    });
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



// ---------------------------------------escanear codigo de barras-----------------------------------------


let scannerIsRunning = false;

document.addEventListener('DOMContentLoaded', function() {
    const scanButton = document.getElementById('scan-button');
    const scannerContainer = document.getElementById('scanner-container');

    scanButton.addEventListener('click', function(e) {
        e.preventDefault(); // Previene el comportamiento por defecto
        e.stopPropagation(); // Evita que el evento se propague al formulario
        
        if (scannerIsRunning) {
            Quagga.stop();
            scannerContainer.style.display = 'none';
            scannerIsRunning = false;
        } else {
            scannerContainer.style.display = 'flex';
            startScanner();
        }
    });
});

function startScanner() {
    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#interactive'),
            constraints: {
                width: 480,
                height: 320,
                facingMode: "environment"
            },
        },
        decoder: {
            readers: [
                "ean_reader",
                "ean_8_reader",
                "code_39_reader",
                "code_128_reader",
                "upc_reader",
                "upc_e_reader"
            ],
            debug: {
                showCanvas: true,
                showPatches: true,
                showFoundPatches: true,
                showSkeleton: true,
                showLabels: true,
                showPatchLabels: true,
                showRemainingPatchLabels: true,
                boxFromPatches: {
                    showTransformed: true,
                    showTransformedBox: true,
                    showBB: true
                }
            }
        },
    }, function(err) {
        if (err) {
            console.log(err);
            return;
        }
        console.log("Initialization finished. Ready to start");
        Quagga.start();
        scannerIsRunning = true;
    });

    Quagga.onDetected(function(result) {
        const code = result.codeResult.code;
        document.querySelector('input[name="txtbuscar"]').value = code;
        Quagga.stop();
        document.getElementById('scanner-container').style.display = 'none';
        scannerIsRunning = false;
        // En lugar de enviar el formulario automáticamente, podemos activar el botón de búsqueda
        document.querySelector('button[name="btnbuscar"]').click();
    });
}