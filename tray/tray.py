import pystray
from PIL import Image
import win32gui
import win32con
import ctypes
import os


# -------------------------
# CONSOLE WINDOW
# -------------------------
hwnd = ctypes.windll.kernel32.GetConsoleWindow()


# -------------------------
# HIDE / SHOW
# -------------------------
def hide_console(icon=None, item=None):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


def show_console(icon=None, item=None):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)


def toggle_console(icon=None, item=None):

    if win32gui.IsWindowVisible(hwnd):
        hide_console()
    else:
        show_console()


# -------------------------
# EXIT
# -------------------------
def quit_app(icon, item):

    icon.stop()

    os._exit(0)


# -------------------------
# START TRAY
# -------------------------
def start_tray():
    icon_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets",
        "icons",
        "jarvis.ico"
    )

    image = Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem("Показать / скрыть", toggle_console),
        pystray.MenuItem("Выход", quit_app)
    )

    icon = pystray.Icon(
        "Jarvis",
        image,
        "JARVIS",
        menu
    )

    # скрываем консоль
    hide_console()

    icon.run()

# ----------------------------------
# created https://github.com/Tynfolz
# ----------------------------------