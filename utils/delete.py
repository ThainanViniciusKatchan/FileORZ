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
        self.CONFIG = load_config("dist", "config")

    @property
    def Ativado(self):
        return self.CONFIG["folder_delete"]["ativado"]

    @property
    def Lixeira(self):
        return self.CONFIG["folder_delete"]["lixeira"]

    @property
    def Permanente(self):
        return self.CONFIG["folder_delete"]["excluir_permanentemente"]

    @property
    def PastaORZ(self):
        return self.CONFIG["folder_delete"]["pastas_ORZ"]

    @property
    def Tudo(self):
        return self.CONFIG["folder_delete"]["tudo"]

    @Ativado.getter
    def GetAtivado(self):
        return self.CONFIG["folder_delete"]["ativado"]

    @Ativado.setter
    def Ativado(self, ativado: bool):
        self.CONFIG["folder_delete"]["ativado"] = ativado
        save_config("dist", "config", self.CONFIG)

    @Lixeira.getter
    def GetLixeira(self):
        return self.CONFIG["folder_delete"]["lixeira"]

    @Lixeira.setter
    def Lixeira(self, lixeira: bool):
        self.CONFIG["folder_delete"]["lixeira"] = lixeira
        save_config("dist", "config", self.CONFIG)

    @Permanente.getter
    def GetPermanente(self):
        return self.CONFIG["folder_delete"]["excluir_permanentemente"]

    @Permanente.setter
    def Permanente(self, perma: bool):
        self.CONFIG["folder_delete"]["excluir_permanentemente"] = perma
        save_config("dist", "config", self.CONFIG)

    @PastaORZ.getter
    def GetPastaORZ(self):
        return self.CONFIG["folder_delete"]["pastas_ORZ"]

    @PastaORZ.setter
    def PastaORZ(self, pastaORZ: bool):
        self.CONFIG["folder_delete"]["pastas_ORZ"] = pastaORZ
        save_config("dist", "config", self.CONFIG)

    @Tudo.getter
    def GetTudo(self):
        return self.CONFIG["folder_delete"]["tudo"]

    @Tudo.setter
    def Tudo(self, tudo: bool):
        self.CONFIG["folder_delete"]["tudo"] = tudo
        save_config("dist", "config", self.CONFIG)

    def GetFilters(self):
        CONFIG = load_config("dist", "config")
        items = dict()
        for k, v in CONFIG["folder_delete"].items():
            if (
                k == "ativado"
                or k == "lixeira"
                or k == "excluir_permanentemente"
                or k == "pastas_ORZ"
                or k == "tudo"
            ):
                items[k] = v
        return items

    def SetFilters(self, filter: str, value: bool):
        CONFIG = load_config("dist", "config")
        for F in CONFIG["folder_delete"]:
            if F == "ativado":
                continue
            if F in Folder_Delete.GetFilters(None).keys():
                if filter == "excluir_permanentemente" or filter == "lixeira":
                    CONFIG["folder_delete"][filter] = value
                    if filter != F:
                        CONFIG["folder_delete"][F] = False
                else:
                    CONFIG["folder_delete"][filter] = value
        save_config("dist", "config", CONFIG)


if __name__ == "__main__":
    Folder_Delete().SetFilters("ativado", True)
    Folder_Delete().SetFilters("lixeira", True)
    Folder_Delete().SetFilters("pastas_ORZ", True)
    print(Folder_Delete().GetFilters())
