import os
import sys
import re
import subprocess
from pathlib import Path
from semantic_version import Version
from github_release_downloader import (
    GitHubRepo,
    get_latest_version,
    get_assets,
    download_assets,
)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from utils.version import __version__
from utils.StartTask import close_task

REPO_USER = "ThainanViniciusKatchan"
REPO_NAME = "FileORZ"
DOWNLOADS_DIR = Path("Updates")
ASSETS_MASK = re.compile(r".*\.exe")


def update_check(current_version=__version__):
    try:
        repo = GitHubRepo(REPO_USER, REPO_NAME)
        latest_version = get_latest_version(repo)
        if latest_version is None:
            return False, None

        current = Version(current_version)
        if current < latest_version:
            return True, latest_version
        return False, latest_version
    except Exception as Error:
        print(f"Erro ao verificar atualizações: {Error}")
        return False, None


def download_update(current_version=__version__, downloads_dir=DOWNLOADS_DIR):
    has_update, latest_version = update_check(current_version)
    if has_update and latest_version is not None:
        print(f"Baixando atualização ({latest_version})...")
        try:
            repo = GitHubRepo(REPO_USER, REPO_NAME)
            tag_name = getattr(latest_version, "_origin_tag_name", str(latest_version))
            assets = get_assets(repo, tag_name, ASSETS_MASK)
            if not assets:
                print("Nenhum instalador executável encontrado na release.")
                return None

            downloads_path = Path(downloads_dir)
            download_assets(assets, out_dir=downloads_path)
            print("Download concluído com sucesso!")
            return downloads_path
        except Exception as Error:
            print(f"Erro ao baixar atualização: {Error}")
            return None
    else:
        print("Nenhuma atualização disponivel")
        return None


def install_update(update_path=DOWNLOADS_DIR):
    if update_path is None:
        return "Não foi possível obter o arquivo de atualização"

    update_path = Path(update_path)
    if close_task() is True:
        update_list = list(update_path.glob("*FileORZ_install_*.exe"))
        if not update_list:
            update_list = list(update_path.glob("*.exe"))

        try:
            for update in update_list:
                print(f"Instalando: {update}")
                subprocess.run(str(update))
            return "Atualização instalada com sucesso"
        except Exception as Error:
            print(f"Erro ao instalar atualização: {Error}")
            return "Não foi possível instalar a atualização"
    else:
        return "Não foi possível encerrar os processos"


if __name__ == "__main__":
    ...
