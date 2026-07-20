import os
import random
import re
import time
import threading
import traceback
import subprocess
from difflib import SequenceMatcher
from voice.voice_async import speak_async
from datetime import datetime
from core.phrases import COMMAND_DONE, random_phrase

def run_exe(path, args=None):

    try:

        if args is not None:

            subprocess.Popen(
                [path, str(args)],
                shell=True,
                creationflags=subprocess.DETACHED_PROCESS
            )

        else:

            subprocess.Popen(
                path,
                shell=True,
                creationflags=subprocess.DETACHED_PROCESS
            )

        return True

    except Exception as e:

        print("EXEC ERROR:", e)

        return False

class SkillEngine:

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def find_best_command(self, text):

        best_phrase = None
        best_score = 0

        for phrase in self.commands:

            score = self.similar(text, phrase)

            if score > best_score:
                best_score = score
                best_phrase = phrase

        print("BEST:", best_phrase, best_score)

        if best_score >= 0.65:
            return best_phrase

        return None

    def __init__(self):

        print("🔥 INIT START SkillEngine")

        self.volume_script = "ahk/set_sound.exe"
        self.commands = {}
        self.websites = {}
        self.success_phrases = ["Готово"]

        # -------------------------
        # ЧИСЛА СЛОВАМИ
        # -------------------------
        self.words_map = {
            "ноль": 0,
            "пять": 5,
            "десять": 10,
            "пятнадцать": 15,
            "двадцать": 20,
            "двадцать пять": 25,
            "тридцать": 30,
            "тридцать пять": 35,
            "сорок": 40,
            "сорок пять": 45,
            "пятьдесят": 50,
            "пятьдесят пять": 55,
            "шестьдесят": 60,
            "шестьдесят пять": 65,
            "семьдесят": 70,
            "семьдесят пять": 75,
            "восемьдесят": 80,
            "восемьдесят пять": 85,
            "девяносто": 90,
            "девяносто пять": 95,
            "сто": 100
        }

        try:

            self.initialized = True

            self.commands = {}

            print("🚀 SKILL ENGINE READY")

        except Exception as e:

            print("❌ INIT ERROR:")
            traceback.print_exc()

        # -------------------------
        # TIME SYSTEM
        # -------------------------
        self.timers = []
        self.stopwatch_start = None
        self.alarm_time = None
        self.awaiting_alarm_time = False

        self.reset()

    def reset(self):
        self.timers = []
        self.stopwatch_start = None
        self.alarm_time = None
        self.awaiting_alarm_time = False

        # -------------------------
        # AHK / EXE КОМАНДЫ
        # -------------------------
        self.commands = {
            "открой браузер": "ahk/Run browser.exe",
            "открой оперу": "ahk/Run browser.exe",
            "сверни браузер": "ahk/roll_browser.exe",
            "разверни браузер": "ahk/roll_browser.exe",
            "сверни оперу": "ahk/roll_browser.exe",
            "разверни оперу": "ahk/roll_browser.exe",
            "скопировать ссылку для хитмэн": "ahk/TG_link_hit.exe",
            "скопируй ссылку для хитмэн": "ahk/TG_link_hit.exe",
            "скопируй ссылку для хит": "ahk/TG_link_hit.exe",
            "скопировать ссылку для хит": "ahk/TG_link_hit.exe",
            "скопируй ссылку для патриот": "ahk/TG_link_patriot.exe",
            "скопировать ссылку для патриот": "ahk/TG_link_patriot.exe",
            "останови музыку": "ahk/Start music.exe",
            "установи музыку": "ahk/Start music.exe",
            "включи музыку": "ahk/Start music.exe",
            "музыка стоп": "ahk/Start music.exe",
            "стоп музыка": "ahk/Start music.exe",
            "музыку включи": "ahk/Start music.exe",
            "следующий трек": "ahk/next track.exe",
            "дальше": "ahk/next track.exe",
            "перелестни": "ahk/next track.exe",
            "пролестни": "ahk/next track.exe",
            "прошлый трек": "ahk/last track.exe",
            "прошлый трек включи": "ahk/last track.exe",
            "назад перелестни": "ahk/last track.exe",
            "назад пролестни": "ahk/last track.exe",
            "назад паралель с не": "ahk/last track.exe",
            "назад ": "ahk/last track.exe",
            "скопируй скрипт для дискорда": "ahk/diskord_skript.exe",
            "скопировать скрипт для дискорда": "ahk/diskord_skript.exe",
            "скопируй скрипт для ди дисковод": "ahk/diskord_skript.exe",
            "скопировать скрипт для ди дисковож": "ahk/diskord_skript.exe",
            "скрипт для ди дисковод скопуруй": "ahk/diskord_skript.exe",
            "скопировать скрипт для дискорда": "ahk/diskord_skript.exe",
            "скопируй скрипт для дисковод": "ahk/diskord_skript.exe",
            "скопировать скрипт для дисковод": "ahk/diskord_skript.exe",
            "скрипт для дисковод скопируй": "ahk/diskord_skript.exe",
            "скопируй скрипта для скот": "ahk/diskord_skript.exe",
            "скопировать скрипта для диску отдав": "ahk/diskord_skript.exe",
            "открой сейф": "ahk/ASF.exe",
            "сейф открой": "ahk/ASF.exe",
            "открой майнкрафт": "ahk/astralritch.exe",
            "майнкрафт открой": "ahk/astralritch.exe",
            "открой де про галактик ": "ahk/deep_rock_galactic.exe",
            "ди пророк галактик открой": "ahk/deep_rock_galactic.exe",
            "открой гномов": "ahk/deep_rock_galactic.exe",
            "гномов открой": "ahk/deep_rock_galactic.exe",
            "доту открой": "ahk/dota.exe",
            "открой доту": "ahk/dota.exe",
            "открой гигабайт": "ahk/gigabate_сontrol_сenter.exe",
            "гигибайт открой": "ahk/gigabate_сontrol_сenter.exe",
            "открой лдпр плееров": "ahk/ld_player_9.exe",
            "лдпр плеер открой": "ahk/ld_player_9.exe",
            "открой л до плеер": "ahk/ld_player_9.exe",
            "открой фотошоп": "ahk/photoshop.exe",
            "фотошоп открой": "ahk/photoshop.exe",
            "перезапустить и скотт": "ahk/restart_discord.exe",
            "перезапустить дисконтных": "ahk/restart_discord.exe",
            "перезапустить скорбно": "ahk/restart_discord.exe",
            "перезапустить эскорт": "ahk/restart_discord.exe",
            "перезапустить дисковода": "ahk/restart_discord.exe",
            "перезапустить города": "ahk/restart_discord.exe",
            "перезапустить города": "ahk/restart_discord.exe",
            "ди скотт при запусти": "ahk/restart_discord.exe",
            "где скотт при запусти": "ahk/restart_discord.exe",
            "при запустить эскорт": "ahk/restart_discord.exe",
            "перезапустить дисковод": "ahk/restart_discord.exe",
            "перезапустить скорби": "ahk/restart_discord.exe",
            "перезапустить скотт": "ahk/restart_discord.exe",
            "перезапустить из кодов": "ahk/restart_discord.exe",
            "открой то дата": "ahk/tdata_tg.exe",
            "когда-то открой": "ahk/tdata_tg.exe",
            "те дата открой": "ahk/tdata_tg.exe",
            "открой дата": "ahk/tdata_tg",
            "открой мои туда-то": "ahk/tdata_my.exe",
            "мои то дата открой": "ahk/tdata_my.exe",
            "открой мои тогда-то": "ahk/tdata_my.exe",
            "открой монтаж": "ahk/video_editor_plus.exe",
            "монтаж открой": "ahk/video_editor_plus.exe",
            "запрет открой": "ahk/zapret.exe",
            "открой запрет": "ahk/zapret.exe",
            "открой параметры": "ahk/settings.exe",
            "параметры открой": "ahk/settings.exe",
            "открой настройки": "ahk/settings.exe",
            "настройки открой": "ahk/settings.exe",
            "заблокируй компьютер": "ahk/blocking.exe",
            "компьютер заблокируй": "ahk/blocking.exe",
            "открой блокнот": "ahk/notepads.exe",
            "блокнот открой": "ahk/notepads.exe",
            "очисти корзину": "ahk/Empty trash.exe",
            "корзину очисти": "ahk/Empty trash.exe",
            "корзину открой": "ahk/open_trash.exe",
            "открой корзину": "ahk/open_trash.exe",
            "открой корзину": "ahk/open_trash.exe",
            "сверни все окна": "ahk/Roll up windows.exe",
            "сверни окна": "ahk/Roll up windows.exe",
            "все окна сверни": "ahk/Roll up windows.exe",
            "окна сверни": "ahk/Roll up windows.exe",
            "иди поспи": "ahk/sleep.exe",
            "спать иди": "ahk/sleep.exe",
            "разве они все окнам": "ahk/UNRoll up windows.exe",
            "разверни все окнам": "ahk/UNRoll up windows.exe",
            "развени они все окна": "ahk/UNRoll up windows.exe",
            "разве они все окна": "ahk/UNRoll up windows.exe",

        }

        print("🚀 SKILL ENGINE READY")


    # -------------------------
        # ГРОМКОСТЬ AHK
        # -------------------------
        self.volume_script = "ahk/set_sound.exe"

        # -------------------------
        # САЙТЫ
        # -------------------------
        self.websites = {
            "открой ютуб": "https://youtube.com",
            "ютуб открой": "https://youtube.com",
            "открой гугл": "https://google.com",
            "открой чанга по": "https://chatgpt.com",
            "открой чат же пяти": "https://chatgpt.com",
            "открой чат кгб": "https://chatgpt.com",
            "чат же пяти открой": "https://chatgpt.com",
            "открой твич": "https://twitch.tv",
            "открой вич": "https://twitch.tv",
            "вич открой": "https://twitch.tv",
            "твие открой": "https://twitch.tv",
            "открой твие": "https://twitch.tv",
            "открой переводчику": "https://translate.yandex.ru",
            "открой переводчик": "https://translate.yandex.ru",
            "переводчик открой": "https://translate.yandex.ru",
            "открой дип сик": "https://chat.deepseek.com",
            "дип сик открой": "https://chat.deepseek.com",
            "ди сик открой": "https://chat.deepseek.com",
            "дикси к открой": "https://chat.deepseek.com",
            "открой дневник": "https://dnevnik.ru/r/saratov/marks",
            "открой дневник ру": "https://dnevnik.ru/r/saratov/marks",
            "дневник открой": "https://dnevnik.ru/r/saratov/marks",
            "дневник ру открой": "https://dnevnik.ru/r/saratov/marks",
            "открой озон": "https://www.ozon.ru",
            "открой озона": "https://www.ozon.ru",
            "озон открой": "https://www.ozon.ru",
            "озона открой": "https://www.ozon.ru",
            "открой года знаю": "https://gdz.ru",
            "открой года за": "https://gdz.ru",
            "открой года": "https://gdz.ru",
            "открой гдз": "https://gdz.ru",
            "года за открой": "https://gdz.ru",
            "открой гдз русскому": "https://reshutka.ru/8klass/russkiy/barhudarov/",
            "открой года за по русскому": "https://reshutka.ru/8klass/russkiy/barhudarov/",
            "года за по узкому открой": "https://reshutka.ru/8klass/russkiy/barhudarov/",
            "года за по русскому открой": "https://reshutka.ru/8klass/russkiy/barhudarov/",
            "открой почту": "https://mail.yandex.ru",
            "почту открой": "https://mail.yandex.ru",
            "открой макс": "https://web.max.ru",
            "макс открой": "https://web.max.ru",
            "открой расписание": "https://солярис64.рф/расписание/",
            "расписание открой": "https://солярис64.рф/расписание/",
            "открой фан по эй": "https://funpay.com",
            "открой айфон по и": "https://funpay.com",
            "открой айфон по и": "https://funpay.com",
            "фан открой": "https://funpay.com",
            "открой авито": "https://www.avito.ru",
            "открой вита": "https://www.avito.ru",
            "авито открой": "https://www.avito.ru",
            "вито открой": "https://www.avito.ru",
            "открой карты": "https://yandex.ru/maps",
            "карты открой": "https://yandex.ru/maps",
            "яндекскарты открой": "https://yandex.ru/maps",
            "открой яндекскарты": "https://yandex.ru/maps",
            "открой грок": "https://grok.com",
            "открой игрок": "https://grok.com",
            "грок открой": "https://grok.com",
            "грог открой": "https://grok.com",
            "днс открой": "https://www.dns-shop.ru",
            "открой донец": "https://www.dns-shop.ru",
            "донец открой": "https://www.dns-shop.ru",
            "открой до нас": "https://www.dns-shop.ru",
            "открой днс": "https://www.dns-shop.ru",
            "открой донёс": "https://www.dns-shop.ru",
            "дота маркет открой": "https://market.dota2.net",
            "открой дота маркет": "https://market.dota2.net",
            "маркет дота открой": "https://market.dota2.net",
            "открой а затем": "https://lzt.market",
            "открой л затем": "https://lzt.market",
            "зато открой": "https://lzt.market",
            "коллектор шопа открой": "https://collector.shop",
            "открой коллектора шоб": "https://collector.shop",
            "открой коллектора шоп": "https://collector.shop",
            "открой конвертер валют": "https://yandex.ru/search/?text=конвертер+валют+из+гривен+в+рубли&lr=194&clid=11528081&src=suggest_Pers",
            "конвертор валют открой": "https://yandex.ru/search/?text=конвертер+валют+из+гривен+в+рубли&lr=194&clid=11528081&src=suggest_Pers",
            "пополни стим": "https://store.steampowered.com",
            "пополни с тим": "https://store.steampowered.com",
            "пополни стин": "https://store.steampowered.com",
            "стим пополни": "https://store.steampowered.com",
            "стин пополни": "https://store.steampowered.com",
            "открой гугл диск": "https://drive.google.com/drive/home",
            "открой гугл диска": "https://drive.google.com/drive/home",
            "гугл диск открой": "https://drive.google.com/drive/home",
            "гугл диска открой": "https://drive.google.com/drive/home",
            "открой ситилинк": "https://www.citilink.ru",
            "ситилинк открой": "https://www.citilink.ru",
            "открой труд всем": "https://trudvsem.ru/auth/candidate/",
            "труд всем открой": "https://trudvsem.ru/auth/candidate/",
            "открой работа россию": "https://trudvsem.ru/auth/candidate/",
            "открой работа россии": "https://trudvsem.ru/auth/candidate/",
            "открой работы россии": "https://trudvsem.ru/auth/candidate/",
            "работа россию открой": "https://trudvsem.ru/auth/candidate/",
            "работа россии открой": "https://trudvsem.ru/auth/candidate/",
            "работы россия открой": "https://trudvsem.ru/auth/candidate/",
            "открой работу россии": "https://trudvsem.ru/auth/candidate/",
            "открой работы россии": "https://trudvsem.ru/auth/candidate/",
            "открой вы к": "https://vk.com",
            "вы к открой": "https://vk.com",
            "открой века": "https://vk.com",
            "века открой": "https://vk.com",
            "с генерируют пароль": "https://randomus.ru/password",
            "сгенерируй пароль": "https://randomus.ru/password",
            "сгенерировать пароль": "https://randomus.ru/password",
            "пароль с генерирует": "https://randomus.ru/password",
            "реп фор реп открой": "https://rep4rep.com/commentlist/1/0/subscribed",
            "открой реп фо реп": "https://rep4rep.com/commentlist/1/0/subscribed",
            "рэп рэп открой": "https://rep4rep.com/commentlist/1/0/subscribed",
        }

        # -------------------------
        # ЧИСЛА СЛОВАМИ
        # -------------------------
        self.words_map = {
            "ноль": 0,
            "пять": 5,
            "десять": 10,
            "пятнадцать": 15,
            "двадцать": 20,
            "двадцать пять": 25,
            "тридцать": 30,
            "тридцать пять": 35,
            "сорок": 40,
            "сорок пять": 45,
            "пятьдесят": 50,
            "пятьдесят пять": 55,
            "шестьдесят": 60,
            "шестьдесят пять": 65,
            "семьдесят": 70,
            "семьдесят пять": 75,
            "восемьдесят": 80,
            "восемьдесят пять": 85,
            "девяносто": 90,
            "девяносто пять": 95,
            "сто": 100
        }

    # -------------------------
    # ТАЙМЕР
    # -------------------------
    def _start_timer(self, seconds):

        def run():
            speak_async(f"Таймер запущен на {seconds} секунд")

            time.sleep(seconds)

            speak_async("Время вышло")

        threading.Thread(target=run, daemon=True).start()

    def _parse_time_to_seconds(self, text):

        text = text.lower()

        numbers = {
            "ноль": 0,
            "один": 1,
            "одна": 1,
            "два": 2,
            "две": 2,
            "три": 3,
            "четыре": 4,
            "пять": 5,
            "шесть": 6,
            "семь": 7,
            "восемь": 8,
            "девять": 9,
            "десять": 10,
            "одиннадцать": 11,
            "двенадцать": 12,
            "тринадцать": 13,
            "четырнадцать": 14,
            "пятнадцать": 15,
            "шестнадцать": 16,
            "семнадцать": 17,
            "восемнадцать": 18,
            "девятнадцать": 19,
            "двадцать": 20,
            "тридцать": 30,
            "сорок": 40,
            "пятьдесят": 50
        }

        words = text.split()

        value = None
        unit = None

        # собираем число
        for w in words:
            if w in numbers:
                value = numbers[w]

            if w.startswith("мин"):
                unit = "min"
            elif w.startswith("сек"):
                unit = "sec"
            elif w.startswith("час"):
                unit = "hour"

        if value is None:
            match = re.search(r"\d+", text)
            if match:
                value = int(match.group())

        if value is None or unit is None:
            return 0

        if unit == "min":
            return value * 60
        if unit == "hour":
            return value * 3600
        if unit == "sec":
            return value

        return 0

    def _start_stopwatch(self):

        self.stopwatch_start = time.time()
        speak_async("Секундомер запущен")

    def _stop_stopwatch(self):

        if not self.stopwatch_start:
            speak_async("Секундомер не запущен")
            return

        elapsed = int(time.time() - self.stopwatch_start)
        self.stopwatch_start = None

        speak_async(f"Прошло {elapsed} секунд")

    def _set_alarm(self, hour, minute):

        def run():
            speak_async(f"Будильник установлен на {hour:02d}:{minute:02d}")

            while True:
                now = datetime.now()

                if now.hour == hour and now.minute == minute:
                    speak_async("⏰ Будильник сработал")
                    break

                time.sleep(5)

        threading.Thread(target=run, daemon=True).start()

        speak_async(f"Будильник установлен на {hour}:{minute}")

    def _words_to_time(self, text):

        numbers = {
            "ноль": 0,
            "один": 1,
            "одна": 1,
            "два": 2,
            "две": 2,
            "три": 3,
            "четыре": 4,
            "пять": 5,
            "шесть": 6,
            "семь": 7,
            "восемь": 8,
            "девять": 9,
            "десять": 10,
            "одиннадцать": 11,
            "двенадцать": 12,
            "тринадцать": 13,
            "четырнадцать": 14,
            "пятнадцать": 15,
            "шестнадцать": 16,
            "семнадцать": 17,
            "восемнадцать": 18,
            "девятнадцать": 19,
            "двадцать": 20,
            "тридцать": 30,
            "сорок": 40,
            "пятьдесят": 50
        }

        words = text.split()

        nums = []
        i = 0

        while i < len(words):

            w = words[i]

            # прямое число
            if w in numbers:

                # проверяем связку "двадцать три"
                if i + 1 < len(words) and words[i + 1] in numbers:

                    a = numbers[w]
                    b = numbers[words[i + 1]]

                    # только для десятков
                    if a in [20, 30, 40, 50]:
                        nums.append(a + b)
                        i += 2
                        continue

                nums.append(numbers[w])

            i += 1

        if len(nums) >= 2:
            return nums[0], nums[1]

        return None

    # -------------------------
    # ВРЕМЯ (ИСПРАВЛЕНО)
    # -------------------------
    def _handle_time(self, text):

        time_phrases = [
            "сколько времени",
            "который час",
            "сколько время",
            "время скажи",
            "сколько сейчас времени",
            "сколько сейчас временя"
        ]

        if any(p in text for p in time_phrases):

            now = datetime.now()
            h = now.hour
            m = now.minute

            # красиво: 09:05 вместо 9 5
            speak_async(f"Сейчас {h:02d}:{m:02d}")
            return True

        return False


    # -------------------------
    # ГРОМКОСТЬ (ИСПРАВЛЕНО)
    # -------------------------
    def _extract_volume(self, text):

        text = text.lower()

        # 1) цифры
        match = re.search(r"\d+", text)
        if match:
            return max(0, min(100, int(match.group())))

        # 2) числа словами (ИСПРАВЛЕНО: точное совпадение фраз)
        for word, num in sorted(self.words_map.items(), key=lambda x: -len(x[0])):
            if word in text:
                return num

        return None

    # -------------------------
    # WEBSITE
    # -------------------------
    def open_site(self, url):

        try:

            import webbrowser

            webbrowser.open(url)

            print("🌐 OPEN WEBSITE:", url)

            return True

        except Exception as e:

            print("WEB ERROR:", e)

            return False


# -------------------------
    # MAIN
    # -------------------------
    def process(self, text):

        print("PROCESS START:", text)

        if not text:
            return False

        text = text.lower().strip()

        # -------------------------
        # 0. AHK КОМАНДЫ (ПРИОРИТЕТ)
        # -------------------------
        # -------------------------
        # 2. КОМАНДЫ
        # -------------------------
        matched = self.find_best_command(text)

        print("MATCHED =", matched)

        if matched:

            file_path = self.commands[matched]

            print("FUZZY MATCH:", matched)

            if not os.path.exists(file_path):
                print("❌ FILE NOT FOUND:", file_path)

                threading.Thread(
                    target=speak_async,
                    args=("Файл не найден",),
                    daemon=True
                ).start()

                return True

            try:

                os.system(f'start "" "{file_path}"')

                print("🚀 RUN:", file_path)

                threading.Thread(
                    target=speak_async,
                    args=(random_phrase(COMMAND_DONE),),
                    daemon=True
                ).start()

                return True

            except Exception as e:

                print("AHK ERROR:", e)

                threading.Thread(
                    target=speak_async,
                    args=("Ошибка запуска",),
                    daemon=True
                ).start()

                return True

        # -------------------------
        # WAITING FOR ALARM TIME
        # -------------------------
        if self.awaiting_alarm_time:

            match = re.search(r"(\d{1,2})\D+(\d{2})", text)

            if match:
                hour = int(match.group(1))
                minute = int(match.group(2))
            else:
                result = self._words_to_time(text)

                if result is None:
                    speak_async("Не понял время")
                    return True

                hour, minute = result

            # ДОП ЗАЩИТА (ВАЖНО)
            if hour is None or minute is None:
                speak_async("Не понял время")
                return True

            self._set_alarm(hour, minute)
            self.awaiting_alarm_time = False
            return True

        # -------------------------
        # ВРЕМЯ (ПЕРВЫЙ ПРИОРИТЕТ)
        # -------------------------
        if self._handle_time(text):
            return True
        # -------------------------
        # TIMER / STOPWATCH / ALARM
        # -------------------------

        # ⏱ таймер
        if "таймер" in text:
            seconds = self._parse_time_to_seconds(text)

            if seconds == 0:
                speak_async("Не понял время таймера")
                return True

            self._start_timer(seconds)
            return True

        # ⏳ секундомер
        if "секундомер" in text:
            if "стоп" in text:
                self._stop_stopwatch()
            else:
                self._start_stopwatch()
            return True

        # ⏰ будильник
        if "будильник" in text:
            speak_async("Укажите время")
            self.awaiting_alarm_time = True
            return True
    # -------------------------
        # 1. ГРОМКОСТЬ
        # -------------------------
        volume_triggers = [
            "громкость ",
            "громкость на",
            "поставь громоксть",
            "громкость поставь",
        ]

        if any(t in text for t in volume_triggers):

            value = self._extract_volume(text)

            if value is None:
                speak_async("Не понял уровень громкости")
                return True

            try:

                cmd = f'"{self.volume_script}" {value}'
                subprocess.Popen(cmd, shell=True)

                print(f"🔊 VOLUME SET: {value}")

                threading.Thread(
                    target=speak_async,
                    args=(random_phrase(COMMAND_DONE),),
                    daemon=True
                ).start()

            except Exception as e:

                print("VOLUME ERROR:", e)
                speak_async("Ошибка громкости")

            return True

        # -------------------------
        # 3. САЙТЫ
        # -------------------------
        for phrase, url in self.websites.items():

            if phrase in text:

                print("🌐 OPEN WEBSITE:", url)

                if self.open_site(url):
                    threading.Thread(
                        target=speak_async,
                        args=(random_phrase(COMMAND_DONE),),
                        daemon=True
                    ).start()
                    
                else:
                    speak_async("Ошибка открытия сайта")

                return True

        return False

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------