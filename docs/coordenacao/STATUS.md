# STATUS

## Situação atual

- **Última atualização:** 2026-07-16 22:47 (America/Sao_Paulo)
- **Agente:** Claude
- **Etapa do projeto:** 1 — Fundação **CONCLUÍDA**

## Trabalho realizado nesta atualização

- Estrutura do repositório, documentação de coordenação, inventário-esqueleto ITA 2026–2002 (25 edições, situação `aguardando verificacao`).
- Scripts em `ferramentas/`: `validar_pdf.py`, `protecao.py`, `qr.py`, `montar.py` (com `verificar_fidelidade_visual` por renderização), `catalogo.py`, `teste_fundacao.py`.
- Teste de fumaça passou por completo (Caso 1 e Caso 2 com material fictício; QR decodificado de volta à URL exata; fidelidade visual das páginas da prova confirmada).
- Site Astro em `site/`: página inicial, página do ITA com 25 anos em ordem decrescente e filtro por ano, página por ano com botões "Abrir prova — gabarito no final" e selo "GABARITO NO FINAL". Build OK: 27 páginas geradas.

## Pendências que bloqueiam as próximas etapas

1. **Rede do ambiente bloqueada** para `vestibular.ita.br` e `poliedroresolve.sistemapoliedro.com.br` — o usuário precisa liberar nas configurações do ambiente (instruções já enviadas). Bloqueia: verificação do acervo, inventário real, toda a ingestão.
2. GitHub Pages ainda não ativado (só será necessário na fase de pré-visualização).

## Próxima tarefa recomendada

Assim que a rede for liberada: verificar o acervo oficial do ITA (`provas.htm`), mapear anos/formatos reais, preencher o inventário 2026–2002 e **medir o tamanho real dos primeiros PDFs** antes de decidir onde armazená-los (ver DECISOES.md D5).
