import time
from voice.tts import model, SPEAKER, SAMPLE_RATE

start = time.time()

audio = model.apply_tts(
    text="рад вас слышать сэр",
    speaker=SPEAKER,
    sample_rate=SAMPLE_RATE
)

print("TTS TIME:", time.time() - start)