import os
import json

json_entrada = 'respuesta_batch.json'
carpeta_salida = 'archivos'
with open(json_entrada, 'r') as file:
    while linea:=file.readline():
        data = json.loads(linea)
        with open(f'{carpeta_salida}/respuesta_{data["custom_id"]}', 'w') as f:
            f.write(str(data["response"]["body"]["choices"][0]["message"]["content"]))

print('Proceso terminado')