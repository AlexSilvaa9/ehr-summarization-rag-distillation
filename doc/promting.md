# Técnicas Generales de Prompting

## 1. Prompting Basado en Templates Específicos

Este enfoque utiliza plantillas cuidadosamente diseñadas para guiar al modelo en la generación de resúmenes, como:

### Ejemplo para Resumen de Historial Médico

```plaintext
Paciente: [Nombre del Paciente]
Edad: [Edad]
Diagnósticos previos: [Lista de diagnósticos]
Medicamentos actuales: [Lista de medicamentos]
Procedimientos recientes: [Lista de procedimientos]
Resumen conciso: Proporciona un resumen en lenguaje claro y directo para el siguiente historial médico.

Historial: [Texto del historial médico]

Resumen:
```

Este enfoque proporciona estructura y asegura que el modelo cubra aspectos importantes.

## 2. Chain of Thought Prompting

Esta técnica es útil para tareas de razonamiento complejo.

### Ejemplo

```plaintext
Lee el historial médico siguiente y desglósalo en pasos clave para identificar:
1. Condiciones médicas actuales
2. Medicaciones y dosis relevantes
3. Procedimientos importantes
4. Síntomas actuales
5. Recomendaciones del médico

Historial: [Texto completo del historial]

Pasos:
1. [Extracción del paso 1]
2. [Extracción del paso 2]
...
Resumen final basado en estos puntos clave.
```

Este método mejora la precisión y reduce la alucinación, ya que divide el razonamiento en pasos lógicos.

## 3. Few-Shot Prompting

Proporciona ejemplos explícitos para guiar al modelo:

### Ejemplo

```plaintext
Ejemplo 1:
Historial: Paciente con hipertensión tratada con amlodipino 10 mg. Diagnóstico reciente de diabetes tipo 2.
Resumen: Paciente hipertenso bajo tratamiento con amlodipino, recientemente diagnosticado con diabetes tipo 2.

Ejemplo 2:
Historial: [Nuevo historial]
Resumen:
```

Este enfoque mejora las respuestas proporcionando un contexto basado en ejemplos.

## 4. Prompting Jerárquico

Este enfoque descompone la tarea en múltiples niveles, comenzando con la extracción de información clave antes de generar un resumen global.

### Ejemplo

```plaintext
Primero identifica los conceptos principales en el siguiente historial médico:
- Condiciones médicas
- Tratamientos actuales
- Síntomas reportados
- Recomendaciones del médico

Luego, combina esta información en un resumen de no más de 3 oraciones.

Historial: [Texto del historial]
```

Este método permite manejar documentos largos desglosando la información en componentes procesables.

## 5. Prompting Basado en Roles

Simula diferentes perspectivas, como la del médico o el paciente, para mejorar la precisión contextual.

### Ejemplo

```plaintext
Imagina que eres un médico de cabecera. Resume el siguiente historial médico para:
- Un médico especialista (uso técnico y detallado)
- Un paciente (lenguaje claro y sencillo)

Historial: [Texto del historial]
```

Este enfoque permite personalizar la respuesta según la audiencia.

---

### Consejos Adicionales para Prompting Efectivo (según OpenAI)

- Solicitar escritura de nivel experto.
- Proporcionar detalles claros.
- Adoptar perspectivas específicas (personalizar roles).
- Dividir tareas complejas en subtareas más simples (Split complex tasks into simpler subtasks).
- Proporcionar ejemplos claros.
- Especificar la longitud y el formato esperado de la respuesta.
- Combinar varias técnicas para obtener mejores resultados.

---

### Uso de Razonamiento Recursivo

Para resumir documentos largos como libros, se puede dividir en secciones:

1. Crear resúmenes para cada sección.
2. Combinar los resúmenes parciales en un resumen global.

Fuente: [OpenAI Documentation on Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)

---

Según  [Prompt Chaining or Stepwise Prompt? Refinement in Text Summarization 10.48550/arXiv.2406.00507](https://arxiv.org/abs/2406.00507) Chain of pronting funciona mejor que stepwise prompt, pero para batches es mas complejo implementarlo ya que tiene que ser un promt detras de otro

---

### Evaluación de Resúmenes con Modelos LLM

Para evaluar resúmenes con mayor precisión que métricas tradicionales como ROUGE o BLEU:

#### Prompt para Comparar Resúmenes (Referencia: DOI: [10.48550/arXiv.2403.02901](https://doi.org/10.48550/arXiv.2403.02901))

```plaintext
————–SYSTEM MESSAGE————-
You are a helpful assistant designed to output JSON.
In this task, you will be provided with a news article, a specific summary requirement, and two summaries. The summaries are crafted to meet a specific summary requirement. Note that there may be identical summaries.

Your task is to compare the overall quality of these two summaries concerning the summary requirement and pick the one that is better (there can be a tie).
First you will give an explanation of your decision then you will provide your decision in the format of 1 or 2 or tie.

Example Response:
{
"explanation": "Your explanation here",
"decision": "1 or 2 or tie"
}
```

Esta técnica ha demostrado ser más efectiva que ROUGE o BLEU según el artículo de referencia.

# Anotaciones generales

- En general casi todas las fuentes coinciden en que lo mejor es combinar varias tecnicas.
- No dejar nada en el aire y cuanto mas detalle mejor.
- No hay ningun prompt perfecto, hay que probar mucho. No todas las fuentes estan de acuerdo en las mejores practicas.
- Cuidado con los modelos grandes de razonamiento nuevos como el o1 porque funcionan al reves, hay que ser muy directo.
