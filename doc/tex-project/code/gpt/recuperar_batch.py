import os
from openai import OpenAI

def obtener_api():
    openai = OpenAI()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Error: No se encontró la clave de la API. Configura la variable de entorno 'OPENAI_API_KEY'.")
    return openai

def recuperar_batch(file_name):
    openai = obtener_api()
    file_response = openai.files.content(file_name)
    return file_response.text

if __name__ == "__main__":
    file_name = 'file-PWeoYjCEL9az9Q3djxosY7'
    with open('respuesta_batch.json', 'w') as batch_response_file:
        batch_response_file.write(recuperar_batch(file_name))