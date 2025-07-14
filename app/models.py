import torch
from transformers import (
    Pipeline,
    pipeline
)
import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

system_prompt = """
You are a web scraping assistant. Your job is to extract and summarize content from web pages provided by the user.
Always respond in markdown format with clear and concise summaries.
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#--------------------- TEXT GENERATION ---------------------

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def load_text_model(model: str = "gemini-2.5-pro") -> Optional[genai.GenerativeModel]:
#     """Carga el modelo de Gemini"""
#     try:
#         return genai.GenerativeModel(model)
#     except Exception as e:
#         print(f"Error loading model: {str(e)}")
#         return None

# def generate_text(
#     prompt: str,
#     model: str = "gemini-2.5-pro",
#     temperature: float = 0.7
# ) -> str:
#     """
#     Procesa el texto usando el modelo cargado.
#     Combina el system_prompt con el prompt del usuario.
#     """
#     try:
#         # Cargar el modelo (solo se carga una vez)
#         model = load_text_model(model)
#         if model is None:
#             return "Error: Model could not be loaded."

#         # Crear el prompt completo
#         full_prompt = f"{system_prompt}\n\nUser request:\n{prompt}"

#         # Generar la respuesta
#         response = model.generate_content(
#             contents=full_prompt,
#             generation_config=genai.types.GenerationConfig(
#                 temperature=temperature,
#                 top_p=0.9,
#                 top_k=40
#             )
#         )

#         # Manejar la respuesta
#         if response.candidates and response.text:
#             return response.text
#         else:
#             return "Error: No valid response generated from the model."

#     except Exception as e:
#         return f"An error occurred while generating text: {str(e)}"

def load_text_model():
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.bfloat16,
        device=device,
    )
    return pipe


def generate_text(pipe: Pipeline, prompt: str, temperature: float = 0.7) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    predictions = pipe(
        prompt,
        temperature=temperature,
        max_new_tokens=256,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    )
    output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
    return output