"""Integra um pacote do Codex (formato D10): monta os PDFs finais Caso 2,
valida tudo e registra inventário e respostas complementares.

Uso: python integrar_pacote.py <caminho/do/pacote.json> [--somente-validar]

Para cada item com status "pronto":
1. confere que o PDF original existe e que o SHA-256 bate com o declarado;
2. confere que a URL direta do Poliedro responde 200;
3. monta o PDF final Caso 2 (prova + 2 proteções com crédito/link/QR +
   gabarito oficial quando houver + respostas finais complementares);
4. valida o PDF final, a fidelidade visual das páginas da prova e decodifica
   o QR Code renderizado, comparando com a URL declarada;
5. registra a linha `pdf_final` no inventário e as respostas em
   RESPOSTAS_COMPLEMENTARES.csv.

Itens com status diferente de "pronto" são apenas listados como pendências.
"""

import argparse
import csv
import json
import sys
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from comum import renderizar_pagina, sha256_arquivo
from ingestao import INVENTARIO, registrar_linha
from montar import montar_pdf_final, verificar_fidelidade_visual
from qr import decodificar_qr
from validar_pdf import validar

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "site" / "public" / "pdfs" / "ita"
RESPOSTAS_CSV = RAIZ / "docs" / "coordenacao" / "RESPOSTAS_COMPLEMENTARES.csv"


def url_responde(url: str) -> bool:
    try:
        req = urllib.request.Request(
            url.split("#")[0], headers={"User-Agent": "Mozilla/5.0 (verificacao de link)"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status == 200
    except Exception:
        return False


def registrar_respostas(item: dict, agente: str, hoje: str) -> None:
    with open(RESPOSTAS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for r in item.get("respostas", []):
            w.writerow([
                item["id"], r.get("questao", r.get("rotulo", "")), r["resposta"],
                r.get("url_fonte", item["poliedro"]["url_direta"]), hoje, agente,
                "transcrita pelo Codex; integrada por Claude",
                r.get("obs", "") + (f" | evidência: {r['evidencia']}" if r.get("evidencia") else ""),
            ])


def integrar_item(item: dict, hoje: str, somente_validar: bool) -> list[str]:
    """Devolve a lista de erros (vazia = sucesso)."""
    erros = []
    original = RAIZ / item["pdf_original"]
    if not original.is_file():
        return [f"PDF original não existe: {original}"]
    if item.get("sha256_original"):
        if sha256_arquivo(original) != item["sha256_original"]:
            return ["SHA-256 do original diverge do declarado no pacote"]

    gabarito = None
    if item.get("gabarito_oficial"):
        gabarito = RAIZ / item["gabarito_oficial"]
        if not gabarito.is_file():
            return [f"gabarito oficial não existe: {gabarito}"]

    url = item["poliedro"]["url_direta"]
    if not url_responde(url):
        erros.append(f"URL direta do Poliedro não respondeu 200: {url}")

    if not item.get("respostas"):
        erros.append("item 'pronto' sem lista de respostas")
    if erros:
        return erros

    if somente_validar:
        return []

    nome_final = item.get(
        "nome_final", f"{item['id']}-com-respostas-no-final.pdf"
    )
    pasta = DESTINO / item["ano"]
    pasta.mkdir(parents=True, exist_ok=True)
    saida = pasta / nome_final

    rotulo_link = item.get("materia", "")
    resumo = montar_pdf_final(
        original, saida, caso=2, gabarito_oficial=gabarito,
        links_poliedro=[{"rotulo": rotulo_link, "url": url}],
        respostas=item["respostas"],
    )

    resultado = validar(saida)
    if not resultado["valido"]:
        return [f"validação do PDF final falhou: {resultado['erros']}"]
    ruins = [r for r in verificar_fidelidade_visual(original, saida) if not r["ok"]]
    if ruins:
        return [f"fidelidade visual falhou: {ruins}"]

    # QR na 2ª página de proteção (logo após as páginas da prova + 1ª proteção).
    indice_qr = resumo["prova"] + 1
    img = renderizar_pagina(saida, indice_qr, escala=3.0)
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        img.save(tmp.name)
        lido = decodificar_qr(Path(tmp.name))
    if lido != url:
        return [f"QR decodificado ({lido!r}) difere da URL declarada ({url!r})"]

    registrar_linha({
        "instituicao": "ITA", "ano": item["ano"],
        "fase_formato": item.get("fase", ""), "dia": item.get("dia", ""),
        "materia": item.get("materia", ""), "tipo_material": "pdf_final",
        "nome_original": f"{original.name} + protecoes + "
                         f"{gabarito.name if gabarito else 'sem gabarito oficial'} + respostas",
        "nome_padronizado": nome_final,
        "url_pagina_origem": item.get("url_pagina_origem", ""),
        "url_arquivo": "", "fonte": "montagem local (Caso 2, respostas conferidas no Poliedro Resolve)",
        "oficial": "sim" if gabarito else "nao",
        "situacao_autorizacao": "prova oficial + resultados finais mínimos com crédito ao Poliedro",
        "data_acesso": hoje,
        "num_paginas": resultado["num_paginas"],
        "tamanho_bytes": resultado["tamanho_bytes"],
        "sha256": resultado["sha256"],
        "situacao": "encontrado",
        "observacoes": f"Caso 2; blocos: {resumo}; link direto: {url}",
    })
    registrar_respostas(item, "Codex (transcrição) / Claude (integração)", hoje)
    print(f"OK {nome_final}: {resumo}")
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pacote", type=Path)
    ap.add_argument("--somente-validar", action="store_true")
    args = ap.parse_args()

    pacote = json.loads(args.pacote.read_text(encoding="utf-8"))
    hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    falhas, pendentes, ok = [], [], 0

    for item in pacote.get("itens", []):
        if item.get("status") != "pronto":
            pendentes.append(f"{item.get('id', '?')} (status: {item.get('status')})")
            continue
        erros = integrar_item(item, hoje, args.somente_validar)
        if erros:
            falhas.append((item["id"], erros))
        else:
            ok += 1

    print(f"\nPacote {pacote.get('pacote')}: {ok} item(ns) OK, "
          f"{len(falhas)} falha(s), {len(pendentes)} pendente(s)")
    for id_, erros in falhas:
        print(f"  FALHA {id_}:")
        for e in erros:
            print(f"    - {e}")
    for p in pendentes:
        print(f"  pendente: {p}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
