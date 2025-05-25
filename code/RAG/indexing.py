import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os
from os import path
import json
documentos_rag_path = "../../common_data/medmcqa_docs.json"
# Paso 1: Carga modelo de embeddings ligero
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paso 2: Crea base vectorial en memoria
client = chromadb.PersistentClient()

collection = client.create_collection(name="medicina")
documentos = []
with open(documentos_rag_path, "r") as file:
    for line in file:
        documentos.append(json.loads(line))
# Cargar documentos médicos desde el archivo JSON
# Paso 3: Documentos médicos (prueba para ver si funciona)


# Paso 4: Inserta en colección
for i, texto in enumerate(documentos):
    vector = model.encode(texto["question"]).tolist()

    respuesta = texto.get("exp")
    if respuesta is None:
        respuesta = "Sin respuesta"

    collection.add(
        documents=[texto["question"]],
        embeddings=[vector],
        metadatas=[{"respuesta": respuesta}],
        ids=[f"doc{i}"]
    )


