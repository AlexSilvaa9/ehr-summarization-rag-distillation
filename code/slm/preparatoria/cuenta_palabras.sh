#!/bin/bash

dir="../../../common_data/entradas"

if [ ! -d "$dir" ]; then
    echo "Error: La carpeta '$dir' no existe."
    exit 1
fi

total_palabras=0
max_palabras=0
num_archivos=0

for file in "$dir"/*; do
    if [ -f "$file" ]; then
        num_palabras=$(wc -w < "$file")
        echo "Archivo: $(basename "$file") - Palabras: $num_palabras"
        total_palabras=$((total_palabras + num_palabras))
        if (( num_palabras > max_palabras )); then
            max_palabras=$num_palabras
        fi
        ((num_archivos++))
    fi
done

if (( num_archivos > 0 )); then
    media=$((total_palabras / num_archivos))
    echo "\nNúmero de archivos: $num_archivos"
    echo "Promedio de palabras por archivo: $media"
    echo "Máximo de palabras en un archivo: $max_palabras"
else
    echo "No se encontraron archivos en '$dir'."
fi