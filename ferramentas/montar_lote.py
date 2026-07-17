"""Monta em lote os PDFs finais (Caso 1) e registra no inventário.

Nesta primeira leva: 1ª fase 2019–2026 (prova 100% objetiva + gabarito oficial
completo do ITA). O PDF final = prova + página de proteção + gabarito oficial.

Uso: python montar_lote.py
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from comum import sha256_arquivo
from ingestao import CABECALHO, INVENTARIO, ORIGINAIS
from montar import montar_pdf_final, verificar_fidelidade_visual
from validar_pdf import validar

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "site" / "public" / "pdfs" / "ita"
PAGINA_ORIGEM = "https://www.vestibular.ita.br/provas.htm"

NOTA_REDACAO = {
    "titulo": "OBSERVAÇÃO SOBRE A REDAÇÃO",
    "itens": [{"rotulo": "Redação", "questao": "",
               "resposta": "Não possui resposta única — produção textual."}],
}

# Trabalhos Caso 1: gabarito oficial cobre todas as questões objetivas da prova.
# Cada item: dict com ano, prova, gabarito, nome_final, fase, dia, materia e
# opcionalmente "nota" (página de observação após o gabarito — decisão D11).
TRABALHOS_CASO1 = [
    {"ano": str(ano), "prova": f"{ano}_fase1.pdf", "gabarito": f"gabarito_{ano}.pdf",
     "nome_final": f"ita-{ano}-1-fase-prova-com-gabarito-no-final.pdf",
     "fase": "1ª fase", "dia": "", "materia": ""}
    for ano in range(2019, 2027)
] + [
    {"ano": str(ano), "prova": f"portugues_{ano}_2f.pdf",
     "gabarito": f"gabarito_{ano}_2f.pdf",
     "nome_final": f"ita-{ano}-2-fase-portugues-e-redacao-com-gabarito-no-final.pdf",
     "fase": "2ª fase", "dia": "dia 4", "materia": "Português e Redação",
     "nota": NOTA_REDACAO,
     "obs": "15 questões objetivas cobertas pelo gabarito oficial da 2ª fase; "
            "redação sem resposta única (página de observação)"}
    for ano in (2025, 2026)
]


def ja_registrado(nome_final: str) -> bool:
    with open(INVENTARIO, newline="", encoding="utf-8") as f:
        return any(
            linha["nome_padronizado"] == nome_final
            and linha["tipo_material"] == "pdf_final"
            and linha["situacao"] == "encontrado"
            for linha in csv.DictReader(f)
        )


def registrar_pdf_final(linha: dict) -> None:
    """Substitui o registro do mesmo PDF final, sem duplicar o inventário."""
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
        w = csv.DictWriter(f, fieldnames=CABECALHO, lineterminator="\n")
        w.writeheader()
        w.writerows(existentes)
        w.writerow(linha)
    temporario.replace(INVENTARIO)


def main(regerar: bool = False) -> int:
    hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    falhas = []
    for t in TRABALHOS_CASO1:
        ano, prova, gabarito = t["ano"], t["prova"], t["gabarito"]
        nome_final, fase, materia = t["nome_final"], t["fase"], t["materia"]
        nota = t.get("nota")
        if ja_registrado(nome_final) and not regerar:
            print(f"pulado (já registrado): {nome_final}")
            continue
        caminho_prova = ORIGINAIS / ano / prova
        caminho_gab = ORIGINAIS / ano / gabarito
        pasta_saida = DESTINO / ano
        pasta_saida.mkdir(parents=True, exist_ok=True)
        saida = pasta_saida / nome_final
        try:
            resumo = montar_pdf_final(
                caminho_prova, saida, caso=1, gabarito_oficial=caminho_gab,
                respostas=nota["itens"] if nota else None,
                respostas_titulo=nota["titulo"] if nota else "",
            )
            resultado = validar(saida)
            if not resultado["valido"]:
                raise RuntimeError(f"validação falhou: {resultado['erros']}")
            fidelidade = verificar_fidelidade_visual(caminho_prova, saida)
            ruins = [r for r in fidelidade if not r["ok"]]
            if ruins:
                raise RuntimeError(f"fidelidade visual falhou: {ruins}")
            registrar_pdf_final({
                "instituicao": "ITA", "ano": ano, "fase_formato": fase,
                "dia": t["dia"], "materia": materia, "tipo_material": "pdf_final",
                "nome_original": f"{prova} + protecao + {gabarito}",
                "nome_padronizado": nome_final,
                "url_pagina_origem": PAGINA_ORIGEM, "url_arquivo": "",
                "fonte": "montagem local (prova e gabarito oficiais do ITA)",
                "oficial": "sim", "situacao_autorizacao": "acervo público oficial",
                "data_acesso": hoje,
                "num_paginas": resultado["num_paginas"],
                "tamanho_bytes": resultado["tamanho_bytes"],
                "sha256": resultado["sha256"],
                "situacao": "encontrado",
                "observacoes": f"Caso 1; blocos: {resumo}"
                + (f"; {t['obs']}" if t.get("obs") else ""),
            })
            print(f"OK {nome_final}: {resumo}")
        except Exception as e:
            falhas.append((nome_final, str(e)))
            print(f"FALHA {nome_final}: {e}", file=sys.stderr)
    if falhas:
        print(f"\n{len(falhas)} falha(s)", file=sys.stderr)
        return 1
    print("\nTodos os PDFs finais do lote foram montados e validados.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--regerar", action="store_true",
        help="remonta mesmo os PDFs já registrados e substitui seus registros",
    )
    args = ap.parse_args()
    sys.exit(main(regerar=args.regerar))
