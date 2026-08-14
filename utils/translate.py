from model import json_path
import json


class Translate:
    def __init__(self, lang: str = "pt-br", local: str = "", name: str = ""):
        self.lang = lang
        self.local = local
        self.name = name

    def get_json(self, local: str) -> str:

        JSON_PATH = json_path("locate", self.lang)

        json_data = ""
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        return json_data

    def get_text(self, local: str, name: str) -> str:
        json_data = self.get_json(local)
        text_load = json_data.get(local, {}).get(name, {})
        return text_load


if __name__ == "__main__":
    print(f"Text: {Translate().get_text('index_window', 'title')}")
