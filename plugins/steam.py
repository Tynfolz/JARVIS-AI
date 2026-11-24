PHRASES = [
    "открой стим", "запусти стим", "стим"
]

def run(jarvis, text):
    jarvis.open.program("steam://open/client")
    return True