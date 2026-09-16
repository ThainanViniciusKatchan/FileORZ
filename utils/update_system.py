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

REPO_USER = "ThainanViniciusKatchan"
REPO_NAME = "FileORZ"
DOWNLOADS_DIR = Path(PROJECT_DIR) / "Updates"
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
        return False, "Não foi possível obter o arquivo de atualização"

    update_path = Path(update_path)
    if not update_path.is_absolute():
        update_path = Path(PROJECT_DIR) / update_path

    if not update_path.exists():
        return False, f"Pasta de atualização não encontrada: {update_path}"

    update_list = sorted(
        update_path.glob("*FileORZ_install_*.exe"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not update_list:
        update_list = sorted(
            update_path.glob("*.exe"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    if not update_list:
        return False, "Nenhum instalador executável encontrado"

    installer = update_list[0]

    try:
        print(f"Iniciando instalador: {installer}")
        if hasattr(os, "startfile"):
            os.startfile(str(installer))
        else:
            creationflags = 0
            if sys.platform == "win32":
                creationflags = (
                    subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
                )
            subprocess.Popen(
                [str(installer)],
                creationflags=creationflags,
                close_fds=True,
            )
        return True, "Instalador iniciado com sucesso"
    except Exception as Error:
        print(f"Erro ao iniciar instalador: {Error}")
        return False, f"Não foi possível iniciar o instalador: {Error}"


if __name__ == "__main__":
    ...
