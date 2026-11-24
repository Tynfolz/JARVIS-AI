PHRASES = [
    "включи впн", "открой впн", "хаппи впн"
]

# Команда для запуска VPN (Happy VPN)
VPN_COMMAND = r"C:\path\to\happy-vpn.exe"

def run(jarvis, text):
    jarvis.open.program(VPN_COMMAND)
    return True