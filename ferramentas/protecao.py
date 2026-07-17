"""Gera as páginas de proteção e a seção de respostas finais complementares.

Caso 1 (tudo oficial): 1 página de proteção.
Caso 2 (Poliedro usado): 2 páginas de proteção (a segunda com crédito, link legível
e QR Code por matéria) + seção de respostas finais complementares.

As páginas nunca contêm respostas, alternativas, miniaturas ou prévias.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from qr import gerar_qr

LARGURA, ALTURA = A4


def _registrar_fontes_unicode() -> tuple[str, str]:
    """Registra fontes TrueType com símbolos matemáticos e acentos.

    DejaVu Sans existe tanto no Windows usado para a montagem local quanto no
    Ubuntu do GitHub Actions. As fontes Vera do próprio ReportLab são o fallback.
    """
    pasta_reportlab = Path(reportlab.__file__).resolve().parent / "fonts"
    candidatos = [
        (
            Path("C:/Windows/Fonts/DejaVuSans.ttf"),
            Path("C:/Windows/Fonts/DejaVuSans-Bold.ttf"),
        ),
        (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ),
        (pasta_reportlab / "Vera.ttf", pasta_reportlab / "VeraBd.ttf"),
    ]
    for normal, negrito in candidatos:
        if normal.is_file() and negrito.is_file():
            pdfmetrics.registerFont(TTFont("RevisaoSans", str(normal)))
            pdfmetrics.registerFont(TTFont("RevisaoSans-Bold", str(negrito)))
            return "RevisaoSans", "RevisaoSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONTE, FONTE_NEGRITO = _registrar_fontes_unicode()


def _quebrar_texto(texto: str, fonte: str, tamanho: float, largura: float) -> list[str]:
    """Quebra por largura real, inclusive URLs e fórmulas sem espaços."""
    if not texto:
        return [""]

    def largura_de(valor: str) -> float:
        return pdfmetrics.stringWidth(valor, fonte, tamanho)

    def fragmentar(token: str) -> list[str]:
        partes, atual = [], ""
        for caractere in token:
            candidato = atual + caractere
            if atual and largura_de(candidato) > largura:
                partes.append(atual)
                atual = caractere
            else:
                atual = candidato
        if atual:
            partes.append(atual)
        return partes

    linhas, atual = [], ""
    for palavra in texto.split():
        if largura_de(palavra) > largura:
            if atual:
                linhas.append(atual)
                atual = ""
            pedacos = fragmentar(palavra)
            linhas.extend(pedacos[:-1])
            atual = pedacos[-1]
            continue
        candidato = palavra if not atual else f"{atual} {palavra}"
        if largura_de(candidato) <= largura:
            atual = candidato
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def _texto_central(c: Canvas, linhas: list[tuple[str, int]], y_inicial: float) -> float:
    """Desenha linhas centralizadas; cada item é (texto, tamanho da fonte)."""
    y = y_inicial
    for texto, tamanho in linhas:
        c.setFont(FONTE_NEGRITO, tamanho)
        if not texto:
            y -= tamanho * 1.6
            continue
        for linha in _quebrar_texto(texto, FONTE_NEGRITO, tamanho, LARGURA - 3 * cm):
            y -= tamanho * 1.6
            c.drawCentredString(LARGURA / 2, y, linha)
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
    c.setFont(FONTE_NEGRITO, 26)
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
    c.setFont(FONTE, 12)
    for linha in paragrafo:
        c.drawCentredString(LARGURA / 2, y, linha)
        y -= 0.55 * cm
    y -= 0.5 * cm

    lado_qr = 4.5 * cm
    for item in links:
        rotulo, url = item.get("rotulo", ""), item["url"]
        if rotulo:
            c.setFont(FONTE_NEGRITO, 13)
            c.drawCentredString(LARGURA / 2, y, rotulo)
            y -= 0.55 * cm
        c.setFont(FONTE_NEGRITO, 11)
        c.drawCentredString(LARGURA / 2, y, "Link direto:")
        y -= 0.5 * cm
        tamanho_url = 8.5
        c.setFont(FONTE, tamanho_url)
        c.setFillColorRGB(0, 0, 0.7)
        for linha_url in _quebrar_texto(url, FONTE, tamanho_url, LARGURA - 2 * cm):
            largura_linha = pdfmetrics.stringWidth(linha_url, FONTE, tamanho_url)
            x_inicial = (LARGURA - largura_linha) / 2
            c.linkURL(
                url,
                (x_inicial, y - 0.15 * cm, x_inicial + largura_linha, y + 0.3 * cm),
            )
            c.drawString(x_inicial, y, linha_url)
            y -= 0.42 * cm
        c.setFillColorRGB(0, 0, 0)
        y -= 0.25 * cm

        arq_qr = dir_temp / f"qr_{abs(hash(url))}.png"
        gerar_qr(url, arq_qr)
        c.drawImage(
            str(arq_qr), (LARGURA - lado_qr) / 2, y - lado_qr,
            width=lado_qr, height=lado_qr,
        )
        y -= lado_qr + 0.4 * cm
        c.setFont(FONTE, 10)
        c.drawCentredString(
            LARGURA / 2, y, "Aponte a câmera do celular para o QR Code acima."
        )
        y -= 1.0 * cm
    c.showPage()


TITULO_RESPOSTAS_POLIEDRO = "RESPOSTAS FINAIS COMPLEMENTARES - FONTE: POLIEDRO RESOLVE"


def paginas_respostas_complementares(
    c: Canvas, respostas: list[dict], titulo: str = TITULO_RESPOSTAS_POLIEDRO
) -> None:
    """Seção de respostas/observações após o gabarito.

    respostas: lista de {"questao": "1", "resposta": "12"} já transcritas e
    conferidas a partir da fonte (nunca redigidas pelo agente). Um item pode
    trazer "rotulo" (ex.: "Redação") no lugar do prefixo "Questão N".
    """
    y = ALTURA - 2.5 * cm
    tamanho_titulo = 14
    c.setFont(FONTE_NEGRITO, tamanho_titulo)
    for linha_titulo in _quebrar_texto(
        titulo, FONTE_NEGRITO, tamanho_titulo, LARGURA - 3 * cm
    ):
        c.drawCentredString(LARGURA / 2, y, linha_titulo)
        y -= 0.58 * cm
    y -= 0.35 * cm
    tamanho_texto = 12
    entrelinha = 0.58 * cm
    c.setFont(FONTE, tamanho_texto)
    for item in respostas:
        prefixo = item.get("rotulo") or f"Questão {item['questao']}"
        texto = f"{prefixo}: {item['resposta']}"
        linhas_item = _quebrar_texto(texto, FONTE, tamanho_texto, LARGURA - 4.4 * cm)
        altura_item = len(linhas_item) * entrelinha + 0.22 * cm
        if y - altura_item < 2.2 * cm:
            c.showPage()
            y = ALTURA - 2.5 * cm
            c.setFont(FONTE, tamanho_texto)
        for linha in linhas_item:
            c.drawString(2.2 * cm, y, linha)
            y -= entrelinha
        y -= 0.22 * cm
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
