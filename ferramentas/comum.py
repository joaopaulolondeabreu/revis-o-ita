"""Funções compartilhadas pelas ferramentas do projeto."""

import hashlib
from pathlib import Path

import pypdfium2 as pdfium


def sha256_arquivo(caminho: str | Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def renderizar_pagina(caminho_pdf: str | Path, indice: int, escala: float = 2.0):
    """Renderiza uma página do PDF como imagem PIL (para conferência visual e testes)."""
    pdf = pdfium.PdfDocument(str(caminho_pdf))
    try:
        pagina = pdf[indice]
        return pagina.render(scale=escala).to_pil()
    finally:
        pdf.close()


def numero_paginas(caminho_pdf: str | Path) -> int:
    pdf = pdfium.PdfDocument(str(caminho_pdf))
    try:
        return len(pdf)
    finally:
        pdf.close()
