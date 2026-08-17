import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config


class StartUpSys:
    def __init__(self, value: bool = False):
        self._value = value

    @property
    def enabled(self):
        return self._value

    @enabled.getter
    def GetEnabled(self):
        CONFIG = load_config("dist", "config")
        return CONFIG["Startup"]

    @enabled.setter
    def enabled(self, value: bool):
        CONFIG = load_config("dist", "config")
        CONFIG["Startup"] = value
        save_config("dist", "config", CONFIG)


if __name__ == "__main__":
    # StartUp = StartUpSys()
    # StartUp.enabled = True
    # print(StartUp.GetEnabled)
    ...
