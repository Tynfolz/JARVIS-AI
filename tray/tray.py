import ctypes
import os

import pystray
import win32con
import win32gui
from PIL import Image

hwnd = ctypes.windll.kernel32.GetConsoleWindow()


def hide_console(icon=None, item=None):
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


def show_console(icon=None, item=None):
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)


def toggle_console(icon=None, item=None):
    if hwnd and win32gui.IsWindowVisible(hwnd):
        hide_console()
    else:
        show_console()


def quit_app(icon, item):
    icon.stop()
    os._exit(0)


def start_tray(hide=True):
    icon_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets", "icons", "jarvis.ico",
    )
    image = Image.open(icon_path)

    menu = pystray.Menu(
        pystray.MenuItem("Показать / скрыть", toggle_console),
        pystray.MenuItem("Выход", quit_app),
    )
    icon = pystray.Icon("Jarvis", image, "JARVIS", menu)

    if hide:
        hide_console()

    icon.run()