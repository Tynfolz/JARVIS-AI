# plugins/spicetify_bridge.py
# Управление Spotify через Spicetify bridge
# Состояние сервера хранится в sys, чтобы переживать reload плагина

import json
import re
import sys
import threading
import time
import uuid
from typing import Any, Dict, Optional

REQUIREMENTS = [
    "websockets",
]

PHRASES = [
    "включи трек",
    "включи песню",
    "поставь трек",
    "поставь песню",
    "играй трек",
    "играй песню",
    "включи",
    "поставь",
    "найди и включи",
    "найди песню",
    "найди трек",
    "включи плейлист",
    "поставь плейлист",
    "запусти плейлист",
    "открой плейлист",
    "играй плейлист",
    "включи плэй лист",
    "включи любимые",
    "включи любимые треки",
    "поставь любимые",
    "поставь любимые треки",
    "добавь в плейлист",
    "добавь трек в плейлист",
    "добавь песню в плейлист",
    "добавь текущий трек в плейлист",
    "добавь эту песню в плейлист",
    "добавь в любимые",
    "добавь в любимые треки",
    "сохрани в плейлист",
    "сохрани в любимые",
    "кинь в плейлист",
    "кинь в любимые",
    "что играет",
    "что сейчас играет",
    "какой трек",
    "какая песня",
    "какой сейчас трек",
    "какое трек сейчас играет",
    "сейчас играет",
]

WS_HOST = "127.0.0.1"
WS_PORT = 18765
_STATE_KEY = "_jarvis_spicetify_bridge_state"


def _state() -> dict:
    st = getattr(sys, _STATE_KEY, None)
    if st is None:
        st = {
            "clients": set(),
            "pending": {},
            "lock": threading.Lock(),
            "start_lock": threading.Lock(),
            "started": False,
            "loop": None,
            "server": None,
        }
        setattr(sys, _STATE_KEY, st)
    return st


def _ensure_server():
    st = _state()
    with st["start_lock"]:
        if st["started"]:
            return
        st["started"] = True

    def runner():
        import asyncio
        from websockets.server import serve

        async def handler(websocket):
            st2 = _state()
            st2["clients"].add(websocket)
            print("[spicetify_bridge] client connected, total:", len(st2["clients"]))
            try:
                async for raw in websocket:
                    try:
                        msg = json.loads(raw)
                    except Exception:
                        continue

                    mtype = msg.get("type")
                    if mtype == "hello":
                        print("[spicetify_bridge] hello from", msg.get("client"))
                        continue

                    if mtype == "response":
                        rid = msg.get("id")
                        print(
                            "[spicetify_bridge] response id=",
                            rid,
                            "ok=",
                            msg.get("ok"),
                            "err=",
                            msg.get("error"),
                        )
                        if rid:
                            with st2["lock"]:
                                fut = st2["pending"].get(rid)
                                if fut is not None:
                                    fut["result"] = msg
                                    fut["event"].set()
            finally:
                st2["clients"].discard(websocket)
                print("[spicetify_bridge] client disconnected, total:", len(st2["clients"]))

        async def main():
            try:
                server = await serve(handler, WS_HOST, WS_PORT)
            except OSError as e:
                print("[spicetify_bridge] bind failed (port busy?):", e)
                # порт занят старым процессом — всё равно помечаем loop
                return
            st3 = _state()
            st3["server"] = server
            print(f"[spicetify_bridge] WS server on ws://{WS_HOST}:{WS_PORT}")
            await asyncio.Future()

        loop = asyncio.new_event_loop()
        st4 = _state()
        st4["loop"] = loop
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
        except Exception as e:
            print("[spicetify_bridge] server crashed:", e)

    t = threading.Thread(target=runner, daemon=True, name="spicetify-ws")
    t.start()
    time.sleep(0.6)


def _wait_for_client(timeout: float = 8.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        st = _state()
        if st["clients"]:
            return True
        time.sleep(0.15)
    return bool(_state()["clients"])


def _send_command(action: str, payload: Optional[dict] = None, timeout: float = 10.0) -> dict:
    import asyncio

    _ensure_server()
    st = _state()

    if not st["clients"]:
        print("[spicetify_bridge] no clients yet, waiting... (have", len(st["clients"]), ")")
        if not _wait_for_client(8.0):
            return {
                "ok": False,
                "error": "Spicetify bridge не подключён. Открой Spotify со Spicetify и jarvis-bridge. Сначала Jarvis, потом Spotify.",
            }

    req_id = str(uuid.uuid4())
    event = threading.Event()
    with st["lock"]:
        st["pending"][req_id] = {"event": event, "result": None}

    message = json.dumps(
        {
            "type": "command",
            "id": req_id,
            "action": action,
            "payload": payload or {},
        },
        ensure_ascii=False,
    )

    print(
        "[spicetify_bridge] send",
        action,
        "id=",
        req_id,
        "clients=",
        len(st["clients"]),
    )

    async def _broadcast():
        st2 = _state()
        dead = []
        for ws in list(st2["clients"]):
            try:
                await ws.send(message)
            except Exception as e:
                print("[spicetify_bridge] send error:", e)
                dead.append(ws)
        for ws in dead:
            st2["clients"].discard(ws)

    loop = st["loop"]
    try:
        if loop and loop.is_running():
            fut = asyncio.run_coroutine_threadsafe(_broadcast(), loop)
            fut.result(timeout=3.0)
        else:
            with st["lock"]:
                st["pending"].pop(req_id, None)
            return {"ok": False, "error": "WS loop not running"}
    except Exception as e:
        with st["lock"]:
            st["pending"].pop(req_id, None)
        return {"ok": False, "error": f"send failed: {e}"}

    ok = event.wait(timeout=timeout)
    with st["lock"]:
        entry = st["pending"].pop(req_id, None)

    if not ok or not entry or not entry.get("result"):
        return {"ok": False, "error": "timeout — нет ответа от Spicetify"}

    return entry["result"]


def _speak(text: str):
    try:
        from voice.tts import speak
        speak(text)
    except Exception:
        print("[spicetify_bridge] speak:", text)


def _done():
    try:
        from core.phrases import COMMAND_DONE, random_phrase
        from voice.tts import speak
        speak(random_phrase(COMMAND_DONE))
    except Exception:
        _speak("Готово")


def _normalize(text: str) -> str:
    t = text.lower().strip()
    repl = [
        ("плэй лист", "плейлист"),
        ("плей лист", "плейлист"),
        ("плэйлист", "плейлист"),
        ("play list", "плейлист"),
        ("playlist", "плейлист"),
        ("трека ", "трек "),
        ("какое трек", "какой трек"),
        ("какая трек", "какой трек"),
        ("любимая", "любимые"),
        ("любимую", "любимые"),
        ("любимое", "любимые"),
    ]
    for a, b in repl:
        t = t.replace(a, b)
    t = t.replace("плейлист лист", "плейлист")
    while "  " in t:
        t = t.replace("  ", " ")
    return t.strip()


def _is_liked(name: str) -> bool:
    if not name:
        return False
    n = name.lower().strip()
    keys = ["любим", "лайк", "liked", "favorite", "favourite", "избран", "моя музыка"]
    return any(k in n for k in keys)


def _strip_cmd(text: str, prefixes) -> str:
    t = text.strip()
    for p in sorted(prefixes, key=len, reverse=True):
        if t.startswith(p):
            return t[len(p) :].strip(" \t-—:")
    return t


def _parse_play_track(text: str) -> Optional[str]:
    if "плейлист" in text:
        return None
    if any(x in text for x in ["добавь", "сохрани", "кинь"]):
        return None
    if _is_liked(text) and any(
        x in text for x in ["включи", "поставь", "запусти", "открой", "играй"]
    ):
        return None

    prefixes = [
        "найди и включи",
        "найди песню",
        "найди трек",
        "включи трек",
        "включи песню",
        "поставь трек",
        "поставь песню",
        "играй трек",
        "играй песню",
        "включи",
        "поставь",
        "играй",
    ]
    q = _strip_cmd(text, prefixes)
    if not q or q in ("трек", "песню", "музыку", "спотифай", "spotify", "плейлист"):
        return None
    return q


def _parse_play_playlist(text: str) -> Optional[str]:
    if "плейлист" not in text and not (
        _is_liked(text)
        and any(x in text for x in ["включи", "поставь", "запусти", "открой", "играй"])
    ):
        return None

    prefixes = [
        "включи плейлист",
        "поставь плейлист",
        "запусти плейлист",
        "открой плейлист",
        "играй плейлист",
        "включи",
        "поставь",
        "запусти",
        "открой",
        "играй",
    ]
    q = _strip_cmd(text, prefixes)
    q = q.replace("плейлист", "").strip(" \t-—:")
    if not q and _is_liked(text):
        return "любимые"
    return q or None


def _parse_add_to_playlist(text: str) -> Optional[dict]:
    if not any(x in text for x in ["добавь", "сохрани", "кинь"]):
        return None

    if _is_liked(text) and "плейлист" not in text:
        return {"mode": "current", "playlist": "любимые", "query": None}

    if "плейлист" not in text and not _is_liked(text):
        return None

    m = re.search(
        r"(?:добавь|сохрани|кинь)\s+(?:трек\s+|песн[ую]\s+)?(.+?)\s+в\s+плейлист\s+(.+)$",
        text,
    )
    if m:
        left, playlist = m.group(1).strip(), m.group(2).strip()
        if left in ("текущий", "текущую", "этот", "эту", "эту песню", "этот трек") or not left:
            return {"mode": "current", "playlist": playlist, "query": None}
        return {"mode": "search", "playlist": playlist, "query": left}

    m = re.search(r"(?:добавь|сохрани|кинь).*?(?:в\s+)?(?:плейлист\s+)?(.+)$", text)
    if m:
        name = m.group(1).strip().replace("плейлист", "").strip()
        if not name or _is_liked(name) or _is_liked(text):
            name = "любимые"
        return {"mode": "current", "playlist": name, "query": None}

    return None


def run(jarvis, text: str) -> bool:
    if not text or not isinstance(text, str):
        return False

    text = _normalize(text)
    print("[spicetify_bridge] text:", text)
    print("[spicetify_bridge] clients now:", len(_state()["clients"]))

    _ensure_server()

    if any(
        x in text
        for x in [
            "что играет",
            "что сейчас играет",
            "какой трек",
            "какая песня",
            "какой сейчас трек",
            "какая сейчас песня",
            "сейчас играет",
        ]
    ):
        res = _send_command("now_playing")
        print("[spicetify_bridge] now_playing result:", res)
        if not res.get("ok"):
            _speak(res.get("error") or "Не удалось узнать трек")
            return True
        track = (res.get("data") or {}).get("track")
        if not track:
            _speak("Сейчас ничего не играет")
        else:
            artists = track.get("artists") or ""
            name = track.get("name") or ""
            if artists:
                _speak(f"Сейчас играет {name}, {artists}")
            else:
                _speak(f"Сейчас играет {name}")
        return True

    add = _parse_add_to_playlist(text)
    if add:
        if add["mode"] == "current":
            res = _send_command("add_to_playlist", {"playlistName": add["playlist"]})
        else:
            res = _send_command(
                "add_search_to_playlist",
                {"query": add["query"], "playlistName": add["playlist"]},
            )
        print("[spicetify_bridge] add result:", res)
        if res.get("ok"):
            _done()
        else:
            err = str(res.get("error") or "")
            if "not found" in err.lower():
                _speak("Не нашёл плейлист или трек")
            else:
                _speak("Не удалось добавить в плейлист")
        return True

    pl = _parse_play_playlist(text)
    if pl:
        res = _send_command("play_playlist", {"name": pl, "query": pl})
        print("[spicetify_bridge] playlist result:", res)
        if res.get("ok"):
            name = (res.get("data") or {}).get("name") or pl
            _speak(f"Включаю плейлист {name}")
        else:
            _speak("Плейлист не найден")
        return True

    q = _parse_play_track(text)
    if q:
        res = _send_command("play_track", {"query": q})
        print("[spicetify_bridge] track result:", res)
        if res.get("ok"):
            played = (res.get("data") or {}).get("played")
            if played:
                title = played.get("name") or q
                artists = played.get("artists") or ""
                if artists:
                    _speak(f"Включаю {title}, {artists}")
                else:
                    _speak(f"Включаю {title}")
            else:
                _done()
        else:
            _speak("Трек не найден")
        return True

    return False


# старт сервера сразу при импорте плагина
try:
    _ensure_server()
    print("[spicetify_bridge] server started on import")
except Exception as _e:
    print("[spicetify_bridge] early start failed:", _e)