PHRASES = [
    "открой брав", "запусти брав", "брав"
]

# Путь к Brave Browser (измените на свой)
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

def run(jarvis, text):
    jarvis.open.program(BRAVE_PATH)
    return True