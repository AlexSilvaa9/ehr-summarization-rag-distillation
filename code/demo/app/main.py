from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel  # Importa Pydantic para la validación
import ollama  # Asegúrate de instalar y configurar correctamente el modelo Ollama
import markdown
import time
# Inicializa la aplicación FastAPI
app = FastAPI()

# Monta la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Parámetros de configuración
TEMPERATURA = 0.2
SEMILLA = 42

# Contexto para el modelo de Ollama
contexto = """    
Eres un asistente médico diseñado para generar resúmenes de Historias Clínicas Electrónicas (EMRs, por sus siglas en inglés).

Tu tarea es proporcionar un resumen detallado del siguiente registro médico, cubriendo la siguiente información:

* **Antecedentes personales y familiares**: Enumera los antecedentes médicos personales y familiares.
* **Diagnósticos previos**: Enumera los diagnósticos médicos previos del paciente.
* **Medicamentos y dosis relevantes**: Detalla los medicamentos que está tomando el paciente, junto con sus dosis.
* **Procedimientos significativos**: Enumera cualquier procedimiento médico relevante al que se haya sometido el paciente.
* **Variables clínicas clave**: Incluye información importante como RE y RP, TNM o tamaños tumorales.
* **Resumen general**: Proporciona un resumen completo de la historia médica del paciente, asegurándote de incluir toda la información relevante sin omitir detalles importantes.

<registro>

{record}
"""

# Definir modelo de entrada para el historial
class HistorialRequest(BaseModel):
    historial: str  # Asegúrate de que el campo sea el mismo que el que usas en el frontend

# Cargar el modelo de Ollama
try:
    ollama.create(model='prod_model', system=contexto, from_='phi4')
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo Ollama: {e}")

# Ruta principal para servir el HTML
@app.get("/")
async def get_home():
    with open("app/static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content,
                        headers={"Cache-Control": "no-cache, no-store, must-revalidate"})

# Ruta para procesar el historial médico y generar el resumen
@app.post("/resumen")
async def generar_resumen(request: HistorialRequest):  # Usar Pydantic para recibir el JSON
    historial = request.historial  # Accede al historial desde el modelo Pydantic
    try:
        # Verifica si el historial está vacío
        if not historial.strip():
            raise HTTPException(status_code=400, detail="El historial médico no puede estar vacío.")
        
        # Procesa el historial usando el modelo de Ollama




        # respuesta = ollama.chat(model='prod_model',
        #                         messages=[{'role': 'user', 'content': historial}],
        #                         options={'temperature': TEMPERATURA, 'seed': SEMILLA})
        # Extrae el resumen de la respuesta de Ollama
        # resumen_md = respuesta['message']['content'].strip()
        time.sleep(5)
        with open("app/static/assets/resumen.txt") as f:
            resumen_md = f.read()
        # Simula la respuesta del modelo para pruebas


        # Convierte el resumen a HTML
        resumen = markdown.markdown(resumen_md)
        # Devuelve el historial original y el resumen generado
        return JSONResponse(content={
            "original": historial,
            "resumen": resumen
        })
    
    except Exception as e:
        # Maneja errores de procesamiento y devuelve un mensaje de error
        raise HTTPException(status_code=500, detail=f"Error al generar el resumen: {e}")
