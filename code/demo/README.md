
# Aplicación de Resumen Médico con Ollama

Esta aplicación utiliza FastAPI para procesar historiales médicos y generar resúmenes mediante el modelo Ollama. Además, permite ver la diferencia entre el texto original y el resumen generado.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalados los siguientes componentes:

- Python 3.8 o superior.
- FastAPI.
- Uvicorn.
- Ollama (modelo de resumen de texto).

## Instalación

### 1. Clona o descarga el repositorio

Si aún no tienes los archivos de la aplicación, clónalos o descárgalos en tu máquina:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### 2. Crea un entorno virtual (opcional, pero recomendado)

Es recomendable crear un entorno virtual para gestionar las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate  # En Windows
```

### 3. Instala las dependencias

Instala las librerías necesarias con `pip`:

```bash
pip install fastapi uvicorn ollama
```

Asegúrate de que `ollama` esté correctamente instalado y configurado en tu entorno.

### 4. Configura el modelo de Ollama

Asegúrate de que tienes el modelo de Ollama que necesitas para la generación de resúmenes. El modelo debe estar configurado correctamente y ser accesible desde la aplicación.

### 5. Estructura de Archivos

La estructura de directorios debe ser la siguiente:

```
app/
├── static/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── main.py
```

### 6. Ejecución de la aplicación

Para ejecutar la aplicación, usa el siguiente comando:

```bash
uvicorn app.main:app --reload
```

Esto iniciará el servidor de desarrollo de FastAPI. La aplicación estará disponible en [http://localhost:8000](http://localhost:8000).

## Uso

### Interfaz Web

Una vez que la aplicación esté en funcionamiento, puedes acceder a ella en tu navegador. La interfaz web te permitirá ingresar un historial médico (o cargarlo) y obtener un resumen del mismo.

- **Área de texto**: Ingresa el historial médico.
- **Botón**: Haz clic en "Generar Resumen" para procesar el historial médico.
- **Resultados**: Se mostrarán tanto el historial original como el resumen generado.

### API REST

La aplicación también ofrece una API REST en el endpoint `/resumen`. Puedes enviar un historial médico en formato JSON y recibir un resumen en respuesta. Ejemplo de solicitud POST:

```bash
POST http://localhost:8000/resumen
Content-Type: application/json

{
  "historial": "Aquí va el historial médico completo del paciente..."
}
```

La respuesta será un objeto JSON con el historial original y el resumen generado:

```json
{
  "original": "Aquí va el historial médico completo del paciente...",
  "resumen": "Este es el resumen generado del historial médico..."
}
```

## Contribuciones

Si deseas contribuir a la aplicación, puedes abrir un *pull request* con las mejoras que desees realizar. Para reportar errores, abre un *issue* en el repositorio.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
```

### Instrucciones adicionales

1. **Ollama**: Asegúrate de tener acceso a la API o el modelo que utilizarás para el resumen. Puede que necesites obtener una clave de API o realizar configuraciones adicionales según tu caso.

2. **Entorno**: Si tienes algún problema con las dependencias o las versiones de las librerías, asegúrate de revisar las versiones compatibles y la documentación de cada una.

Este `README.md` cubre la instalación, configuración y ejecución básica del proyecto, además de proporcionar instrucciones de uso tanto para la interfaz web como para la API. ¡Espero que te sirva!