
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


// modal para agregar libro

const modalAdd1 = document.querySelector('#modalAdd1');

const openModal = (event) => {
    event.preventDefault(); // Prevenir el comportamiento predeterminado del evento
    modalAdd1.style.display = 'flex';
  }

const closeModal = () => {
    modalAdd1.style.display = 'none';
} 

// boton para agregar la portada

let uploadButton = document.getElementById("upload-button");
let lugarPortada = document.getElementById("lugar-portada");
let nombreArchivo = document.getElementById("nombre-archivo");

uploadButton.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadButton.files[0]);
    console.log(uploadButton.files[0]);
    reader.onload = () => {
        lugarPortada.setAttribute("src",reader.result);
    }
    nombreArchivo.textContent = uploadButton.files[0].name;
}

let editUploadButton = document.getElementById("edit-upload-button");
let editLugarPortada = document.getElementById("edit-lugar-portada");
let editNombreArchivo = document.getElementById("edit-nombre-archivo");

editUploadButton.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(editUploadButton.files[0]);
    console.log(editUploadButton.files[0]);
    reader.onload = () => {
        editLugarPortada.setAttribute("src",reader.result);
    }
    editNombreArchivo.textContent = editUploadButton.files[0].name;
}


// Función para mostrar el mensaje de que libro ha sido agregado

document.addEventListener('DOMContentLoaded', function() {
    var messageContainer = document.getElementById('message-container');
    if (messageContainer && messageContainer.innerHTML.trim() !== '') {
        var message = messageContainer.innerText.trim();
        alert(message);
    }
});


function showModal(message) {
    var modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.left = '50%';
    modal.style.top = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = 'white';
    modal.style.padding = '20px';
    modal.style.border = '1px solid black';
    modal.style.zIndex = '1000';
    modal.innerHTML = `
        <p>${message}</p>
        <button onclick="this.parentElement.remove()">Cerrar</button>
    `;
    document.body.appendChild(modal);
}


// modal para editar libros

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.editar-libro').forEach(function(elemento) {
        elemento.addEventListener('click', function() {
            var libroId = this.getAttribute('data-libro-id');
            console.log('Editando libro con ID:', libroId);
            editarLibro(libroId);
        });
    });
});


function editarLibro(libroId) {
    // Mostrar el modal
    document.getElementById('modalEdit').style.display = 'flex';
    
    // Realizar una solicitud AJAX para obtener los datos del libro
        const url = `/App1/obtener_libro/${libroId}/`;
        const form = document.getElementById('editLibroForm');
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(libro => {
            console.log('Datos del libro recibidos:', libro);
            // Rellenar el formulario con los datos del libro
            document.getElementById('edit-titulo').value = libro.titulo || '';
            document.getElementById('edit-autor').value = libro.autor || '';
            document.getElementById('edit-editorial').value = libro.editorial || '';
            document.getElementById('edit-fecha').value = libro.fecha || '';
            document.getElementById('edit-isbn').value = libro.isbn || '';
            document.getElementById('edit-numero_pags').value = libro.numero_pags || '';
            document.getElementById('edit-numero_topografia').value = libro.numero_topografia || '';
            document.getElementById('edit-numero_ejemplar').value = libro.numero_ejemplar || '';
            document.getElementById('edit-descripcion').value = libro.descripcion || '';
            
            if (libro.portada) {
                document.getElementById('edit-lugar-portada').src = libro.portada;
                document.getElementById('edit-nombre-archivo').textContent = 'Portada actual';
            } else {
                document.getElementById('edit-lugar-portada').src = '';
                document.getElementById('edit-nombre-archivo').textContent = 'Sin portada';
            }
            
            document.getElementById('editLibroForm').action = `/App1/editar_libro/${libroId}/`;
            form.action = form.action.replace('/0/', `/${libroId}/`);
        })
        .catch(error => {
            console.error('Error al obtener datos del libro:', error);
            alert('Hubo un error al cargar los datos del libro. Por favor, intenta de nuevo.');
        });
}

function closeEditModal() {
    document.getElementById('modalEdit').style.display = 'none';
}


// modal para ver libro

function verLibro(libroId) {
    // Mostrar el modal
    document.getElementById('modalView').style.display = 'flex';
    
    // Realizar una solicitud AJAX para obtener los datos del libro
    const url = `/App1/obtener_libro/${libroId}/`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(libro => {
            // Rellenar el modal con los datos del libro
            const modalContent = document.querySelector('#modalView .modal-contenedor1');
            modalContent.innerHTML = `
                <div onclick="closeViewModal()" class="close-modal">X</div>
                <div class="libro-ver">
                    <div class="portada-titulo">
                        <img src="${libro.portada || '/static/default_cover.jpg'}" alt="${libro.titulo}">
                        <div class="titulo-id">
                            <p><strong># </strong>${libro.id}</p>
                            <h4>${libro.titulo}</h4>
                        </div>
                    </div>
                    <p><strong>ISBN: </strong>${libro.isbn}</p>
                    <p><strong>Autor: </strong>${libro.autor}</p>
                    <p><strong>Editorial: </strong>${libro.editorial}</p>
                    <p><strong>Fecha: </strong>${libro.fecha}</p>
                    <p><strong>Numero de paginas: </strong>${libro.numero_pags}</p>
                    <p><strong>Numero de topografia: </strong>${libro.numero_topografia}</p>
                    <p><strong>Numero de ejemplar: </strong>${libro.numero_ejemplar}</p>
                    <p><strong>Descripción: </strong>${libro.descripcion}</p>
                </div>
            `;
        })
        .catch(error => {
            console.error('Error al obtener datos del libro:', error);
            alert('Hubo un error al cargar los datos del libro. Por favor, intenta de nuevo.');
        });
}

function closeViewModal() {
    document.getElementById('modalView').style.display = 'none';
}


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
