"""Monta em lote os PDFs finais (Caso 1) e registra no inventário.

Nesta primeira leva: 1ª fase 2019–2026 (prova 100% objetiva + gabarito oficial
completo do ITA). O PDF final = prova + página de proteção + gabarito oficial.

Uso: python montar_lote.py
"""

import csv
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from comum import sha256_arquivo
from ingestao import CABECALHO, INVENTARIO, ORIGINAIS, registrar_linha
from montar import montar_pdf_final, verificar_fidelidade_visual
from validar_pdf import validar

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "site" / "public" / "pdfs" / "ita"
PAGINA_ORIGEM = "https://www.vestibular.ita.br/provas.htm"

# (ano, prova, gabarito, nome_final, fase, materia)
TRABALHOS_CASO1 = [
    (str(ano), f"{ano}_fase1.pdf", f"gabarito_{ano}.pdf",
     f"ita-{ano}-1-fase-prova-com-gabarito-no-final.pdf", "1ª fase", "")
    for ano in range(2019, 2027)
]


def ja_registrado(nome_final: str) -> bool:
    with open(INVENTARIO, newline="", encoding="utf-8") as f:
        return any(
            linha["nome_padronizado"] == nome_final
            and linha["tipo_material"] == "pdf_final"
            and linha["situacao"] == "encontrado"
            for linha in csv.DictReader(f)
        )


def main() -> int:
    hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    falhas = []
    for ano, prova, gabarito, nome_final, fase, materia in TRABALHOS_CASO1:
        if ja_registrado(nome_final):
            print(f"pulado (já registrado): {nome_final}")
            continue
        caminho_prova = ORIGINAIS / ano / prova
        caminho_gab = ORIGINAIS / ano / gabarito
        pasta_saida = DESTINO / ano
        pasta_saida.mkdir(parents=True, exist_ok=True)
        saida = pasta_saida / nome_final
        try:
            resumo = montar_pdf_final(
                caminho_prova, saida, caso=1, gabarito_oficial=caminho_gab
            )
            resultado = validar(saida)
            if not resultado["valido"]:
                raise RuntimeError(f"validação falhou: {resultado['erros']}")
            fidelidade = verificar_fidelidade_visual(caminho_prova, saida)
            ruins = [r for r in fidelidade if not r["ok"]]
            if ruins:
                raise RuntimeError(f"fidelidade visual falhou: {ruins}")
            registrar_linha({
                "instituicao": "ITA", "ano": ano, "fase_formato": fase,
                "dia": "", "materia": materia, "tipo_material": "pdf_final",
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
                "observacoes": f"Caso 1; blocos: {resumo}",
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
    sys.exit(main())
