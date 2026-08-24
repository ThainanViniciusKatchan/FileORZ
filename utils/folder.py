import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config


class Folder:
    def __init__(self, folder: str = ""):
        self._folderOrz = folder

    @property
    def folder(self) -> str:
        return self._folderOrz

    @folder.getter
    def Getfolder(self) -> str:
        CONFIG = load_config("dist", "config")
        return CONFIG["Folder"]

    @folder.setter
    def folder(self, folder: str):
        CONFIG = load_config("dist", "config")
        if CONFIG["timeverification"]:
            pass
        if folder != "":
            if folder != Folder.Getfolder:
                CONFIG["Folder"] = folder.replace("/", "\\")
                save_config("dist", "config", CONFIG)
            else:
                pass
        else:
            pass


class Delete_Folde:
    def __init__(
        self,
        ativado: bool = False,
        lixeira: bool = False,
        excluir_permanentemente: bool = False,
        pasta_orz: bool = False,
        todas: bool = False,
    ):
        self._ativado = ativado
        self._lixeira = lixeira
        self._excluir_permanentemente = excluir_permanentemente
        self._pasta_orz = pasta_orz
        self._todas = todas

    @property
    def ativado(self) -> bool:
        return self._ativado

    @ativado.setter
    def ativado(self, ativado: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["ativado"] = ativado
        save_config("dist", "config", CONFIG)

    @ativado.getter
    def Getativado(self) -> bool:
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("ativado", False)

    @property
    def lixeira(self) -> bool:
        return self._lixeira

    @lixeira.setter
    def lixeira(self, lixeira: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["lixeira"] = lixeira
        save_config("dist", "config", CONFIG)

    @lixeira.getter
    def Getlixeira(self) -> bool:
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("lixeira", False)

    @property
    def excluir_permanentemente(self) -> bool:
        return self._excluir_permanentemente

    @excluir_permanentemente.setter
    def excluir_permanentemente(self, excluir_permanentemente: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["excluir_permanentemente"] = excluir_permanentemente
        save_config("dist", "config", CONFIG)

    @excluir_permanentemente.getter
    def Getexcluir_permanentemente(self) -> bool:
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("excluir_permanentemente", False)

    @property
    def pasta_orz(self) -> bool:
        return self._pasta_orz

    @pasta_orz.setter
    def pasta_orz(self, pasta_orz: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["pastas_ORZ"] = pasta_orz
        save_config("dist", "config", CONFIG)

    @pasta_orz.getter
    def Getpasta_orz(self) -> bool:
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("pastas_ORZ", False)

    @property
    def todas(self) -> bool:
        return self._todas

    @todas.setter
    def todas(self, todas: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["todas"] = todas
        if "tudo" in CONFIG["folder_delete"]:
            del CONFIG["folder_delete"]["tudo"]
        save_config("dist", "config", CONFIG)

    @todas.getter
    def Gettodas(self) -> bool:
        CONFIG = load_config("dist", "config")
        fd = CONFIG.get("folder_delete", {})
        return fd.get("todas", fd.get("tudo", False))


if __name__ == "__main__":
    ...