"""Relatório resumido do inventário: contagem por situação e por ano.

Uso: python relatorio.py
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

INVENTARIO = Path(__file__).resolve().parent.parent / "docs" / "coordenacao" / "INVENTARIO_ITA.csv"


def main() -> None:
    por_situacao = Counter()
    por_ano = defaultdict(Counter)
    with open(INVENTARIO, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            situacao = linha["situacao"].strip() or "(sem situação)"
            por_situacao[situacao] += 1
            por_ano[linha["ano"].strip()][situacao] += 1

    print("== Por situação ==")
    for situacao, n in por_situacao.most_common():
        print(f"  {situacao}: {n}")

    print("\n== Por ano ==")
    for ano in sorted(por_ano, reverse=True):
        detalhe = ", ".join(f"{s}: {n}" for s, n in sorted(por_ano[ano].items()))
        print(f"  {ano}: {detalhe}")

    pendencias = [
        s for s in por_situacao
        if s not in ("encontrado",) and por_situacao[s] > 0
    ]
    if pendencias:
        print("\nAtenção: existem itens fora de 'encontrado' — ver inventário.")


if __name__ == "__main__":
    main()
