import os
import json

def generar_jsonl(contextos_dir, entradas_dir, jsonl_file):
    with open(jsonl_file, 'w', encoding='utf-8') as jsonl:
        for contexto_nombre in os.listdir(contextos_dir):
            if contexto_nombre.endswith('.txt'):
                with open(os.path.join(contextos_dir, contexto_nombre), 'r', encoding='utf-8') as ctx_file:
                    contexto = ctx_file.read()

                for archivo_nombre in os.listdir(entradas_dir):
                    if archivo_nombre.endswith('.txt'):
                        with open(os.path.join(entradas_dir, archivo_nombre), 'r', encoding='utf-8') as entrada_file:
                            contenido = entrada_file.read()

                        # Crear una solicitud para cada combinación de contexto y archivo
                        solicitud = {
                            "custom_id": f"{archivo_nombre}_with_{contexto_nombre}",
                            "method": "POST",
                            "url": "/v1/chat/completions",
                            "body": {
                                "model": "gpt-4o-mini",
                                "messages": [
                                    {"role": "system", "content": contexto},
                                    {"role": "user", "content": f"<record>\n{contenido}"}
                                ],
                                "max_tokens": 500
                            }
                        }
                        jsonl.write(json.dumps(solicitud) + '\n')

    print(f"Archivo {jsonl_file} generado para Batch API.")

if __name__ == "__main__":
    common_data_dir = '../../common_data'
    contextos_dir = os.path.join(common_data_dir, 'contextos')
    entradas_dir = os.path.join(common_data_dir, 'entradas')
    jsonl_file = 'batch_input.jsonl'
    generar_jsonl(contextos_dir, entradas_dir, jsonl_file)

    print("JSONL generado con éxito.")
