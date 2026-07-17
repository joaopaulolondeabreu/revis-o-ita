# Revisão ITA

Site de estudos gratuito, sem anúncios e sem login, com as provas do vestibular do ITA (2002–2026) e seus gabaritos oficiais, reunidos em um único PDF por prova — com as respostas sempre **no final**, depois de página(s) de proteção.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `docs/coordenacao/` | Documentação de coordenação entre agentes (Claude e Codex), inventário e fontes |
| `ferramentas/` | Scripts Python de validação, montagem de PDFs, páginas de proteção e QR Codes |
| `arquivos/originais/` | PDFs de origem, intactos, com SHA-256 registrado no inventário |
| `site/` | Site estático (Astro) gerado a partir do catálogo |

## Regras centrais

1. Um único PDF principal por prova; o nome do arquivo informa que o gabarito está no final.
2. Páginas da prova original visualmente intactas — sem corte, redigitação ou alteração de conteúdo, com conferência por renderização.
3. Gabarito oficial do ITA sempre tem prioridade e é anexado integralmente.
4. Do Poliedro Resolve, somente resultados finais explícitos de discursivas não cobertas oficialmente, com crédito, link direto e QR Code. Nenhuma resolução completa é copiada ou hospedada.
5. Nenhum dado pessoal em código, commits, logs, inventário, PDFs, site ou documentação.

Antes de trabalhar neste repositório, leia `docs/coordenacao/README.md`.
