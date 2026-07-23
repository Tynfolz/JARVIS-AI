from voice.tts import speak
from core.phrases import MODES, random_phrase


class ModeManager:


    def __init__(self):

        self.listen_mode = "ACTIVE"

        self.ai_mode = False

        self.sleep_requested = False



    def process(self, text):


        # -------------------------
        # AI MODE ON
        # -------------------------

        ai_on_phrases = [

            "режим общения",
            "включи ии",
            "включи искусственный интеллект",
            "включи режим ии",
            "активируй ии",
            "активируй искусственный интеллект",
            "давай поговорим",
            "поговорим",
            "пообщаемся",
            "хочу поговорить",
            "общайся со мной",
            "перейди в режим общения",
            "запусти режим общения",
            "джарвис поговорим",
            "джарвис включи ии",

        ]


        if text in ai_on_phrases:

            self.ai_mode = True


            speak(
                random_phrase(
                    MODES["ai_on"]
                )
            )


            return True



        # -------------------------
        # AI MODE OFF
        # -------------------------

        ai_off_phrases = [

            "режим команд",
            "выключи ии",
            "отключи ии",
            "выключи искусственный интеллект",
            "отключи искусственный интеллект",
            "перейди в режим команд",
            "только команды",
            "режим управления",
            "командный режим",
            "верни режим команд",
            "хватит общения",
            "закончить разговор",
            "прекрати разговор",
            "джарвис только команды",

        ]


        if text in ai_off_phrases:


            self.ai_mode = False


            speak(
                random_phrase(
                    MODES["ai_off"]
                )
            )


            return True



        # -------------------------
        # SLEEP
        # -------------------------

        sleep_phrases = [

            "свободен",
            "спи",
            "режим ожидания",
            "оставь"

        ]


        if text in sleep_phrases:


            self.listen_mode = "SLEEP"

            self.sleep_requested = True


            speak(
                random_phrase(
                    MODES["sleep"]
                )
            )


            return "sleep"



        return False



    def reset(self):

        self.listen_mode = "ACTIVE"

        self.sleep_requested = False



    def enable_ai(self):

        self.ai_mode = True



    def disable_ai(self):

        self.ai_mode = False
        
# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------