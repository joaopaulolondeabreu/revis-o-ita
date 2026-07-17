# URLs candidatas (descobertas por busca na web — AINDA NÃO VERIFICADAS)

**Atenção:** tudo nesta página foi encontrado por busca na web em 2026-07-16/17
(America/Sao_Paulo), pois a rede do ambiente ainda bloqueia o acesso direto às
fontes. **Nenhuma URL daqui entra no inventário como `encontrado` sem download
direto, validação e hash.** Padrões podem variar entre anos.

## Acervo oficial do ITA — padrões observados

Base: `https://www.vestibular.ita.br/provas/`

| Material | Padrão observado | Exemplos confirmados pela busca |
|---|---|---|
| Prova 1ª fase | `<ano>_fase1.pdf` | `2026_fase1.pdf`, `2025_fase1.pdf`, `2024_fase1.pdf`, `2023_fase1.pdf`, `2021_fase1.pdf` |
| Prova 2ª fase por matéria | `<materia>_<ano>_2f.pdf` | `portugues_2026_2f.pdf` |
| Gabarito (geral/1ª fase ou por matéria) | `gabarito_<ano>.pdf` | `gabarito_2026.pdf`, `gabarito_2025.pdf`, `gabarito_2024.pdf`, `gabarito_2023.pdf`, `gabarito_2012.pdf` |
| Gabarito 2ª fase | `gabarito_<ano>_2fase.pdf` | `gabarito_2025_2fase.pdf` |

Conclusões provisórias (a confirmar no acesso direto):
- O acervo oficial cobre pelo menos até **2012** (existe `gabarito_2012.pdf`), coerente com a estimativa "2008–2026".
- A página índice é `https://www.vestibular.ita.br/provas.htm` — mapear a lista completa por lá, não por adivinhação de padrões.

## Poliedro Resolve — estrutura observada

- Página do ITA: `https://poliedroresolve.sistemapoliedro.com.br/vestibulares/ita`
- Estrutura por prova/questão observada:
  `…/vestibulares/ita/<ano>/<slug-da-prova>/<slug-da-questao>`
  (ex.: `…/vestibulares/ita/2026/ita-1-fase-05-10-2025-1-fase/questao-1-matematica-1-fase-ita-2026`)
- Indício de que existe uma **página por prova** (`…/ita/<ano>/<slug-da-prova>/`) — candidata ideal para o link direto + QR Code. Confirmar se ela permite baixar a resolução daquela prova.

## Fontes terciárias vistas na busca (usar só como último recurso, com registro de autorização)

- `cosseno.com/provas-anteriores/ITA`
- `quimicaparaovestibular.com.br` e `sotaodaquimica.com.br` (afirmam colaboração com COMAER/ITA)
- `projetoagathaedu.com.br` (anos ~2010–2023)

Para 2002–2007: priorizar fonte oficial ou cópia pública confiável da própria prova (regra D7 em DECISOES.md).
