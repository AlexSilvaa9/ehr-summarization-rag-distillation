import os
from openai import OpenAI

def obtener_api():
    openai = OpenAI()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Error: No se encontró la clave de la API. Configura la variable de entorno 'OPENAI_API_KEY'.")
    return openai

def subir_batch(jsonl_file):
    openai = obtener_api()

    # Subir archivo a Batch API
    batch_input_file = openai.files.create(
        file=open(jsonl_file, 'rb'),
        purpose='batch'
    )

    print(f"Archivo de entrada subido con ID: {batch_input_file.id}")

    # Crear un trabajo batch
    batch_job = openai.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "Resumen de historiales clínicos prompt templates"}
    )

    print(f"Trabajo batch creado con ID: {batch_job.id}")
    return str(batch_job)
# Subir batch y guardar respuesta
if __name__ == "__main__":
    jsonl_file = 'batch_input.jsonl'
    batch_job = subir_batch(jsonl_file)
    
    with open('batch_job_id.txt', 'w') as batch_job_file:
        batch_job_file.write(batch_job)

    #  File "/home/alex/Documents/UNI/Cuarto/segundo_cuatri/tfg/code/gpt_api_EHR_summarization/subir_batch.py", line 38, in <module>
    #batch_job_file.write(batch_job)
    #TypeError: write() argument must be str, not Batch
    print(f"Trabajo batch subido con éxito. ID: {batch_job.id}")
