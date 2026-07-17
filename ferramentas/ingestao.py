"""Baixa um material de origem, valida, calcula hash e registra no inventário.

Uso:
  python ingestao.py <url_arquivo> --ano 2025 --tipo prova --fase "1ª fase" \
      --pagina-origem https://www.vestibular.ita.br/provas.htm \
      [--dia ""] [--materia ""] [--fonte "vestibular.ita.br"] [--oficial sim] \
      [--nome-padronizado ita-2025-fase1-original.pdf]

O arquivo é salvo intacto em arquivos/originais/ita/<ano>/ e a linha é
acrescentada em docs/coordenacao/INVENTARIO_ITA.csv com situação `encontrado`
(ou `invalido`, se a validação falhar). Nunca sobrescreve um arquivo existente
com conteúdo diferente — nesse caso aborta e pede decisão humana.
"""

import argparse
import csv
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from comum import sha256_arquivo
from validar_pdf import validar

RAIZ = Path(__file__).resolve().parent.parent
INVENTARIO = RAIZ / "docs" / "coordenacao" / "INVENTARIO_ITA.csv"
ORIGINAIS = RAIZ / "arquivos" / "originais" / "ita"

CABECALHO = [
    "instituicao", "ano", "fase_formato", "dia", "materia", "tipo_material",
    "nome_original", "nome_padronizado", "url_pagina_origem", "url_arquivo",
    "fonte", "oficial", "situacao_autorizacao", "data_acesso", "num_paginas",
    "tamanho_bytes", "sha256", "situacao", "observacoes",
]


def baixar(url: str, destino: Path, tentativas: int = 4) -> None:
    """Download com tentativas e intervalo educado entre elas."""
    ultimo_erro = None
    for i in range(tentativas):
        try:
            requisicao = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (projeto de estudos; download pausado)"}
            )
            with urllib.request.urlopen(requisicao, timeout=60) as resposta, open(destino, "wb") as f:
                f.write(resposta.read())
            return
        except Exception as e:
            ultimo_erro = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"download falhou após {tentativas} tentativas: {ultimo_erro}")


def registrar_linha(linha: dict) -> None:
    with open(INVENTARIO, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CABECALHO).writerow(linha)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--ano", required=True)
    ap.add_argument("--tipo", required=True, help="prova | gabarito | outro")
    ap.add_argument("--fase", default="", dest="fase_formato")
    ap.add_argument("--dia", default="")
    ap.add_argument("--materia", default="")
    ap.add_argument("--pagina-origem", required=True)
    ap.add_argument("--fonte", default="vestibular.ita.br")
    ap.add_argument("--oficial", default="sim", choices=["sim", "nao"])
    ap.add_argument("--autorizacao", default="acervo público oficial")
    ap.add_argument("--nome-padronizado", default="")
    ap.add_argument("--observacoes", default="")
    args = ap.parse_args()

    nome_original = args.url.rstrip("/").split("/")[-1]
    nome_final = args.nome_padronizado or nome_original
    pasta = ORIGINAIS / args.ano
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / nome_final

    temporario = destino.with_suffix(destino.suffix + ".baixando")
    baixar(args.url, temporario)

    if destino.exists():
        if sha256_arquivo(destino) != sha256_arquivo(temporario):
            temporario.unlink()
            print(
                f"ERRO: {destino} já existe com conteúdo DIFERENTE do baixado. "
                "Nada foi sobrescrito — decisão humana necessária.",
                file=sys.stderr,
            )
            return 1
        temporario.unlink()
        print(f"Já existia com o mesmo conteúdo: {destino}")
    else:
        temporario.rename(destino)

    resultado = validar(destino)
    agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    linha = {
        "instituicao": "ITA",
        "ano": args.ano,
        "fase_formato": args.fase_formato,
        "dia": args.dia,
        "materia": args.materia,
        "tipo_material": args.tipo,
        "nome_original": nome_original,
        "nome_padronizado": nome_final,
        "url_pagina_origem": args.pagina_origem,
        "url_arquivo": args.url,
        "fonte": args.fonte,
        "oficial": args.oficial,
        "situacao_autorizacao": args.autorizacao,
        "data_acesso": agora,
        "num_paginas": resultado["num_paginas"] or "",
        "tamanho_bytes": resultado["tamanho_bytes"] or "",
        "sha256": resultado["sha256"] or "",
        "situacao": "encontrado" if resultado["valido"] else "invalido",
        "observacoes": args.observacoes
        or ("; ".join(resultado["erros"]) if resultado["erros"] else ""),
    }
    registrar_linha(linha)
    print(f"{linha['situacao'].upper()}: {destino} ({linha['num_paginas']} págs, "
          f"{linha['tamanho_bytes']} bytes)\nsha256: {linha['sha256']}")
    return 0 if resultado["valido"] else 1


if __name__ == "__main__":
    sys.exit(main())
