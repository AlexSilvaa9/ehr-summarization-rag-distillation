#!/bin/bash

# Directorio de trabajo
directorio="./resultados/"

# Cambiar al directorio especificado
cd "$directorio" || exit

# Bucle para procesar todos los archivos .txt (puedes cambiar la extensión si es necesario)
for archivo in *.json; do
    # Comprobamos si el archivo existe
    if [[ -f "$archivo" ]]; then
        # Eliminar las etiquetas <think> </think> usando sed
        sed -i 's/<think>.*<\/think>//g' "$archivo"
        echo "Etiquetas <think> eliminadas en $archivo"
    fi
done
