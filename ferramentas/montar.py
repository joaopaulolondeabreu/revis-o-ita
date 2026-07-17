"""Monta o PDF final de uma prova: prova original + proteção(ões) + gabarito
oficial + respostas complementares, nesta ordem.

As páginas da prova e do gabarito oficial são anexadas como estão, sem
redigitação nem alteração de conteúdo. A fidelidade visual é conferida por
renderização (ver verificar_fidelidade_visual).

Uso programático: montar_pdf_final(...). Ver teste_fundacao.py para exemplo.
"""

from pathlib import Path

import numpy as np
from pypdf import PdfReader, PdfWriter

from comum import numero_paginas, renderizar_pagina
from protecao import TITULO_RESPOSTAS_POLIEDRO, gerar_pdf_protecao, gerar_pdf_respostas


def montar_pdf_final(
    prova: Path,
    saida: Path,
    caso: int,
    gabarito_oficial: Path | None = None,
    links_poliedro: list[dict] | None = None,
    respostas: list[dict] | None = None,
    respostas_titulo: str = TITULO_RESPOSTAS_POLIEDRO,
) -> dict:
    """Monta o PDF final e devolve um resumo com a contagem de páginas por bloco."""
    escritor = PdfWriter()
    resumo = {"prova": 0, "protecao": 0, "gabarito_oficial": 0, "respostas": 0}

    leitor_prova = PdfReader(str(prova))
    for pagina in leitor_prova.pages:
        escritor.add_page(pagina)
    resumo["prova"] = len(leitor_prova.pages)

    pdf_protecao = saida.parent / f"_protecao_{saida.stem}.pdf"
    gerar_pdf_protecao(pdf_protecao, caso, links_poliedro)
    leitor_prot = PdfReader(str(pdf_protecao))
    for pagina in leitor_prot.pages:
        escritor.add_page(pagina)
    resumo["protecao"] = len(leitor_prot.pages)

    if gabarito_oficial is not None:
        leitor_gab = PdfReader(str(gabarito_oficial))
        for pagina in leitor_gab.pages:
            escritor.add_page(pagina)
        resumo["gabarito_oficial"] = len(leitor_gab.pages)

    if respostas:
        pdf_resp = saida.parent / f"_respostas_{saida.stem}.pdf"
        gerar_pdf_respostas(pdf_resp, respostas, respostas_titulo)
        leitor_resp = PdfReader(str(pdf_resp))
        for pagina in leitor_resp.pages:
            escritor.add_page(pagina)
        resumo["respostas"] = len(leitor_resp.pages)
        pdf_resp.unlink()

    with open(saida, "wb") as f:
        escritor.write(f)
    pdf_protecao.unlink()

    resumo["total"] = numero_paginas(saida)
    esperado = sum(v for k, v in resumo.items() if k != "total")
    if resumo["total"] != esperado:
        raise RuntimeError(
            f"contagem de páginas inconsistente: esperado {esperado}, obtido {resumo['total']}"
        )
    return resumo


def verificar_fidelidade_visual(
    original: Path, final: Path, escala: float = 1.5, limiar: float = 0.995
) -> list[dict]:
    """Compara por renderização cada página da prova original com a página
    correspondente do PDF final (as N primeiras). Devolve a similaridade por página.

    limiar: fração mínima de pixels idênticos (tolerância pequena para
    diferenças de compressão interna; o conteúdo visual deve ser o mesmo).
    """
    n = numero_paginas(original)
    resultados = []
    for i in range(n):
        img_a = renderizar_pagina(original, i, escala).convert("L")
        img_b = renderizar_pagina(final, i, escala).convert("L")
        if img_a.size != img_b.size:
            img_b = img_b.resize(img_a.size)
        a = np.asarray(img_a, dtype=np.int16)
        b = np.asarray(img_b, dtype=np.int16)
        iguais = float(np.mean(np.abs(a - b) <= 4))
        resultados.append({"pagina": i + 1, "similaridade": iguais, "ok": iguais >= limiar})
    return resultados
