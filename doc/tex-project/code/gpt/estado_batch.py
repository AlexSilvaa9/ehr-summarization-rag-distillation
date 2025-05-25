import os
from openai import OpenAI

def obtener_api():
    openai = OpenAI()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Error: No se encontró la clave de la API. Configura la variable de entorno 'OPENAI_API_KEY'.")
    return openai

def estado_batch(batch_job_id):
    openai = obtener_api()

    # Recuperar el estado del trabajo batch
    batch_job = openai.batches.retrieve(batch_job_id)
    #guardamos el estado del batch en un archivo

    return batch_job

batch_job_id = 'batch_67d87bc4e99c8190b1b9dc00cf6e7c9b'
with open('batch_job_status.txt', 'w') as batch_job_status_file:
        batch_job_status_file.write(str(estado_batch(batch_job_id)))

print(f"Estado del trabajo batch guardado con éxito en batch_job_status.txt.")