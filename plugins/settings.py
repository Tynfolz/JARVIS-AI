PHRASES = [
    "открой параметры", "настройки виндовс", "параметры"
]

def run(jarvis, text):
    jarvis.open.program("ms-settings:")  # Универсальная ссылка для Windows 10/11
    return True