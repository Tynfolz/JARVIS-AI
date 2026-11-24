PHRASES = [
    "открой доту", "запусти доту", "дота"
]

def run(jarvis, text):
    # Путь к Dota 2 через Steam
    jarvis.open.program("steam://run/570")  # 570 - AppID Dota 2
    return True