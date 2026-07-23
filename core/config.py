MICROPHONE_NAME = "ME6S"

# -------------------------
# PIPER
# -------------------------
PIPER_VOICE = "ruslan"
PIPER_LENGTH_SCALE = 0.83      # скорость (меньше = быстрее)
PIPER_NOISE_SCALE = 0.50        # эмоциональность
PIPER_NOISE_W = 0.70            # четкость

# -------------------------
# WEATHER
# -------------------------
WEATHER_CITY = "Москва"

def set_config(name, value):

    path = __file__

    with open(path, "r", encoding="utf-8") as f:
        data = f.read()


    old = None

    if name == "WEATHER_CITY":

        old = WEATHER_CITY
        data = data.replace(
            f'WEATHER_CITY = "{old}"',
            f'WEATHER_CITY = "{value}"'
        )


    with open(path, "w", encoding="utf-8") as f:
        f.write(data)