# plugins/spotify.py

import re
import time
import ctypes
import psutil
import keyboard
import win32api
import win32gui
import win32process
import win32con

from ctypes import POINTER, cast
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

from voice.tts import speak
from core.phrases import COMMAND_DONE, random_phrase


# ============================================================
# REQUIREMENTS
# ============================================================

REQUIREMENTS = [
    "psutil",
    "pywin32",
    "keyboard",
    "pycaw",
    "comtypes",
]


# ============================================================
# PHRASES
# ============================================================

PHRASES = [

    # OPEN / RESTORE
    "открой спотифай",
    "открой spotify",
    "открывай спотифай",
    "открывай spotify",
    "запусти спотифай",
    "запусти spotify",
    "запускай спотифай",
    "запускай spotify",
    "включи спотифай",
    "включи spotify",
    "открой музыку",
    "запусти музыку",
    "включи музыку",
    "поставь музыку",
    "давай музыку",
    "хочу музыку",
    "включи песни",
    "запусти песни",

    "разверни спотифай",
    "разверни spotify",
    "развернуть спотифай",
    "развернуть spotify",
    "покажи спотифай",
    "покажи spotify",
    "покажи окно спотифай",
    "покажи окно spotify",
    "верни спотифай",
    "верни spotify",
    "открой окно спотифай",
    "открой окно spotify",
    "выведи спотифай",
    "выведи spotify",
    "разверни музыку",
    "покажи музыку",

    # MINIMIZE
    "сверни спотифай",
    "сверни spotify",
    "свернуть спотифай",
    "свернуть spotify",
    "убери спотифай",
    "убери spotify",
    "скрой спотифай",
    "скрой spotify",
    "спрячь спотифай",
    "спрячь spotify",
    "сверни окно спотифай",
    "сверни окно spotify",
    "сверни музыку",

    # PLAY / PAUSE
    "пауза",
    "поставь паузу",
    "поставь музыку на паузу",
    "останови музыку",
    "останови трек",
    "останови песню",
    "продолжи",
    "продолжи музыку",
    "продолжи трек",
    "продолжи песню",
    "возобнови",
    "возобнови музыку",
    "возобнови трек",
    "возобнови песню",
    "сними с паузы",
    "сними музыку с паузы",
    "играй",
    "включи воспроизведение",

    # NEXT
    "следующий",
    "следующий трек",
    "следующая песня",
    "дальше",
    "дальше трек",
    "дальше песню",
    "следующий трек пожалуйста",
    "переключи трек",
    "переключи песню",
    "пропусти",
    "пропусти трек",
    "пропусти песню",
    "скип",
    "скипни",
    "скипни трек",

    # PREVIOUS
    "предыдущий",
    "предыдущий трек",
    "предыдущая песня",
    "прошлый",
    "прошлый трек",
    "прошлая песня",
    "назад",
    "верни назад",
    "верни предыдущий",
    "предыдущий трек пожалуйста",

    "подбери музыку",
    "подбери песни",
    "подбери треки",
    "включи подборку",
    "музыкальный подбор",
    "включи диджея",
    "запусти диджея",
    "режим диджея",
    "включи режим диджея",
    "запусти режим диджея",
    "диджей",

    # VOLUME UP
    "громче",
    "сделай громче",
    "прибавь",
    "прибавь громкость",
    "увеличь",
    "увеличь громкость",
    "сделай музыку громче",
    "сделай спотифай громче",
    "прибавь звук",
    "увеличь звук",

    # VOLUME DOWN
    "тише",
    "сделай тише",
    "убавь",
    "убавь громкость",
    "уменьши",
    "уменьши громкость",
    "сделай музыку тише",
    "сделай спотифай тише",
    "убавь звук",
    "уменьши звук",

    # EXACT VOLUME
    "громкость",
    "громкость 0",
    "громкость 5",
    "громкость 10",
    "громкость 15",
    "громкость 20",
    "громкость 25",
    "громкость 30",
    "громкость 35",
    "громкость 40",
    "громкость 45",
    "громкость 50",
    "громкость 55",
    "громкость 60",
    "громкость 65",
    "громкость 70",
    "громкость 75",
    "громкость 80",
    "громкость 85",
    "громкость 90",
    "громкость 95",
    "громкость 100",

    "поставь громкость",
    "установи громкость",
    "сделай громкость",

    "громкость на 5",
    "громкость на 10",
    "громкость на 15",
    "громкость на 20",
    "громкость на 25",
    "громкость на 30",
    "громкость на 35",
    "громкость на 40",
    "громкость на 45",
    "громкость на 50",
    "громкость на 55",
    "громкость на 60",
    "громкость на 65",
    "громкость на 70",
    "громкость на 75",
    "громкость на 80",
    "громкость на 85",
    "громкость на 90",
    "громкость на 95",
    "громкость на 100",

    "поставь громкость 5",
    "поставь громкость 10",
    "поставь громкость 15",
    "поставь громкость 20",
    "поставь громкость 25",
    "поставь громкость 30",
    "поставь громкость 35",
    "поставь громкость 40",
    "поставь громкость 45",
    "поставь громкость 50",
    "поставь громкость 55",
    "поставь громкость 60",
    "поставь громкость 65",
    "поставь громкость 70",
    "поставь громкость 75",
    "поставь громкость 80",
    "поставь громкость 85",
    "поставь громкость 90",
    "поставь громкость 95",
    "поставь громкость 100",

    "поставь музыку на 10",
    "поставь музыку на 20",
    "поставь музыку на 25",
    "поставь музыку на 30",
    "поставь музыку на 40",
    "поставь музыку на 50",
    "поставь музыку на 60",
    "поставь музыку на 70",
    "поставь музыку на 80",
    "поставь музыку на 90",
    "поставь музыку на 100",

    # NUMBER WORDS
    "громкость ноль",
    "громкость десять",
    "громкость пятнадцать",
    "громкость двадцать",
    "громкость двадцать пять",
    "громкость тридцать",
    "громкость тридцать пять",
    "громкость сорок",
    "громкость сорок пять",
    "громкость пятьдесят",
    "громкость пятьдесят пять",
    "громкость шестьдесят",
    "громкость шестьдесят пять",
    "громкость семьдесят",
    "громкость семьдесят пять",
    "громкость восемьдесят",
    "громкость восемьдесят пять",
    "громкость девяносто",
    "громкость девяносто пять",
    "громкость сто",

    "поставь громкость десять",
    "поставь громкость пятнадцать",
    "поставь громкость двадцать",
    "поставь громкость двадцать пять",
    "поставь громкость тридцать",
    "поставь громкость тридцать пять",
    "поставь громкость сорок",
    "поставь громкость сорок пять",
    "поставь громкость пятьдесят",
    "поставь громкость пятьдесят пять",
    "поставь громкость шестьдесят",
    "поставь громкость шестьдесят пять",
    "поставь громкость семьдесят",
    "поставь громкость семьдесят пять",
    "поставь громкость восемьдесят",
    "поставь громкость восемьдесят пять",
    "поставь громкость девяносто",
    "поставь громкость девяносто пять",
    "поставь громкость сто",

    "громкость на двадцать пять",
    "громкость на тридцать пять",
    "громкость на сорок пять",
    "громкость на пятьдесят пять",
    "громкость на шестьдесят пять",
    "громкость на семьдесят пять",
    "громкость на восемьдесят пять",
    "громкость на девяносто пять",
]


# ============================================================
# DONE
# ============================================================

def done():
    try:
        speak(random_phrase(COMMAND_DONE))
    except Exception:
        try:
            speak("Готово")
        except Exception:
            pass


# ============================================================
# SPOTIFY INDICATORS
# ============================================================

def is_spotify_context(text: str) -> bool:
    indicators = [
        "споти", "spotify", "спот",
        "музык", "песн", "трек", "композиц",
        "фай",
        "спаде", "спать", "пойти",
    ]
    return any(ind in text for ind in indicators)


# ============================================================
# SPOTIFY PIDS
# ============================================================

def get_spotify_pids():
    pids = set()
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = (proc.info["name"] or "").lower()
            if "spotify" in name:
                pids.add(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return pids


# ============================================================
# FIND SPOTIFY WINDOW
# ============================================================

def find_spotify_window():
    pids = get_spotify_pids()
    print("SPOTIFY PIDS:", pids)

    if not pids:
        print("SPOTIFY WINDOW: None")
        return None

    candidates = []

    def callback(hwnd, _):
        if not win32gui.IsWindow(hwnd):
            return

        visible = win32gui.IsWindowVisible(hwnd) or win32gui.IsIconic(hwnd)
        if not visible:
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
        except Exception:
            return

        if pid not in pids:
            return

        title = win32gui.GetWindowText(hwnd) or ""
        try:
            rect = win32gui.GetWindowRect(hwnd)
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
        except Exception:
            w, h = 0, 0

        if w < 80 or h < 80:
            return

        score = 0
        title_l = title.lower()
        if "spotify" in title_l:
            score += 20
        if w > 400 and h > 300:
            score += 10
        if win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0:
            score += 5
        if win32gui.IsIconic(hwnd):
            score += 1

        candidates.append((score, hwnd, title, pid, w, h))

    try:
        win32gui.EnumWindows(callback, None)
    except Exception as e:
        print("SPOTIFY WINDOW ERROR:", e)
        return None

    if not candidates:
        print("SPOTIFY WINDOW: None (no visible windows)")
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    best = candidates[0]
    hwnd = best[1]
    print("SPOTIFY WINDOW:", hwnd)
    print("WINDOW TITLE:", best[2])
    print("WINDOW PID:", best[3])
    print("WINDOW SIZE:", best[4], "x", best[5])
    return hwnd


# ============================================================
# SHOW OR OPEN
# ============================================================

def show_or_open_spotify(jarvis):
    hwnd = find_spotify_window()

    if hwnd:
        try:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            else:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.BringWindowToTop(hwnd)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass
            print("SPOTIFY SHOWN:", hwnd)
            return True
        except Exception as e:
            print("SPOTIFY SHOW ERROR:", e)

    try:
        if hasattr(jarvis, "apps") and jarvis.apps.open("Spotify"):
            print("SPOTIFY OPENED VIA APPS API")
            return True
    except Exception as e:
        print("SPOTIFY APPS OPEN ERROR:", e)

    try:
        import os
        import subprocess
        paths = [
            os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe"),
        ]
        for p in paths:
            if os.path.isfile(p):
                subprocess.Popen([p])
                time.sleep(2.0)
                hwnd = find_spotify_window()
                if hwnd:
                    try:
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(hwnd)
                    except Exception:
                        pass
                print("SPOTIFY LAUNCHED FROM:", p)
                return True
        os.startfile("spotify:")
        print("SPOTIFY LAUNCHED VIA PROTOCOL")
        return True
    except Exception as e:
        print("SPOTIFY FALLBACK OPEN ERROR:", e)

    speak("Spotify не найден")
    return False


# ============================================================
# MINIMIZE
# ============================================================

def minimize_spotify():
    hwnd = find_spotify_window()

    if not hwnd:
        speak("Spotify не запущен")
        return False

    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        print("SPOTIFY MINIMIZED:", hwnd)
        return True
    except Exception as e:
        print("SPOTIFY MINIMIZE ERROR:", e)
        speak("Не удалось свернуть Spotify")
        return False


# ============================================================
# AUDIO SESSION
# ============================================================

def get_spotify_session():
    try:
        sessions = AudioUtilities.GetAllSessions()
    except Exception as e:
        print("GetAllSessions error:", e)
        return None

    print("AUDIO SESSIONS:")
    for session in sessions:
        if not session.Process:
            continue
        try:
            name = session.Process.name()
            pid = session.Process.pid
            print("SESSION:", name, pid)

            if "spotify" not in name.lower():
                continue

            print("SPOTIFY SESSION FOUND")
            volume = cast(
                session._ctl.QueryInterface(ISimpleAudioVolume),
                POINTER(ISimpleAudioVolume)
            )
            return volume
        except Exception as e:
            print("SESSION ERROR:", e)

    print("SPOTIFY SESSION NOT FOUND")
    return None


# ============================================================
# VOLUME
# ============================================================

def spotify_set_volume(percent):
    print("TRY SET VOLUME:", percent)
    volume = get_spotify_session()
    if not volume:
        print("NO SPOTIFY VOLUME")
        return False

    percent = max(0, min(100, int(percent)))
    print("SET SPOTIFY VOLUME:", percent)

    try:
        volume.SetMasterVolume(percent / 100.0, None)
        return True
    except Exception as e:
        print("SET VOLUME ERROR:", e)
        return False


def spotify_volume_up(step=5):
    volume = get_spotify_session()
    if not volume:
        return False
    try:
        current = volume.GetMasterVolume()
        new_value = min(1.0, current + (step / 100.0))
        volume.SetMasterVolume(new_value, None)
        print("SPOTIFY VOLUME:", round(new_value * 100))
        return True
    except Exception as e:
        print("VOLUME UP ERROR:", e)
        return False


def spotify_volume_down(step=5):
    volume = get_spotify_session()
    if not volume:
        return False
    try:
        current = volume.GetMasterVolume()
        new_value = max(0.0, current - (step / 100.0))
        volume.SetMasterVolume(new_value, None)
        print("SPOTIFY VOLUME:", round(new_value * 100))
        return True
    except Exception as e:
        print("VOLUME DOWN ERROR:", e)
        return False


# ============================================================
# PARSE VOLUME
# ============================================================

def words_to_number(text):
    compounds = [
        ("девяносто пять", 95),
        ("восемьдесят пять", 85),
        ("семьдесят пять", 75),
        ("шестьдесят пять", 65),
        ("пятьдесят пять", 55),
        ("сорок пять", 45),
        ("тридцать пять", 35),
        ("двадцать пять", 25),
        ("пятнадцать", 15),
        ("девяносто", 90),
        ("восемьдесят", 80),
        ("семьдесят", 70),
        ("шестьдесят", 60),
        ("пятьдесят", 50),
        ("сорок", 40),
        ("тридцать", 30),
        ("двадцать", 20),
        ("десять", 10),
        ("сто", 100),
        ("ноль", 0),
        ("пять", 5),
    ]
    for word, value in compounds:
        if word in text:
            return value
    return None


def parse_volume(text):
    match = re.search(r"\b(\d{1,3})\b", text)
    if match:
        value = int(match.group(1))
        return max(0, min(100, value))
    return words_to_number(text)


# ============================================================
# MEDIA KEYS
# Команда уходит в окно Spotify, даже если оно не в фокусе.
# ============================================================

WM_APPCOMMAND = 0x0319
APPCOMMAND_MEDIA_NEXTTRACK = 11
APPCOMMAND_MEDIA_PREVIOUSTRACK = 12
APPCOMMAND_MEDIA_PLAY_PAUSE = 14

_user32 = ctypes.windll.user32


def _media_key(vk):
    _user32.keybd_event(vk, 0, 0, 0)
    _user32.keybd_event(vk, 0, 2, 0)


def _send_media(command, vk):
    hwnd = find_spotify_window()
    if hwnd:
        try:
            win32api.SendMessage(hwnd, WM_APPCOMMAND, hwnd, command << 16)
            print("MEDIA APPCOMMAND", command, "HWND", hwnd)
            return True
        except Exception as e:
            print("APPCOMMAND ERROR:", e)

    print("MEDIA KEY FALLBACK", vk)
    _media_key(vk)
    return True


def media_play_pause():
    _send_media(APPCOMMAND_MEDIA_PLAY_PAUSE, 0xB3)


def media_next():
    _send_media(APPCOMMAND_MEDIA_NEXTTRACK, 0xB0)


def media_previous():
    _send_media(APPCOMMAND_MEDIA_PREVIOUSTRACK, 0xB1)


# ============================================================
# RUN
# ============================================================

def run(jarvis, text):
    if not text:
        return False

    text = text.lower().strip()
    print("[spotify] text:", text)

    has_spotify = is_spotify_context(text)

    # --------------------------------------------------------
    # 1. MINIMIZE
    # --------------------------------------------------------
    if any(x in text for x in ["сверни", "свернуть", "убери", "скрой", "спрячь"]):
        if has_spotify:
            if minimize_spotify():
                done()
            return True
        return False

    if any(x in text for x in [
        "подбери",
        "подборк",
        "диджей",
        "диджея",
        "режим диджея",
    ]):
        result = send("play_dj", {})
        if result and result.get("ok"):
            speak("Подбираю музыку")
        else:
            speak("Не удалось включить диджея")
        return True

    # --------------------------------------------------------
    # 2. OPEN + RESTORE
    # --------------------------------------------------------
    open_restore_triggers = [
        "открой", "открывай", "запусти", "запускай", "включи",
        "разверни", "развернуть", "покажи", "отобрази", "выведи", "верни"
    ]

    if any(x in text for x in open_restore_triggers):
        if any(x in text for x in ["назад", "предыдущ", "прошл"]):
            pass
        elif any(x in text for x in ["воспроизведен", "паузу"]):
            pass
        elif has_spotify:
            if show_or_open_spotify(jarvis):
                done()
            return True
        else:
            return False

    # --------------------------------------------------------
    # 3. EXACT VOLUME
    # --------------------------------------------------------
    if any(x in text for x in ["громкость", "процентов", "процент"]):
        if has_spotify or "громкость" in text:
            value = parse_volume(text)
            if value is not None:
                if spotify_set_volume(value):
                    done()
                else:
                    speak("Не удалось изменить громкость Spotify")
                return True
        return False

    # --------------------------------------------------------
    # 4. VOLUME UP
    # --------------------------------------------------------
    if any(x in text for x in ["громче", "прибавь", "увеличь"]):
        if has_spotify:
            if spotify_volume_up():
                done()
            else:
                speak("Не удалось изменить громкость Spotify")
            return True
        return False

    # --------------------------------------------------------
    # 5. VOLUME DOWN
    # --------------------------------------------------------
    if any(x in text for x in ["тише", "убавь", "уменьши"]):
        if has_spotify:
            if spotify_volume_down():
                done()
            else:
                speak("Не удалось изменить громкость Spotify")
            return True
        return False

    # --------------------------------------------------------
    # 6. PLAY / PAUSE
    # --------------------------------------------------------
    if any(x in text for x in ["пауза", "останови", "продолжи", "возобнови", "играй", "сними с паузы"]):
        if any(x in text for x in ["дискорд", "discord", "телеграм", "telegram", "браузер", "хром", "opera"]):
            return False
        media_play_pause()
        done()
        return True

    # --------------------------------------------------------
    # 7. NEXT
    # --------------------------------------------------------
    if any(x in text for x in ["следующий", "дальше", "переключи", "пропусти", "скип"]):
        if any(x in text for x in ["дискорд", "discord", "телеграм", "telegram", "браузер", "хром", "opera"]):
            return False
        media_next()
        done()
        return True

    # --------------------------------------------------------
    # 8. PREVIOUS
    # --------------------------------------------------------
    if any(x in text for x in ["предыдущий", "предыдущая", "прошлый", "прошлая", "назад"]):
        if any(x in text for x in ["дискорд", "discord", "телеграм", "telegram", "браузер", "хром", "opera"]):
            return False
        media_previous()
        done()
        return True

    if "верни" in text and any(x in text for x in ["назад", "предыдущ", "прошл"]):
        media_previous()
        done()
        return True

    return False