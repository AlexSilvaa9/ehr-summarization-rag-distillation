import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os
from os import path
import json

entradas_path = "../../common_data/entradas"
ruta_res = "./resultados/"
nombre_modelo = "phi4"
semilla = 42
temp = 0.2

contexto_final = """
Eres un asistente médico diseñado para generar resúmenes de registros médicos electrónicos (EMRs) en Español.  
Tu tarea es proporcionar un resumen detallado del siguiente registro médico, cubriendo la siguiente información:  
- **Historial médico personal y familiar**
- **Diagnósticos previos**
- **Medicamentos y dosis relevantes**
- **Procedimientos significativos**
- **Variables clínicas clave**
"""

contexto_fusion = """
Eres un asistente médico diseñado para generar resúmenes de registros médicos electrónicos (EMRs) en Español.  
Tu tarea es proporcionar un resumen detallado dados dos resúmenes de distintas partes de un historial, cubriendo la siguiente información(y sin preliminares):  
- **Historial médico personal y familiar**
- **Diagnósticos previos**
- **Medicamentos y dosis relevantes**
- **Procedimientos significativos**
- **Variables clínicas clave**
- **Resumen general**
"""

# Inicializar modelo y cliente
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient()
collection = client.get_collection('medicina')

# Crear modelos de conversación
ollama.create(model="phi4_division", system=contexto_final, from_='phi4')
ollama.create(model="phi4_fusion", system=contexto_fusion, from_='phi4')

def consulta_rag(pregunta, n=3):
    query_vector = model.encode(pregunta).tolist()
    resultados = collection.query(query_embeddings=[query_vector], n_results=n)
    respuestas = [meta["respuesta"] for meta in resultados["metadatas"][0]]
    return respuestas

def desglosar_pregunta(historial):
    prompt = f"""You are a medical assistant specialized in processing clinical records. Your task is to analyze the following patient's medical history and extract a list of key ideas...

    Medical history:
    {historial}
    Return a list of key ideas for RAG search, without repeating concepts and with a maximum of 5 items, without introduction or conclusion. Each idea should be on a separate line, and there should be no additional text or numbering.
    """
    respuesta = ollama.chat(model="phi4", messages=[{"role": "user", "content": prompt}], options={'temperature': 0.2})
    return [idea for idea in respuesta['message']['content'].split("\n") if idea]

def conversar(nombre, texto, ruta_res, sem, temp, contexto="", guarda=False, nombre_archivo=None):
    print(f'Conversando con {nombre_archivo}...')
    respuesta = ollama.chat(model=nombre, messages=[{'role': 'user', 'content': contexto + texto}], options={'temperature': temp, 'seed': sem})
    contenido_respuesta = respuesta['message']['content'].replace('\n', '')
    if guarda:
        fichero_res = path.join(ruta_res, nombre_archivo + '_respuesta.json')
        if os.path.isfile(fichero_res):
            with open(fichero_res, 'r', encoding='utf-8') as file:
                return json.load(file)['respuesta']
        with open(fichero_res, 'w', encoding='utf-8') as outfile:
            json.dump({'modelo': nombre, 'temperature': temp, 'respuesta': contenido_respuesta}, outfile, ensure_ascii=False, indent=4)
    return contenido_respuesta

def dividir_texto(texto):
    mitad = len(texto) // 2
    return texto[:mitad], texto[mitad:]

# Iterar sobre todos los archivos .txt
for archivo in os.listdir(entradas_path):
    if archivo.endswith(".txt"):
        historial_path = path.join(entradas_path, archivo)
        with open(historial_path, "r", encoding="utf-8") as file:
            historial = file.read()

        parte1, parte2 = dividir_texto(historial)

        desglose1 = desglosar_pregunta(parte1)
        contexto_rag1 = "\n".join([consulta_rag(idea, n=1)[0] for idea in desglose1])

        desglose2 = desglosar_pregunta(parte2)
        contexto_rag2 = "\n".join([consulta_rag(idea, n=1)[0] for idea in desglose2])

        resumen1 = conversar("phi4_division", parte1, ruta_res, semilla, temp, contexto=contexto_rag1)
        resumen2 = conversar("phi4_division", parte2, ruta_res, semilla, temp, contexto=contexto_rag2)

        resumen_final = conversar("phi4_fusion", resumen1 + " " + resumen2, ruta_res, semilla, temp, guarda=True, nombre_archivo=archivo.replace('.txt', ''))

print("Proceso completado para todas las entradas.")
