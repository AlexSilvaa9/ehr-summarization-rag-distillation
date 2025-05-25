document.addEventListener("DOMContentLoaded", () => {
    const dropContainer = document.querySelector('.drop-container');
    const fileInput = document.getElementById('file-input');

    if (!dropContainer || !fileInput) {
        console.warn("No se encontró el contenedor de arrastre o el input.");
        return;
    }

    dropContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropContainer.classList.add('hover'); // opcional, si quieres añadir estilo
    });

    dropContainer.addEventListener('dragleave', () => {
        dropContainer.classList.remove('hover');
    });

    dropContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        dropContainer.classList.remove('hover');

        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;

            // Opcional: lanzar el resumen automáticamente
            // obtenerResumen(); 
        }
    });
});


function obtenerResumen() {
    console.log("Iniciando la función obtenerResumen...");

    // Obtener el spinner de carga
    const loadingElement = document.getElementById('loading');
    const resumenContainer = document.querySelector('.result');
    if (loadingElement) {
        loadingElement.style.display = 'flex';
        resumenContainer.style.background = "rgba(219, 217, 217, 0.6)";

    } else {
        console.warn("Elemento con ID 'loading' no encontrado en el DOM.");
    }

    // Verificar si se ha seleccionado un archivo
    const fileInput = document.getElementById('file-input');
    if (!fileInput) {
        console.warn("Elemento con ID 'file-input' no encontrado.");
    }

    const file = fileInput ? fileInput.files[0] : null;
    console.log("Archivo seleccionado:", file);

    let historial;

    if (file) {
        console.log("Leyendo archivo...");
        const reader = new FileReader();
        reader.onload = function(event) {
            historial = event.target.result;
            console.log("Contenido del archivo leído correctamente.");
            const historialElement = document.getElementById('original');
          
            historialElement.textContent = historial;
          
            enviarResumen(historial);
        };
        reader.onerror = function(error) {
            console.error("Error al leer el archivo:", error);
        };
        reader.readAsText(file);
    } 

}

function enviarResumen(historial) {
    console.log("Enviando historial al servidor:", historial);

    fetch('/resumen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ historial: historial }),
    })
    .then(response => {
        console.log("Respuesta recibida del servidor:", response);

        if (response.ok && response.headers.get('Content-Type')?.includes('application/json')) {
            return response.json();
        } else {
            throw new Error('Respuesta del servidor no es JSON o ha ocurrido un error');
        }
    })
    .then(data => {
        console.log("Datos recibidos del servidor:", data);

        let htmlResumen = data.resumen;
        console.log("Resumen recibido:", htmlResumen);

        const resumenElement = document.getElementById('resumen');
        if (!resumenElement) {
            console.warn("Elemento con ID 'resumen' no encontrado.");
        } else {
            resumenElement.innerHTML = htmlResumen;
            console.log("Resumen insertado en el DOM.");
        }
        const loadingElement = document.getElementById('loading');
        const resumenContainer = document.querySelector('.result');
        if (loadingElement) {
            loadingElement.style.display = 'none';
            resumenContainer.style.backgroundColor = "#ffffff";


            console.log("Spinner ocultado.");

        }
    })
    .catch(error => {
        console.error("Error al generar el resumen:", error);

        if (loadingElement) {
            loadingElement.style.display = 'none';
        }

        const resumenElement = document.getElementById('resumen');
        if (resumenElement) {
            resumenElement.textContent = 'Hubo un error al generar el resumen: ' + error.message;
        }
    });
}
