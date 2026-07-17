# STATUS

## Situação atual

- **Última atualização:** 2026-07-16 23:02 (America/Sao_Paulo)
- **Agente:** Claude
- **Etapa do projeto:** 1 — Ingestão oficial CONCLUÍDA; primeiros PDFs finais (Caso 1) montados

## Trabalho realizado nesta atualização

- Estrutura do repositório, documentação de coordenação, inventário-esqueleto ITA 2026–2002 (25 edições, situação `aguardando verificacao`).
- Scripts em `ferramentas/`: `validar_pdf.py`, `protecao.py`, `qr.py`, `montar.py` (com `verificar_fidelidade_visual` por renderização), `catalogo.py`, `teste_fundacao.py`.
- Teste de fumaça passou por completo (Caso 1 e Caso 2 com material fictício; QR decodificado de volta à URL exata; fidelidade visual das páginas da prova confirmada).
- Site Astro em `site/`: página inicial, página do ITA com 25 anos em ordem decrescente e filtro por ano, página por ano com botões "Abrir prova — gabarito no final", selo "GABARITO NO FINAL", aviso "Este PDF contém o gabarito e as respostas depois da página de proteção", página 404. Build OK: 28 páginas.
- Preparação da ingestão sem depender da rede: `ferramentas/ingestao.py` (download + validação + hash + registro automático no inventário, sem sobrescrever nada divergente), `ferramentas/relatorio.py` (resumo do inventário por situação/ano), `docs/coordenacao/URLS_CANDIDATAS.md` (padrões de URL do acervo oficial e do Poliedro descobertos por busca na web — TODOS ainda a verificar).
- Fluxo de publicação criado (`.github/workflows/publicar-site.yml`), disparo manual apenas — nada é publicado sem acionamento deliberado, e a divulgação definitiva só após aprovação explícita do usuário.

## Fatos consolidados (2026-07-16/17)

- Rede liberada pelo usuário; ambos os sites acessíveis.
- Acervo oficial mapeado por `provas.htm`: **116 PDFs, todos baixados, validados e inventariados** (0 falhas).
  - 2008–2018: provas por matéria (Mat/Fís/Quí/Por/Ing), questões 1–20 objetivas + 21–30 dissertativas; gabarito oficial cobre só as objetivas → **Caso 2** para as dissertativas.
  - 2019–2026: 1ª fase objetiva + 2ª fase por matéria (Redação 2019–2024; Português na 2ª fase 2025–2026 com gabarito objetivo próprio `gabarito_<ano>_2f.pdf`); gabaritos oficiais cobrem só objetivas → 2ª fase discursiva é **Caso 2**.
  - 2002–2007: **ausentes do acervo oficial** — pendentes (regra D7).
- **PDFs finais Caso 1 montados e validados: 1ª fase 2019–2026 (8 arquivos)** — prova + página de proteção + gabarito oficial; fidelidade visual conferida por renderização página a página.
- Site atualizado: mostra como disponíveis apenas os PDFs finais; provas já obtidas aparecem como "PDF com gabarito em preparação".

## Pendências

1. GitHub Pages ainda não ativado (necessário só na pré-visualização).
2. Caso 2 pendente: mapear páginas por prova no Poliedro Resolve (link direto + QR), transcrever respostas finais das dissertativas (2008–2018 e 2ª fase 2019–2026).
3. Português 2ª fase 2025/2026: montar com `gabarito_<ano>_2f.pdf` (verificar se a prova inclui redação → entrada "produção textual").
4. 2002–2007: buscar fonte oficial/pública confiável das provas.

## Próxima tarefa recomendada

Mapear o Poliedro Resolve: confirmar a existência de página específica por prova (candidata: `…/vestibulares/ita/<ano>/<slug-da-prova>/`), registrar os links diretos por prova/matéria no inventário e iniciar a transcrição das respostas finais das dissertativas, começando pelos anos mais recentes.
