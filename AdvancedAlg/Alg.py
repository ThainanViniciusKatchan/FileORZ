import os
import re
import shutil
import unicodedata
from pathlib import Path
import pypdf
from utils.model import load_config
from utils import folder


def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    texto_sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto_sem_acento).strip().lower()



def extrair_texto_pdf(caminho_arquivo: str) -> str:
    paginas_texto = []
    try:
        with open(caminho_arquivo, "rb") as f:
            pdf = pypdf.PdfReader(f)
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    paginas_texto.append(texto)
    except Exception as e:
        print(f"[ERRO] Falha ao extrair texto do PDF {caminho_arquivo}: {e}")
        return ""
    return " ".join(paginas_texto)


def classificar_documento(texto_normalizado: str, config_palavras: dict) -> tuple[str | None, int, list]:
    if not texto_normalizado:
        return None, 0, []

    scores = {}
    termos_por_categoria = {}

    for categoria, palavras in config_palavras.items():
        score = 0
        termos_vistos = set()
        encontrados = []

        for palavra in palavras:
            palavra_norm = normalizar_texto(palavra).strip(" ,.-_")
            if not palavra_norm or palavra_norm in termos_vistos:
                continue
            termos_vistos.add(palavra_norm)

            padrao = r"(?<!\w)" + re.escape(palavra_norm) + r"(?!\w)"
            matches = re.findall(padrao, texto_normalizado)
            if matches:
                palavras_no_termo = len(palavra_norm.split())
                if palavras_no_termo >= 2:
                    peso = 3 * palavras_no_termo
                elif len(palavra_norm) <= 3:
                    peso = 1
                else:
                    peso = 2

                bonus_freq = min(len(matches) - 1, 2)
                termo_score = peso + bonus_freq
                score += termo_score
                encontrados.append(palavra)

        scores[categoria] = score
        termos_por_categoria[categoria] = encontrados

    if not scores:
        return None, 0, []

    categorias_ordenadas = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    melhor_categoria, melhor_score = categorias_ordenadas[0]

    if melhor_score < 2:
        return None, 0, []

    if len(categorias_ordenadas) > 1 and categorias_ordenadas[1][1] == melhor_score:
        print(f"[AVISO] Empate de relevância entre '{melhor_categoria}' e '{categorias_ordenadas[1][0]}' (Score: {melhor_score}). Arquivo não movido.")
        return None, melhor_score, []

    return melhor_categoria, melhor_score, termos_por_categoria.get(melhor_categoria, [])


def obter_destino_unico(pasta_destino: str, nome_arquivo: str) -> str:
    destino = os.path.join(pasta_destino, nome_arquivo)
    if not os.path.exists(destino):
        return destino

    nome_base, ext = os.path.splitext(nome_arquivo)
    contador = 1
    while True:
        novo_nome = f"{nome_base}_{contador}{ext}"
        destino = os.path.join(pasta_destino, novo_nome)
        if not os.path.exists(destino):
            return destino
        contador += 1


def processar_texto(diretorio: str = None):
    try:
        config = load_config("dist", "Key_Words")
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar as palavras-chave: {e}")
        return

    if not config:
        return

    diretorio_base = diretorio or folder.Folder().Getfolder
    if not diretorio_base or not os.path.exists(diretorio_base):
        print(f"[INFO] Diretório não configurado ou inacessível: {diretorio_base}")
        return

    try:
        arquivos = [f for f in os.listdir(diretorio_base) if f.lower().endswith(".pdf")]
    except Exception as e:
        print(f"[ERRO] Não foi possível listar o diretório {diretorio_base}: {e}")
        return

    for file in arquivos:
        caminho_completo = os.path.join(diretorio_base, file)
        if not os.path.isfile(caminho_completo):
            continue

        texto = extrair_texto_pdf(caminho_completo)
        texto_norm = normalizar_texto(texto)

        categoria, score, termos = classificar_documento(texto_norm, config)
        if not categoria:
            continue

        pasta_destino = os.path.join(diretorio_base, categoria)
        Path(pasta_destino).mkdir(parents=True, exist_ok=True)
        destino_arquivo = obter_destino_unico(pasta_destino, file)

        try:
            shutil.move(caminho_completo, destino_arquivo)
            print(f"[SUCESSO] '{file}' -> '{categoria}' (Score: {score}, Termos: {', '.join(termos)})")
        except Exception as e:
            print(f"[ERRO] Falha ao mover arquivo '{file}' para '{pasta_destino}': {e}")


if __name__ == "__main__":
    processar_texto()

