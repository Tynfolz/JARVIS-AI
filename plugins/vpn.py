PHRASES = [
    "включи впн", "открой впн", "хаппи впн", "впн"
]


def run(jarvis, text):
    # Try to find VPN in the app database first
    app = jarvis.apps.db.find("vpn")
    if app:
        name, path, app_type = app
        if app_type == "lnk":
            import os
            os.startfile(path)
        else:
            import subprocess
            subprocess.Popen(path)
        jarvis.say("Включаю VPN")
        return True

    # Try common VPN names
    for vpn_name in ["happy vpn", "happyvpn", "protonvpn", "nordvpn", "expressvpn", "surfshark", "windscribe", "tunnelbear", "hotspot shield", "openvpn", "wireguard"]:
        app = jarvis.apps.db.find(vpn_name)
        if app:
            name, path, app_type = app
            if app_type == "lnk":
                import os
                os.startfile(path)
            else:
                import subprocess
                subprocess.Popen(path)
            jarvis.say("Включаю VPN")
            return True

    jarvis.say("VPN не найден в базе. Скажите «обнови приложения»")
    return False