import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.model import load_config, save_config


class AutoDelete:
    def __init__(
        self, AutoDell: bool = bool, Trash: bool = bool, Permanently: bool = bool
    ):
        self._AutoDell = AutoDell
        self._Trash = Trash
        self._Permanently = Permanently

    @property
    def AutoDelete(self):
        return self._AutoDell

    @property
    def Lixeira(self):
        return self._Trash

    @property
    def Permanente(self):
        return self._Permanently

    def GetFilters(self):
        CONFIG = load_config("dist", "config")
        items = dict()
        for k, v in CONFIG.items():
            if k == "Enviar Para Lixeira" or k == "Excluir permanentemente":
                items[k] = v
        return items

    @AutoDelete.getter
    def GetAutoDelete(self):
        CONFIG = load_config("dist", "config")
        return CONFIG["AutoDelete"]

    @AutoDelete.setter
    def AutoDelete(self, AutoDell: bool):
        CONFIG = load_config("dist", "config")
        CONFIG["AutoDelete"] = AutoDell
        save_config("dist", "config", CONFIG)

    @Lixeira.getter
    def GetLixeira(self):
        CONFIG = load_config("dist", "config")
        return CONFIG["Enviar Para Lixeira"]

    @Lixeira.setter
    def Lixeira(self, Trash: bool):
        CONFIG = load_config("dist", "config")
        CONFIG["Enviar Para Lixeira"] = Trash
        save_config("dist", "config", CONFIG)

    @Permanente.getter
    def GetPermanente(self):
        CONFIG = load_config("dist", "config")
        return CONFIG["Excluir permanentemente"]

    @Permanente.setter
    def Permanente(self, Permanently: bool):
        CONFIG = load_config("dist", "config")
        CONFIG["Excluir permanentemente"] = Permanently
        save_config("dist", "config", CONFIG)

    def SetFilters(self, filter: str, value: bool):
        CONFIG = load_config("dist", "config")
        for C in CONFIG:
            if C in AutoDelete.GetFilters(None).keys():
                if filter == C:
                    CONFIG[filter] = value
                else:
                    CONFIG[C] = False
                if filter == True and C == True:
                    raise ValueError(
                        "Ambos os filtros não podem ser ativados ao mesmo tempo"
                    )
        save_config("dist", "config", CONFIG)


class AutoDeleFilter:
    def __init__(self, datacriacao: bool = False, datamodificacao: bool = False):
        self._DataCriacao = datacriacao
        self._DataModificacao = datamodificacao

    @property
    def DataCriacao(self):
        return self._DataCriacao

    @property
    def DataModificacao(self):
        return self._datamodificacao

    @DataCriacao.getter
    def GetDataCriacao(self):
        CONFIG = load_config("dist", "config")
        return CONFIG["AutoDeleteConfig"]["Por Data de Criação"]

    @DataCriacao.setter
    def DataCriacao(self, datacriacao: bool):
        CONFIG = load_config("dist", "config")
        CONFIG["AutoDeleteConfig"]["Por Data de Criação"] = datacriacao
        save_config("dist", "config", CONFIG)

    @DataModificacao.getter
    def GetDataModificacao(self):
        CONFIG = load_config("dist", "config")
        return CONFIG["AutoDeleteConfig"]["Por Data de Modificação"]

    @DataModificacao.setter
    def DataModificacao(self, datamodificacao: bool):
        CONFIG = load_config("dist", "config")
        CONFIG["AutoDeleteConfig"]["Por Data de Modificação"] = datamodificacao
        save_config("dist", "config", CONFIG)

    def GetFilters(self):
        CONFIG = load_config("dist", "config")
        items = dict()
        for k, v in CONFIG["AutoDeleteConfig"].items():
            if k == "Por Data de Criação" or k == "Por Data de Modificação":
                items[k] = v
        return items

    def SetFilters(self, filter: str, value: bool):
        CONFIG = load_config("dist", "config")
        for F in CONFIG["AutoDeleteConfig"]:
            if F in AutoDeleFilter.GetFilters(None).keys():
                if filter == F:
                    CONFIG["AutoDeleteConfig"][filter] = value
                else:
                    CONFIG["AutoDeleteConfig"][F] = False
                if filter == True and F == True:
                    raise ValueError(
                        "Ambos os filtros não podem ser ativados ao mesmo tempo"
                    )
        save_config("dist", "config", CONFIG)


class Folder_Delete:
    def __init__(self):
        pass

    @property
    def Ativado(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("ativado", False)

    @property
    def Lixeira(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("lixeira", False)

    @property
    def Permanente(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("excluir_permanentemente", False)

    @property
    def PastaORZ(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("pastas_ORZ", False)

    @property
    def Tudo(self):
        CONFIG = load_config("dist", "config")
        fd = CONFIG.get("folder_delete", {})
        return fd.get("todas", fd.get("tudo", False))

    @Ativado.getter
    def GetAtivado(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("ativado", False)

    @Ativado.setter
    def Ativado(self, ativado: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["ativado"] = ativado
        save_config("dist", "config", CONFIG)

    @Lixeira.getter
    def GetLixeira(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("lixeira", False)

    @Lixeira.setter
    def Lixeira(self, lixeira: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["lixeira"] = lixeira
        save_config("dist", "config", CONFIG)

    @Permanente.getter
    def GetPermanente(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("excluir_permanentemente", False)

    @Permanente.setter
    def Permanente(self, perma: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["excluir_permanentemente"] = perma
        save_config("dist", "config", CONFIG)

    @PastaORZ.getter
    def GetPastaORZ(self):
        CONFIG = load_config("dist", "config")
        return CONFIG.get("folder_delete", {}).get("pastas_ORZ", False)

    @PastaORZ.setter
    def PastaORZ(self, pastaORZ: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["pastas_ORZ"] = pastaORZ
        save_config("dist", "config", CONFIG)

    @Tudo.getter
    def GetTudo(self):
        CONFIG = load_config("dist", "config")
        fd = CONFIG.get("folder_delete", {})
        return fd.get("todas", fd.get("tudo", False))

    @Tudo.setter
    def Tudo(self, tudo: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {}
        CONFIG["folder_delete"]["todas"] = tudo
        if "tudo" in CONFIG["folder_delete"]:
            del CONFIG["folder_delete"]["tudo"]
        save_config("dist", "config", CONFIG)

    def GetFilters(self):
        CONFIG = load_config("dist", "config")
        fd = CONFIG.get("folder_delete", {})
        return {
            "lixeira": fd.get("lixeira", False),
            "excluir_permanentemente": fd.get("excluir_permanentemente", False),
            "pastas_ORZ": fd.get("pastas_ORZ", False),
            "todas": fd.get("todas", fd.get("tudo", False)),
        }

    def SetFilters(self, filter_key: str, value: bool):
        CONFIG = load_config("dist", "config")
        if "folder_delete" not in CONFIG:
            CONFIG["folder_delete"] = {
                "ativado": False,
                "lixeira": True,
                "excluir_permanentemente": False,
                "pastas_ORZ": False,
                "todas": True,
            }
        if filter_key in ("lixeira", "excluir_permanentemente"):
            CONFIG["folder_delete"]["lixeira"] = (filter_key == "lixeira" and value)
            CONFIG["folder_delete"]["excluir_permanentemente"] = (filter_key == "excluir_permanentemente" and value)
        elif filter_key in ("pastas_ORZ", "todas", "tudo"):
            is_orz = filter_key == "pastas_ORZ" and value
            CONFIG["folder_delete"]["pastas_ORZ"] = is_orz
            CONFIG["folder_delete"]["todas"] = not is_orz
            if "tudo" in CONFIG["folder_delete"]:
                del CONFIG["folder_delete"]["tudo"]
        elif filter_key == "ativado":
            CONFIG["folder_delete"]["ativado"] = value

        save_config("dist", "config", CONFIG)
