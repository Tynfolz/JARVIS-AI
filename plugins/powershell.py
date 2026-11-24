PHRASES = [
    "открой павершел", "павершел", "powershell"
]

def run(jarvis, text):
    jarvis.open.program("powershell", shell=True)  # shell=True для корректной работы
    return True