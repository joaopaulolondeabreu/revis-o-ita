"""Valida um PDF: assinatura, abertura, páginas renderizáveis, hash e tamanho.

Uso: python validar_pdf.py <arquivo.pdf> [--paginas-esperadas N]
Saída: JSON com os resultados; código de saída 0 se válido, 1 se inválido.
"""

import argparse
import json
import sys
from pathlib import Path

import pypdfium2 as pdfium

from comum import sha256_arquivo


def validar(caminho: Path, paginas_esperadas: int | None = None) -> dict:
    resultado = {
        "arquivo": str(caminho),
        "valido": False,
        "erros": [],
        "num_paginas": None,
        "tamanho_bytes": None,
        "sha256": None,
    }
    if not caminho.is_file():
        resultado["erros"].append("arquivo não existe")
        return resultado

    resultado["tamanho_bytes"] = caminho.stat().st_size
    if resultado["tamanho_bytes"] == 0:
        resultado["erros"].append("arquivo vazio")
        return resultado

    with open(caminho, "rb") as f:
        if not f.read(1024).lstrip().startswith(b"%PDF-"):
            resultado["erros"].append("não é um PDF verdadeiro (assinatura %PDF- ausente)")
            return resultado

    resultado["sha256"] = sha256_arquivo(caminho)

    try:
        pdf = pdfium.PdfDocument(str(caminho))
    except Exception as e:
        resultado["erros"].append(f"não abre: {e}")
        return resultado

    try:
        n = len(pdf)
        resultado["num_paginas"] = n
        if n == 0:
            resultado["erros"].append("PDF sem páginas")
        # Renderiza todas as páginas para detectar corrupção.
        for i in range(n):
            try:
                pdf[i].render(scale=0.5)
            except Exception as e:
                resultado["erros"].append(f"página {i + 1} não renderiza: {e}")
        if paginas_esperadas is not None and n != paginas_esperadas:
            resultado["erros"].append(
                f"esperava {paginas_esperadas} páginas, encontrou {n}"
            )
    finally:
        pdf.close()

    resultado["valido"] = not resultado["erros"]
    return resultado


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", type=Path)
    ap.add_argument("--paginas-esperadas", type=int, default=None)
    args = ap.parse_args()
    r = validar(args.arquivo, args.paginas_esperadas)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(0 if r["valido"] else 1)
