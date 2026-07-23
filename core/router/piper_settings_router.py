from core import config
from voice.tts import speak


class PiperSettingsRouter:


    def process(self, text):

        # -------------------------
        # CHANGE VOICE
        # -------------------------

        if (
            text.startswith("смени голос на")
            or text.startswith("сменить голос на")
        ):

            name = (
                text
                .replace("смени голос на", "")
                .replace("сменить голос на", "")
                .strip()
            )


            voices = {

                "дмитрий": "dmitri",
                "ирина": "irina",
                "руслан": "ruslan",

            }


            if name in voices:

                config.PIPER_VOICE = voices[name]

                self.save_config()

                speak(
                    f"Голос изменён на {name}"
                )

            else:

                speak(
                    "Такого голоса нет"
                )


            return True


        return False



    def save_config(self):

        """
        Сохраняем изменение прямо в config.py
        """

        path = r"D:\jarvis\core\config.py"


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                data = file.read()


            import re


            data = re.sub(
                r'PIPER_VOICE\s*=\s*".*?"',
                f'PIPER_VOICE = "{config.PIPER_VOICE}"',
                data
            )


            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(data)


            print(
                "💾 PIPER VOICE SAVED:",
                config.PIPER_VOICE
            )


        except Exception as e:

            print(
                "PIPER SAVE ERROR:",
                e
            )
            
# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------