"""Converte o inventário (fonte única da verdade) no catálogo JSON do site.

Uso: python catalogo.py
Lê  docs/coordenacao/INVENTARIO_ITA.csv
Gera site/src/data/catalogo.json
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INVENTARIO = RAIZ / "docs" / "coordenacao" / "INVENTARIO_ITA.csv"
SAIDA = RAIZ / "site" / "src" / "data" / "catalogo.json"


def gerar_catalogo() -> dict:
    anos: dict[str, list[dict]] = defaultdict(list)
    with open(INVENTARIO, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            if linha["instituicao"].strip().upper() != "ITA":
                continue
            anos[linha["ano"].strip()].append(
                {
                    "fase_formato": linha["fase_formato"].strip(),
                    "dia": linha["dia"].strip(),
                    "materia": linha["materia"].strip(),
                    "tipo": linha["tipo_material"].strip(),
                    "arquivo": linha["nome_padronizado"].strip(),
                    "fonte": linha["fonte"].strip(),
                    "oficial": linha["oficial"].strip().lower() in ("sim", "s", "true"),
                    "situacao": linha["situacao"].strip(),
                }
            )
    return {
        "instituicoes": [
            {
                "id": "ita",
                "nome": "ITA",
                "nome_completo": "Instituto Tecnológico de Aeronáutica",
                "anos": {
                    ano: anos[ano]
                    for ano in sorted(anos, key=int, reverse=True)
                },
            }
        ]
    }


if __name__ == "__main__":
    catalogo = gerar_catalogo()
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(
        json.dumps(catalogo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_anos = len(catalogo["instituicoes"][0]["anos"])
    print(f"Catálogo gerado em {SAIDA} ({n_anos} anos)")
