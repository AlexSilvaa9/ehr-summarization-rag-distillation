import os
import json
from pathlib import Path

import ollama
import time
# Directorios y configuraciones iniciales
datos = '../../common_data/entradas/'

temperaturas = [0.2
                #, 0.5
                , 0.8]
semilla = 42
modelos = [
    # "qwen:14b",
    # "llama3.1",
    # "phi4",
    # "mistral",
    # "deepseek-r1:14b",
    # "deepseek-r1:8b",
    "llama3.2"
]
ruta_res = 'resultados/'

# Crear directorio de resultados si no existe
os.makedirs(ruta_res, exist_ok=True)

# Lectura de contextos

contexto= """
Eres un asistente médico diseñado para generar resúmenes de registros médicos electrónicos (EMRs).  

Tu tarea es proporcionar un resumen detallado del siguiente registro médico, cubriendo la siguiente información:  

- **Historial médico personal y familiar**: Enumera el historial médico personal y familiar del paciente.  
- **Diagnósticos previos**: Enumera los diagnósticos médicos previos del paciente.  
- **Medicamentos y dosis relevantes**: Detalla los medicamentos que el paciente está tomando junto con sus dosis.  
- **Procedimientos significativos**: Enumera cualquier procedimiento médico significativo que el paciente haya experimentado.  
- **Variables clínicas clave**: Proporciona información clave como RE y RP, TNM o tamaños tumorales.  
"""

contexto_fusion = """" \
"Eres un asistente médico diseñado para generar resúmenes de registros médicos electrónicos (EMRs).  

Tu tarea es proporcionar un resumen detallado dados dos resúmenes de distintas partes de un historial, cubriendo la siguiente información:  

- **Historial médico personal y familiar**: Enumera el historial médico personal y familiar del paciente.  
- **Diagnósticos previos**: Enumera los diagnósticos médicos previos del paciente.  
- **Medicamentos y dosis relevantes**: Detalla los medicamentos que el paciente está tomando junto con sus dosis.  
- **Procedimientos significativos**: Enumera cualquier procedimiento médico significativo que el paciente haya experimentado.  
- **Variables clínicas clave**: Proporciona información clave como RE y RP, TNM o tamaños tumorales.  
- **Resumen general**: Ofrece un resumen completo del historial médico del paciente, asegurándote de incluir toda la información relevante sin omitir detalles clave." \
"""

# Lectura de patrones de entrada y salidas esperadas
nombres_ficheros = {nombre.replace(".txt", "") for nombre in os.listdir(datos) if nombre.endswith(".txt")}
info = {}

for nombre_fichero in nombres_ficheros:
    with open(os.path.join(datos, f"{nombre_fichero}.txt"), mode='r', encoding='utf-8-sig') as f:
        contenido = f.read()
    if os.path.isfile(os.path.join(datos, f"{nombre_fichero}.json")):
        with open(os.path.join(datos, f"{nombre_fichero}.json"), mode='r', encoding='utf-8-sig') as f:
            salida_esperada = f.read()
    else:
        salida_esperada = None
    info[nombre_fichero] = [contenido, salida_esperada]

# Función para dividir el texto en dos partes
def dividir_texto(texto):
    mitad = len(texto) // 2
    return texto[:mitad], texto[mitad:]

# Función para conversar con el modelo
def conversar(nombre, texto, nom_modelo, ruta_res, sem, temp, contexto,guarda=False):
    fichero_res = ruta_res + nombre +'-' + "chunked" + '_temp_' + f'{temp}' + '.json'
    print(fichero_res)
    if os.path.isfile(fichero_res):
        with open(fichero_res, 'r', encoding='utf-8') as file:
            resultado_cargado = json.load(file)
        return resultado_cargado['respuesta']
    
    print('Conversando...')
    respuesta = ollama.chat(model=nom_modelo, messages=[{'role': 'user', 'content': texto}], options={'temperature': temp, 'seed': sem})
    contenido_respuesta = respuesta['message']['content'].replace('\n', '')
    print('Respuesta obtenida')
    if guarda:
        # Guardar resultados en JSON
        resultado_json = {'modelo': nom_modelo, 'temperature': temp, 'respuesta': contenido_respuesta}
        with open(fichero_res, 'w', encoding='utf-8') as outfile:
            json.dump(resultado_json, outfile, ensure_ascii=False, indent=4)
        
    return contenido_respuesta

# Ejecutar el proceso completo
for modelo in modelos:
    
    nombre_modelo = modelo + "_test"

    # Verificar si el modelo ya existe
    if nombre_modelo in [model[0] for model in ollama.list()]:
        ollama.delete(nombre_modelo)
        print('Modelo eliminado')
    
    print(f'Creando modelo {modelo}, {contexto}')
    ollama.create(model=nombre_modelo, system=contexto, from_=modelo)
    print(f'Creado modelo {modelo}, {contexto}')
    
    for temp in temperaturas:
        for nombre_archivo, (contenido, salida_esperada) in info.items():
            print(f"Procesando archivo: {nombre_archivo}, modelo: {modelo}, temp: {temp}, contexto: {contexto}")
            # comprobar si el archivo ya existe
            fichero_res = ruta_res + nombre_modelo + '-' + nombre_archivo +'--' + "chunked" + '_temp_' + f'{temp}' + '.json'
            if os.path.isfile(fichero_res):
                print(f"El archivo {fichero_res} ya existe. Saltando...")
                # mala practica, cambiar
                continue
            parte1, parte2 = dividir_texto(contenido)
            resumen1 = conversar(nombre_modelo + "_parte1", parte1, nombre_modelo, ruta_res, semilla, temp, contexto)
            resumen2 = conversar(nombre_modelo + "_parte2", parte2, nombre_modelo, ruta_res, semilla, temp, contexto)
            resumen_final = conversar(nombre_modelo + "-" +nombre_archivo + "-", resumen1 + " " + resumen2, nombre_modelo, ruta_res, semilla, temp, contexto_fusion, guarda=True)
            
            print('Conversación finalizada')
        
    ollama.delete(nombre_modelo)
