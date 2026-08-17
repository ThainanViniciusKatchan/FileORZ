from model import load_config, save_config


class Translate:
    def __init__(self, lang: str = "", local: str = "", name: str = ""):
        self.lang = lang
        self.local = local
        self.name = name

    def set_locate(self, lang: str = "") -> None:
        config = load_config("dist", "config")
        config["lang"] = lang
        save_config("dist", "config", config)
        self.lang = lang

    def get_locate(self) -> str:
        file = load_config("dist", "config")
        self.lang = file["lang"]
        return self.lang

    def get_text(self, local: str, name: str) -> str:
        lang = self.get_locate()
        file = load_config("locate", lang)
        json_data = file.get(local, {}).get(name, {})
        return json_data


if __name__ == "__main__":
    Translate().set_locate(lang="pt-br")
    print(Translate().get_locate())
    print(f"Text: {Translate().get_text('index_window', 'title')}")
