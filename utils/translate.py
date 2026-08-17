import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config


class Translate:
    _listeners = []

    def __init__(self, lang: str = "", local: str = "", name: str = ""):
        self.lang = lang
        self.local = local
        self.name = name

    @classmethod
    def register_listener(cls, callback) -> None:
        if callback not in cls._listeners:
            cls._listeners.append(callback)

    @classmethod
    def unregister_listener(cls, callback) -> None:
        if callback in cls._listeners:
            cls._listeners.remove(callback)

    @classmethod
    def notify_listeners(cls) -> None:
        dead_listeners = []
        for callback in cls._listeners:
            try:
                callback()
            except Exception:
                dead_listeners.append(callback)
        for dead in dead_listeners:
            if dead in cls._listeners:
                cls._listeners.remove(dead)

    def set_locate(self, lang: str = "") -> None:
        config = load_config("dist", "config")
        config["lang"] = lang
        save_config("dist", "config", config)
        self.lang = lang
        self.notify_listeners()

    def get_locate(self) -> str:
        file = load_config("dist", "config")
        self.lang = file.get("lang", "pt-br")
        return self.lang

    def get_text(self, local: str, name: str) -> str:
        lang = self.get_locate()
        try:
            file = load_config("locate", lang)
            json_data = file.get(local, {}).get(name)
            if json_data:
                return json_data
        except Exception:
            pass

        # Fallback para pt-br
        try:
            fallback_file = load_config("locate", "pt-br")
            return fallback_file.get(local, {}).get(name, "")
        except Exception:
            return ""


if __name__ == "__main__":
    Translate().set_locate(lang="pt-br")
    print(Translate().get_locate())
    print(f"Text: {Translate().get_text('index_window', 'title')}")

