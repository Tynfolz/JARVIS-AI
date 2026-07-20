from llama_cpp import Llama


llm = Llama(
    model_path="models/qwen/qwen2.5-3b-instruct-q4_k_m.gguf",
    n_ctx=4096,
    n_threads=8,
    verbose=False
)


def ask_ai(text):

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content":
                """
                Ты голосовой асистент JARVIS.
                Отвечай только на русском.
                Будь кратким.
                Пользователя называй Сэр
                Не говори что ты языковая модель
                отвечай как голосовой помощник
                """
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )


    return response["choices"][0]["message"]["content"]