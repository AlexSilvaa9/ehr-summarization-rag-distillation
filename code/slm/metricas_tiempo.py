import os
import json
from pathlib import Path
import time
import ollama
import statistics
# Directorios y configuraciones iniciales
datos = '../../common_data/entradas_tiempo/'
ruta_contextos = '../../common_data/contextos_tiempo/'
temperaturas = [#0.2
                #, 0.5
                 0.8]

semilla = 42
modelos = [
    "qwen:14b",
    "llama3.1",
    "mistral",
    "phi4",
    "deepseek-r1:14b",
    "deepseek-r1:8b"
 #   ,'phi3','gemma2'
]
ruta_res = 'resultados/'

# Crear directorio de resultados si no existe
os.makedirs(ruta_res, exist_ok=True)

# Lectura de contextos
contextos = []
for nombre in os.listdir(ruta_contextos):
    if nombre.endswith(".txt"):
        contextos.append(nombre)

# Función para leer archivos de contexto
def leer_contexto(ruta_contexto):
    with open(ruta_contexto, mode='r', encoding='utf-8-sig') as f:
        return f.read()

# Lectura de patrones de entrada y salidas esperadas
nombres_ficheros = set([nombre_archivo.replace(".txt", "") for nombre_archivo in os.listdir(datos) if nombre_archivo.endswith(".txt")])
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


        



def conversar(nombre, texto, nom_modelo, ruta_res, sem, temp,contexto):
        fichero_res = ruta_res + nom_modelo + "-" + nombre + '-' + contexto.replace(".txt","") + '_temp_' + f'{temp}' + '.json'
        
        # si no permite un mensaje grande
        # resto = texto
        # maxc = 1000 # Número de caracteres de cada fragmento de mensaje
        # mensajes = []
        # while len(resto) > 0:
        #     mensajes.append({'role': 'user', 'content': resto[0:maxc]})
        #     resto = resto[maxc:]
        print('conversando...')
        respuesta = ollama.chat(model = nom_modelo,
                                messages = [{'role': 'user', 'content': texto}],
                                options = {'temperature': temp, 'seed': sem})

        contenido_respuesta = respuesta['message']['content'].replace('\n', '')
        print('respuesta obtenida')
        # Guardar resultados en JSON
        resultado_json = {
            'modelo': nom_modelo,
            'temperature': temp,
            'respuesta': contenido_respuesta
        }
    
        return contenido_respuesta

tiempo = {}
# Ejecutar el proceso completo
for modelo in modelos:
    for contexto in contextos:
        nombre_modelo = modelo + "_test"
        contexto_texto = leer_contexto(os.path.join(ruta_contextos, contexto))
       
        # verificar si el modelo ya existe
        if nombre_modelo in [model[0] for model in ollama.list()]:
            ollama.delete(nombre_modelo)
            print('modelo eliminado')
        print(f'creando modelo {modelo}, {contexto}')
        ollama.create(model=nombre_modelo, system=contexto_texto,from_=modelo)
        print(f'creado modelo {modelo}, {contexto}')
        for temp in temperaturas:
            for nombre_archivo, (contenido, salida_esperada) in info.items():
                tiempo_inicial = time.time()
                salida_modelo = conversar(
                    nombre=nombre_archivo.replace(".txt", ""),
                    texto=contenido,
                    nom_modelo=nombre_modelo,
                    ruta_res=ruta_res,
                    sem=semilla,
                    temp=temp,
                    contexto=contexto
 
                )
                tiempo_transcurrido = time.time() - tiempo_inicial
                if modelo not in tiempo:
                    tiempo[modelo] =  [tiempo_transcurrido]
                else:
                    tiempo[modelo].append(tiempo_transcurrido)
                
        
        ollama.delete(nombre_modelo)

# Guardar resultados en CSV y hacer media y desviación
for modelo, tiempos in tiempo.items():
    media = statistics.mean(tiempos)
    desviacion = statistics.stdev(tiempos)
    print(f"Modelo: {modelo}, Media: {media:.2f} segundos, Desviación: {desviacion:.2f} segundos")
    # Guardar en CSV
    with open(f"tiempos_{modelo}.csv", 'w', encoding='utf-8') as f:
        f.write("Modelo,Media,Desviación\n")
        f.write(f"{modelo},{media:.2f},{desviacion:.2f}\n")