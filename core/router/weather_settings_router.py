from core import config
from voice.tts import speak


class WeatherSettingsRouter:


    def process(self, text):

        # -------------------------
        # CHANGE WEATHER CITY
        # -------------------------

        if (
            text.startswith("смени город на")
            or text.startswith("сменить город на")
        ):

            city = (
                text
                .replace("смени город на", "")
                .replace("сменить город на", "")
                .strip()
            )


            if city:

                city = city.capitalize()

                config.WEATHER_CITY = city

                self.save_config(
                    city
                )

                speak(
                    f"Город изменён на {city}"
                )


            else:

                speak(
                    "Не удалось определить город"
                )


            return True


        return False



    def save_config(self, city):

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
                r'WEATHER_CITY\s*=\s*".*?"',
                f'WEATHER_CITY = "{city}"',
                data
            )


            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(data)


            print(
                "💾 WEATHER CITY SAVED:",
                city
            )


        except Exception as e:

            print(
                "WEATHER CITY SAVE ERROR:",
                e
            )

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------