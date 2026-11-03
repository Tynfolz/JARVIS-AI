from core.phrases import MODES, random_phrase
from voice.tts import speak

AI_ON = {
    "режим общения", "включи ии", "включи искусственный интеллект", "включи режим ии",
    "активируй ии", "активируй искусственный интеллект", "давай поговорим", "поговорим",
    "пообщаемся", "хочу поговорить", "общайся со мной", "перейди в режим общения",
    "запусти режим общения", "джарвис поговорим", "джарвис включи ии",
}

AI_OFF = {
    "режим команд", "выключи ии", "отключи ии", "выключи искусственный интеллект",
    "отключи искусственный интеллект", "перейди в режим команд", "только команды",
    "режим управления", "командный режим", "верни режим команд", "хватит общения",
    "закончить разговор", "прекрати разговор", "джарвис только команды",
}

SLEEP = {"свободен", "спи", "режим ожидания", "оставь"}


class ModeManager:

    def __init__(self):
        self.ai_mode = False

    def process(self, text):
        if text in AI_ON:
            self.ai_mode = True
            speak(random_phrase(MODES["ai_on"]))
            return True

        if text in AI_OFF:
            self.ai_mode = False
            speak(random_phrase(MODES["ai_off"]))
            return True

        if text in SLEEP:
            speak(random_phrase(MODES["sleep"]))
            return "sleep"

        return False

    def reset(self):
        pass

    def enable_ai(self):
        self.ai_mode = True

    def disable_ai(self):
        self.ai_mode = False