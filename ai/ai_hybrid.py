from llama_cpp import Llama
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "qwen",
    "Qwen2.5-3B-Instruct-Q4_K_M.gguf"
)


llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=1024,
    n_threads=max(2, os.cpu_count() // 2),
    verbose=False
)

def ask_ai(text: str, memory_context: str = ""):

    system_prompt = f"""
Ты JARVIS — персональный AI ассистент.

ВАЖНО:
- отвечай только на русском языке
- будь кратким
- не выдумывай факты
- называй пользователя "сэр"
- не повторяй вопрос пользователя
- не говори что ты языковая модель
- отвечай как голосовой помощник

ПАМЯТЬ:
{memory_context}
"""


    try:

        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ],

            temperature=0.7,
            max_tokens=300
        )


        return response["choices"][0]["message"]["content"].strip()


    except Exception as e:

        print("LLAMA ERROR:", e)

        return "Локальный ИИ недоступен."

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------