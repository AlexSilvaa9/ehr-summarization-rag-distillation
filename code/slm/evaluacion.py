import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score
import pandas as pd
import os

# Función para calcular las métricas BLEU, ROUGE y BERTScore
def calcular_metricas(salida_modelo, salida_esperada):
    # BLEU
    chencherry = SmoothingFunction()
    bleu = sentence_bleu(
        [salida_esperada.split()],
        salida_modelo.split(),
        smoothing_function=chencherry.method7
    )

    # ROUGE
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(salida_esperada, salida_modelo)

    # BERTScore
    P, R, F1 = score([salida_modelo], [salida_esperada], lang="es", verbose=False)

    return (
        bleu,
        scores['rouge1'].fmeasure,
        scores['rouge2'].fmeasure,
        scores['rougeL'].fmeasure,
        P.item(),
        R.item(),
        F1.item()
    )


# Cargar salidas de los modelos
carpeta_resultados = 'resultados/'
salidas_modelos = os.listdir(carpeta_resultados)

# Cargar salidas esperadas
carpeta_esperadas = "../../common_data/gold_standard_gpt4/"
salidas_esperadas = os.listdir(carpeta_esperadas)

# Parejas salida vs esperada
parejas = []
for salida in salidas_modelos:
    for esperada in salidas_esperadas:
        if salida.split("-")[1] == esperada.split("-")[0].replace("respuesta_", ""):
            parejas.append((salida, esperada))
            # los nombres de deepseek tienen un guion antes de lo esperado
        elif salida.split("-")[2] == esperada.split("-")[0].replace("respuesta_", ""):
                parejas.append((salida, esperada))

print(parejas)

# Calcular métricas
metricas = {}
for pareja in parejas:
    with open(os.path.join(carpeta_resultados, pareja[0]), 'r', encoding='utf-8') as f1:
        salida_modelo = f1.read()

    with open(os.path.join(carpeta_esperadas, pareja[1]), 'r', encoding='utf-8') as f2:
        salida_esperada = f2.read()

    metricas[pareja] = calcular_metricas(salida_modelo, salida_esperada)
    print(f'{pareja[0]} vs {pareja[1]}')

# Crear DataFrame con las métricas
df = pd.DataFrame(metricas).T
df.columns = ['BLEU', 'ROUGE1', 'ROUGE2', 'ROUGEL', 'BERT_P', 'BERT_R', 'BERT_F1']

# Guardar en CSV
df.to_csv('metricas.csv', header=True)
print(df)
