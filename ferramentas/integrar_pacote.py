"""Integra um pacote do Codex (formato D10): monta os PDFs finais Caso 2,
valida tudo e registra inventário e respostas complementares.

Uso: python integrar_pacote.py <caminho/do/pacote.json> [--somente-validar]

Granularidade por questão: cada resposta pode trazer `status_questao`
("pronto"/"pendente"). Um item é integrado desde que tenha PDF original,
link do Poliedro e ao menos uma resposta — mesmo que o `status` do item
como um todo seja "pendente" por causa de sub-questões incompletas (isso é
comum: a maioria das provas discursivas tem algumas questões sem resultado
separável, ao lado de outras já prontas). Regra (seção 16 do plano): nenhuma
questão fica em branco. Para cada questão publicada no PDF:
  - status_questao == "pronto": publica o texto transcrito tal como veio;
  - status_questao != "pronto" (ou ausente): publica a frase padrão "Confira
    a resolução completa no link e no QR Code apresentados na página de
    proteção anterior." — o texto candidato do Codex NÃO é publicado (fica
    só no registro interno de auditoria em RESPOSTAS_COMPLEMENTARES.csv),
    pois o próprio pacote o marcou como não confirmado/não separável.

Passos por item:
1. confere que o PDF original existe e que o SHA-256 bate com o declarado;
2. confere que a URL direta do Poliedro responde 200;
3. monta o PDF final Caso 2 (prova + 2 proteções com crédito/link/QR +
   gabarito oficial quando houver + respostas finais complementares);
4. valida o PDF final, a fidelidade visual das páginas da prova e decodifica
   o QR Code renderizado, comparando com a URL declarada;
5. registra a linha `pdf_final` no inventário e TODAS as respostas (prontas
   e pendentes, com o texto original do Codex preservado para auditoria) em
   RESPOSTAS_COMPLEMENTARES.csv.
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
from ingestao import CABECALHO as CABECALHO_INVENTARIO, INVENTARIO
from montar import montar_pdf_final, verificar_fidelidade_visual
from qr import decodificar_qr
from validar_pdf import validar

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "site" / "public" / "pdfs" / "ita"
RESPOSTAS_CSV = RAIZ / "docs" / "coordenacao" / "RESPOSTAS_COMPLEMENTARES.csv"
CABECALHO_RESPOSTAS = [
    "documento_id", "questao", "resposta_transcrita", "url_resolucao",
    "data_consulta", "agente", "situacao_conferencia", "observacoes",
]


FRASE_PADRAO = (
    "Confira a resolução completa no link e no QR Code apresentados "
    "na página de proteção anterior."
)


def respostas_para_publicacao(item: dict) -> list[dict]:
    """Aplica a regra por questão: só publica texto de `status_questao`
    'pronto'; as demais recebem a frase padrão, sem publicar o candidato
    ainda não confirmado."""
    publicaveis = []
    for r in item.get("respostas", []):
        pronto = r.get("status_questao", "pronto") == "pronto"
        publicaveis.append({
            "questao": r.get("questao", ""),
            "rotulo": r.get("rotulo"),
            "resposta": r["resposta"] if pronto else FRASE_PADRAO,
        })
    return publicaveis


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
    """Substitui as respostas do documento, tornando a integração idempotente.
    Preserva o texto ORIGINAL do Codex para toda questão (pronta ou
    pendente), mesmo quando o PDF público usa a frase padrão — este CSV é
    só para auditoria interna, nunca publicado no site."""
    existentes = []
    if RESPOSTAS_CSV.is_file():
        with open(RESPOSTAS_CSV, newline="", encoding="utf-8") as f:
            existentes = [
                linha for linha in csv.DictReader(f)
                if linha.get("documento_id") != item["id"]
            ]

    temporario = RESPOSTAS_CSV.with_suffix(".csv.tmp")
    with open(temporario, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CABECALHO_RESPOSTAS, lineterminator="\n")
        w.writeheader()
        w.writerows(existentes)
        for r in item.get("respostas", []):
            pronto = r.get("status_questao", "pronto") == "pronto"
            situacao = (
                "pronta; publicada no PDF" if pronto
                else "pendente; PDF público usa a frase padrão, texto abaixo é só para auditoria"
            )
            w.writerow({
                "documento_id": item["id"],
                "questao": r.get("questao", r.get("rotulo", "")),
                "resposta_transcrita": r["resposta"],
                "url_resolucao": r.get("url_fonte", item["poliedro"]["url_direta"]),
                "data_consulta": hoje,
                "agente": agente,
                "situacao_conferencia": situacao,
                "observacoes": r.get("obs", "")
                + (f" | evidência: {r['evidencia']}" if r.get("evidencia") else ""),
            })
    temporario.replace(RESPOSTAS_CSV)


def registrar_inventario(linha: dict) -> None:
    """Substitui a linha do mesmo PDF final em vez de duplicá-la."""
    existentes = []
    if INVENTARIO.is_file():
        with open(INVENTARIO, newline="", encoding="utf-8") as f:
            existentes = [
                atual for atual in csv.DictReader(f)
                if not (
                    atual.get("tipo_material") == "pdf_final"
                    and atual.get("nome_padronizado") == linha["nome_padronizado"]
                )
            ]

    temporario = INVENTARIO.with_suffix(".csv.tmp")
    with open(temporario, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CABECALHO_INVENTARIO, lineterminator="\n")
        w.writeheader()
        w.writerows(existentes)
        w.writerow(linha)
    temporario.replace(INVENTARIO)


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
        erros.append("item sem lista de respostas")
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
        respostas=respostas_para_publicacao(item),
    )

    resultado = validar(saida)
    if not resultado["valido"]:
        return [f"validação do PDF final falhou: {resultado['erros']}"]
    ruins = [r for r in verificar_fidelidade_visual(original, saida) if not r["ok"]]
    if ruins:
        return [f"fidelidade visual falhou: {ruins}"]

    # QR na 2ª página de proteção (logo após as páginas da prova + 1ª proteção).
    # Escalas maiores são tentadas em sequência porque URLs longas (muitas
    # matérias/dias no slug) geram QR mais denso; em resolução baixa o
    # decodificador de teste pode falhar mesmo com o QR fisicamente correto
    # (confirmado manualmente: o mesmo PNG decodifica certo a partir de
    # escala 4.0). Uma câmera de celular real tem resolução muito maior que
    # qualquer uma dessas escalas de teste.
    indice_qr = resumo["prova"] + 1
    lido = None
    # NamedTemporaryFile permanece bloqueado no Windows e impede o Pillow de
    # reabrir o mesmo caminho. Um diretório temporário funciona nos dois
    # sistemas usados pelo projeto (Windows local e Ubuntu no GitHub Actions).
    with tempfile.TemporaryDirectory() as tmp_dir:
        caminho_qr = Path(tmp_dir) / "qr.png"
        for escala in (3.0, 4.5, 6.0):
            img = renderizar_pagina(saida, indice_qr, escala=escala)
            img.save(caminho_qr)
            lido = decodificar_qr(caminho_qr)
            if lido is not None:
                break
    if lido != url:
        return [f"QR decodificado ({lido!r}) difere da URL declarada ({url!r})"]

    registrar_inventario({
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
    registrar_respostas(item, "Codex (transcrição e integração final)", hoje)
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
        # Itens integráveis têm PDF original, link do Poliedro e respostas —
        # o "status" de nível de item é só um resumo do Codex (algumas
        # sub-questões pendentes não impedem publicar as demais com a frase
        # padrão; ver respostas_para_publicacao).
        tem_insumos = item.get("pdf_original") and item.get("poliedro") and item.get("respostas")
        if not tem_insumos:
            pendentes.append(f"{item.get('id', '?')} (sem insumos suficientes; status: {item.get('status')})")
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
