import os
import json
from pathlib import Path
import gc
from unsloth import FastLanguageModel
from transformers import TextStreamer
import torch

# ========== CONFIGURACIÓN ==========
# Paths
datos = '../../common_data/entradas/'
ruta_res = 'resultados/'

# Parámetros
temperaturas = [0.2]
semilla = 42
max_seq_length = 10000
dtype = None
load_in_4bit = True

# Cargar modelo LoRA con unsloth
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name= "unsloth/Llama-3.2-3B-Instruct",
    # "lora_model",  # Cambia si tu carpeta tiene otro nombre
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)
FastLanguageModel.for_inference(model)
print(tokenizer.chat_template)

# Crear carpeta de resultados si no existe
os.makedirs(ruta_res, exist_ok=True)

# ========== CONTEXTOS ==========
contexto = """
Eres un asistente médico diseñado para generar resúmenes de registros médicos electrónicos (EMRs).  
Tu tarea es proporcionar un resumen detallado del siguiente registro médico, cubriendo la siguiente información:  
- **Historial médico personal y familiar**  
- **Diagnósticos previos**  
- **Medicamentos y dosis relevantes**  
- **Procedimientos significativos**  
- **Variables clínicas clave** (como RE y RP, TNM o tamaños tumorales)
"""

contexto_fusion = """
Eres un asistente médico diseñado para generar resúmenes de registros médicos electrónicos (EMRs).  
Tu tarea es proporcionar un resumen detallado dados dos resúmenes de distintas partes de un historial, cubriendo:  
- **Historial médico personal y familiar**  
- **Diagnósticos previos**  
- **Medicamentos y dosis relevantes**  
- **Procedimientos significativos**  
- **Variables clínicas clave**  
- **Resumen general** del historial médico completo, sin omitir detalles clave
"""

# ========== FUNCIONES ==========
def dividir_texto(texto):
    mitad = len(texto) // 2
    return texto[:mitad], texto[mitad:]

def conversar_local(nombre, texto, ruta_res, sem, temp, contexto, guarda=False):
    fichero_res = os.path.join(ruta_res, f"{nombre}_temp_{temp}.json")
    print(fichero_res)
    if os.path.isfile(fichero_res):
        with open(fichero_res, 'r', encoding='utf-8') as file:
            resultado_cargado = json.load(file)
        return resultado_cargado['respuesta']

    print("Conversando...")

    messages = [
        {"role": "system", "content": contexto},
        {"role": "user", "content": texto}
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to("cuda")
 
    attention_mask = (inputs != tokenizer.pad_token_id).long()
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    output = model.generate(
        input_ids=inputs,
        attention_mask=attention_mask,
        streamer=streamer,
        max_new_tokens=512,
        temperature=temp,
        do_sample=True,
        top_p=0.9,
    )

    respuesta = tokenizer.decode(output[0], skip_special_tokens=True,).strip()

    if guarda:
        resultado_json = {
            'modelo': 'lora_model',
            'temperature': temp,
            'respuesta': respuesta
        }
        with open(fichero_res, 'w', encoding='utf-8') as outfile:
            json.dump(resultado_json, outfile, ensure_ascii=False, indent=4)

        # Limpieza de memoria tras la conversación
    del inputs, attention_mask, output
    gc.collect()
    torch.cuda.empty_cache()


    return respuesta

# ========== CARGA DE DATOS ==========
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

# ========== PROCESAMIENTO ==========
for temp in temperaturas:
    for nombre_archivo, (contenido, salida_esperada) in info.items():
        print(f"Procesando archivo: {nombre_archivo}, temp: {temp}")

        parte1, parte2 = dividir_texto(contenido)

        resumen1 = conversar_local(f"{nombre_archivo}_parte1", parte1, ruta_res, semilla, temp, contexto)
        resumen2 = conversar_local(f"{nombre_archivo}_parte2", parte2, ruta_res, semilla, temp, contexto)

        resumen_final = conversar_local(f"{nombre_archivo}_fusion", resumen1 + " " + resumen2, ruta_res, semilla, temp, contexto_fusion, guarda=True)

        print("Conversación finalizada")
