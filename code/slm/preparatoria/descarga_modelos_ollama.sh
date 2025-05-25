#!/bin/bash

# Lista de modelos a descargar
models=(
    "deepseek-r1:8b"
    "llama3.1"
    "mistral"
    "deepseek-r1:14b"
    "qwen:14b"
    "phi4"
)

# Función para verificar si un modelo ya está descargado
is_model_downloaded() {
    local model_name=$(echo "$1" | sed 's|.*/||')
    ollama list | grep -q "^$model_name "
}

# Descargar modelos si no están ya descargados
for model in "${models[@]}"; do
    if is_model_downloaded "$model"; then
        echo "El modelo $model ya está descargado."
    else
        echo "Descargando el modelo $model..."
        ollama pull "$model"
    fi
done
