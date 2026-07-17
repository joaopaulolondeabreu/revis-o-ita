# STATUS

## Situação atual

- **Última atualização:** 2026-07-16 22:52 (America/Sao_Paulo)
- **Agente:** Claude
- **Etapa do projeto:** 1 — Fundação **CONCLUÍDA** + preparação da ingestão (offline)

## Trabalho realizado nesta atualização

- Estrutura do repositório, documentação de coordenação, inventário-esqueleto ITA 2026–2002 (25 edições, situação `aguardando verificacao`).
- Scripts em `ferramentas/`: `validar_pdf.py`, `protecao.py`, `qr.py`, `montar.py` (com `verificar_fidelidade_visual` por renderização), `catalogo.py`, `teste_fundacao.py`.
- Teste de fumaça passou por completo (Caso 1 e Caso 2 com material fictício; QR decodificado de volta à URL exata; fidelidade visual das páginas da prova confirmada).
- Site Astro em `site/`: página inicial, página do ITA com 25 anos em ordem decrescente e filtro por ano, página por ano com botões "Abrir prova — gabarito no final", selo "GABARITO NO FINAL", aviso "Este PDF contém o gabarito e as respostas depois da página de proteção", página 404. Build OK: 28 páginas.
- Preparação da ingestão sem depender da rede: `ferramentas/ingestao.py` (download + validação + hash + registro automático no inventário, sem sobrescrever nada divergente), `ferramentas/relatorio.py` (resumo do inventário por situação/ano), `docs/coordenacao/URLS_CANDIDATAS.md` (padrões de URL do acervo oficial e do Poliedro descobertos por busca na web — TODOS ainda a verificar).
- Fluxo de publicação criado (`.github/workflows/publicar-site.yml`), disparo manual apenas — nada é publicado sem acionamento deliberado, e a divulgação definitiva só após aprovação explícita do usuário.

## Pendências que bloqueiam as próximas etapas

1. **Rede do ambiente bloqueada** para `vestibular.ita.br` e `poliedroresolve.sistemapoliedro.com.br` — o usuário precisa liberar nas configurações do ambiente (instruções já enviadas). Bloqueia: verificação do acervo, inventário real, toda a ingestão.
2. GitHub Pages ainda não ativado (só será necessário na fase de pré-visualização).

## Próxima tarefa recomendada

Assim que a rede for liberada: verificar o acervo oficial do ITA (`provas.htm`), mapear anos/formatos reais, preencher o inventário 2026–2002 e **medir o tamanho real dos primeiros PDFs** antes de decidir onde armazená-los (ver DECISOES.md D5).
