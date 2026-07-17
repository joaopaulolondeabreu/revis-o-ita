"""Gera as páginas de proteção e a seção de respostas finais complementares.

Caso 1 (tudo oficial): 1 página de proteção.
Caso 2 (Poliedro usado): 2 páginas de proteção (a segunda com crédito, link legível
e QR Code por matéria) + seção de respostas finais complementares.

As páginas nunca contêm respostas, alternativas, miniaturas ou prévias.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from qr import gerar_qr

LARGURA, ALTURA = A4


def _texto_central(c: Canvas, linhas: list[tuple[str, int]], y_inicial: float) -> float:
    """Desenha linhas centralizadas; cada item é (texto, tamanho da fonte)."""
    y = y_inicial
    for texto, tamanho in linhas:
        c.setFont("Helvetica-Bold", tamanho)
        y -= tamanho * 1.6
        c.drawCentredString(LARGURA / 2, y, texto)
    return y


def pagina_protecao_fim_da_prova(c: Canvas, gabarito_na_proxima: bool) -> None:
    if gabarito_na_proxima:
        ultima = "O GABARITO COMEÇA NA PRÓXIMA PÁGINA."
    else:
        ultima = "INFORMAÇÕES SOBRE O GABARITO E AS RESOLUÇÕES"
    linhas = [
        ("FIM DA PROVA", 40),
        ("", 12),
        ("PARE AQUI SE AINDA NÃO QUISER", 24),
        ("VER AS RESPOSTAS.", 24),
        ("", 12),
        (ultima, 22),
    ]
    if not gabarito_na_proxima:
        linhas.append(("COMEÇAM NA PRÓXIMA PÁGINA.", 22))
    _texto_central(c, linhas, ALTURA - 6 * cm)
    c.showPage()


def pagina_protecao_creditos(c: Canvas, links: list[dict], dir_temp: Path) -> None:
    """Segunda página de proteção (Caso 2).

    links: lista de {"rotulo": "Matemática" | "" (prova única), "url": "..."}.
    Cada link recebe URL escrita legível e QR Code apontando para o MESMO endereço.
    """
    y = ALTURA - 2.5 * cm
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(LARGURA / 2, y, "RESOLUÇÕES COMPLETAS")
    y -= 1.4 * cm

    paragrafo = [
        "O gabarito oficial do ITA e as respostas finais disponíveis serão",
        "apresentados nas páginas seguintes.",
        "As respostas finais complementares foram conferidas no Poliedro Resolve.",
        "Para consultar e baixar as resoluções completas das questões discursivas,",
        "acesse o material correspondente no Poliedro Resolve.",
        "Créditos das resoluções: Poliedro Resolve.",
        "As resoluções completas pertencem ao Poliedro Resolve.",
    ]
    c.setFont("Helvetica", 12)
    for linha in paragrafo:
        c.drawCentredString(LARGURA / 2, y, linha)
        y -= 0.55 * cm
    y -= 0.5 * cm

    lado_qr = 4.5 * cm
    for item in links:
        rotulo, url = item.get("rotulo", ""), item["url"]
        if rotulo:
            c.setFont("Helvetica-Bold", 13)
            c.drawCentredString(LARGURA / 2, y, rotulo)
            y -= 0.55 * cm
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(LARGURA / 2, y, "Link direto:")
        y -= 0.5 * cm
        c.setFont("Helvetica", 10)
        c.linkURL(url, (1 * cm, y - 0.2 * cm, LARGURA - 1 * cm, y + 0.35 * cm))
        c.setFillColorRGB(0, 0, 0.7)
        c.drawCentredString(LARGURA / 2, y, url)
        c.setFillColorRGB(0, 0, 0)
        y -= 0.7 * cm

        arq_qr = dir_temp / f"qr_{abs(hash(url))}.png"
        gerar_qr(url, arq_qr)
        c.drawImage(
            str(arq_qr), (LARGURA - lado_qr) / 2, y - lado_qr,
            width=lado_qr, height=lado_qr,
        )
        y -= lado_qr + 0.4 * cm
        c.setFont("Helvetica", 10)
        c.drawCentredString(
            LARGURA / 2, y, "Aponte a câmera do celular para o QR Code acima."
        )
        y -= 1.0 * cm
    c.showPage()


TITULO_RESPOSTAS_POLIEDRO = "RESPOSTAS FINAIS COMPLEMENTARES — FONTE: POLIEDRO RESOLVE"


def paginas_respostas_complementares(
    c: Canvas, respostas: list[dict], titulo: str = TITULO_RESPOSTAS_POLIEDRO
) -> None:
    """Seção de respostas/observações após o gabarito.

    respostas: lista de {"questao": "1", "resposta": "12"} já transcritas e
    conferidas a partir da fonte (nunca redigidas pelo agente). Um item pode
    trazer "rotulo" (ex.: "Redação") no lugar do prefixo "Questão N".
    """
    y = ALTURA - 2.5 * cm
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(LARGURA / 2, y, titulo)
    y -= 1.2 * cm
    c.setFont("Helvetica", 13)
    for item in respostas:
        prefixo = item.get("rotulo") or f"Questão {item['questao']}"
        texto = f"{prefixo}: {item['resposta']}"
        c.drawString(2.5 * cm, y, texto)
        y -= 0.8 * cm
        if y < 2.5 * cm:
            c.showPage()
            y = ALTURA - 2.5 * cm
            c.setFont("Helvetica", 13)
    c.showPage()


def gerar_pdf_protecao(
    saida: Path,
    caso: int,
    links_poliedro: list[dict] | None = None,
) -> Path:
    """Gera o PDF intermediário com a(s) página(s) de proteção."""
    c = Canvas(str(saida), pagesize=A4)
    if caso == 1:
        pagina_protecao_fim_da_prova(c, gabarito_na_proxima=True)
    elif caso == 2:
        if not links_poliedro:
            raise ValueError("Caso 2 exige ao menos um link direto do Poliedro")
        pagina_protecao_fim_da_prova(c, gabarito_na_proxima=False)
        with TemporaryDirectory() as dir_temp:
            pagina_protecao_creditos(c, links_poliedro, Path(dir_temp))
    else:
        raise ValueError("caso deve ser 1 ou 2")
    c.save()
    return saida


def gerar_pdf_respostas(
    saida: Path, respostas: list[dict], titulo: str = TITULO_RESPOSTAS_POLIEDRO
) -> Path:
    c = Canvas(str(saida), pagesize=A4)
    paginas_respostas_complementares(c, respostas, titulo)
    c.save()
    return saida
