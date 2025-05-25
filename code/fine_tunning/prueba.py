from unsloth import FastLanguageModel
from transformers import TextStreamer

max_seq_length = 2048
dtype = None
load_in_4bit = True

# Cargar el modelo ya entrenado con LoRA
model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "lora_model", # YOUR MODEL YOU USED FOR TRAINING
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )
FastLanguageModel.for_inference(model)  # Activa optimizaciones de inferencia

# Crear mensaje estilo chat
messages = [
    {"role": "user", "content": "Describe a tall tower in the capital of France."},
]

# Crear input_ids
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)

input_ids = inputs.to("cuda")

# Generar attention_mask manualmente
attention_mask = (input_ids != tokenizer.pad_token_id).long()

# Generar texto con atención explícita
text_streamer = TextStreamer(tokenizer, skip_prompt=True)

_ = model.generate(
    input_ids=input_ids,
    attention_mask=attention_mask,  # 👈 Evita el warning y errores
    streamer=text_streamer,
    max_new_tokens=128,
    use_cache=True,
    temperature=1.5,
    top_p=0.9  # puedes usar min_p si es parte de tu sampling strategy
)
