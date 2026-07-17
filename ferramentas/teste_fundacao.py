"""Teste de fumaça da cadeia completa de montagem de PDFs, com material FICTÍCIO.

Nenhum conteúdo real de prova é usado aqui. O teste confirma que:
1. uma "prova" e um "gabarito" fictícios são gerados;
2. o PDF final Caso 1 tem prova + 1 proteção + gabarito, na ordem certa;
3. o PDF final Caso 2 tem prova + 2 proteções + gabarito + respostas;
4. as páginas da prova permanecem visualmente intactas (conferência por renderização);
5. o QR Code embutido na 2ª página de proteção decodifica para a URL exata;
6. o validador aprova os PDFs finais.

Uso: python teste_fundacao.py [dir_saida]
"""

import sys
import tempfile
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from comum import renderizar_pagina
from montar import montar_pdf_final, verificar_fidelidade_visual
from qr import decodificar_qr
from validar_pdf import validar

URL_TESTE = "https://poliedroresolve.sistemapoliedro.com.br/vestibulares/ita"


def _pdf_ficticio(caminho: Path, titulo: str, paginas: int) -> Path:
    c = Canvas(str(caminho), pagesize=A4)
    for i in range(paginas):
        c.setFont("Helvetica", 20)
        c.drawString(100, 700, f"{titulo} — página {i + 1} de {paginas} (FICTÍCIO)")
        c.showPage()
    c.save()
    return caminho


def main(dir_saida: Path) -> None:
    dir_saida.mkdir(parents=True, exist_ok=True)
    prova = _pdf_ficticio(dir_saida / "prova_ficticia.pdf", "PROVA DE TESTE", 3)
    gabarito = _pdf_ficticio(dir_saida / "gabarito_ficticio.pdf", "GABARITO DE TESTE", 1)
    falhas = []

    # Caso 1
    final1 = dir_saida / "teste-caso1-com-gabarito-no-final.pdf"
    r1 = montar_pdf_final(prova, final1, caso=1, gabarito_oficial=gabarito)
    assert r1 == {"prova": 3, "protecao": 1, "gabarito_oficial": 1, "respostas": 0, "total": 5}, r1
    if not validar(final1)["valido"]:
        falhas.append("Caso 1: validação falhou")

    # Caso 2
    final2 = dir_saida / "teste-caso2-com-respostas-no-final.pdf"
    r2 = montar_pdf_final(
        prova, final2, caso=2, gabarito_oficial=gabarito,
        links_poliedro=[{"rotulo": "", "url": URL_TESTE}],
        respostas=[{"questao": "1", "resposta": "12"}, {"questao": "2", "resposta": "x = 3"}],
    )
    assert r2 == {"prova": 3, "protecao": 2, "gabarito_oficial": 1, "respostas": 1, "total": 7}, r2
    if not validar(final2)["valido"]:
        falhas.append("Caso 2: validação falhou")

    # Fidelidade visual das páginas da prova
    for nome, final in (("Caso 1", final1), ("Caso 2", final2)):
        for r in verificar_fidelidade_visual(prova, final):
            if not r["ok"]:
                falhas.append(f"{nome}: página {r['pagina']} divergente ({r['similaridade']:.4f})")

    # QR Code da 2ª página de proteção (página 5 do Caso 2, índice 4)
    img = renderizar_pagina(final2, 4, escala=3.0)
    with tempfile.TemporaryDirectory() as tmp_dir:
        caminho_qr = Path(tmp_dir) / "qr.png"
        img.save(caminho_qr)
        lido = decodificar_qr(caminho_qr)
    if lido != URL_TESTE:
        falhas.append(f"QR: esperado {URL_TESTE!r}, lido {lido!r}")

    if falhas:
        print("FALHAS:")
        for f in falhas:
            print(f" - {f}")
        sys.exit(1)
    print("Teste de fumaça: TODOS OS PASSOS OK")
    print(f" - Caso 1: {r1}")
    print(f" - Caso 2: {r2}")
    print(f" - QR decodificado corretamente: {lido}")


if __name__ == "__main__":
    destino = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    main(destino)
