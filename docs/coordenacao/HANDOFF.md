# HANDOFF — resumo para o próximo agente

- **Última atualização:** 2026-07-16 22:52 (America/Sao_Paulo) — Claude

## O que já existe

- Plano aprovado pelo usuário em 2026-07-16, com 5 ajustes incorporados (ver DECISOES.md D3, D4, D5, D7, D9).
- Fundação criada nesta sessão: documentação de coordenação, inventário-esqueleto (`INVENTARIO_ITA.csv`, 25 edições com situação `aguardando verificacao`), scripts em `ferramentas/`, site Astro em `site/`.
- Cadeia de montagem de PDF testada com material fictício (teste de fumaça em `ferramentas/teste_fundacao.py`).
- Ingestão pronta para rodar assim que a rede for liberada: `ferramentas/ingestao.py` + padrões de URL candidatos em `docs/coordenacao/URLS_CANDIDATAS.md` (não verificados — confirmar pela página índice `provas.htm`, nunca por adivinhação de padrão).
- Workflow de publicação manual em `.github/workflows/publicar-site.yml` (exige o usuário ativar Pages em Settings → Pages → Source: GitHub Actions, uma única vez, antes da pré-visualização).

## O que NÃO fazer

- Não iniciar IME ou outras instituições (aguarda autorização explícita do usuário).
- Não extrair questões individuais.
- Não copiar/hospedar resoluções completas do Poliedro.
- Não resolver/deduzir/redigir respostas — só transcrição fiel de resultado final explícito.
- Não divulgar link definitivo antes da aprovação explícita do usuário.
- Não colocar dados pessoais do usuário em lugar nenhum (incluindo autoria de commits — usar identidade neutra).

## Bloqueio atual

A rede do ambiente nega acesso às duas fontes (ITA e Poliedro). O usuário foi instruído a liberar. **Nada de ingestão até isso ser resolvido e testado.**

## Próxima ação

Ver STATUS.md → "Próxima tarefa recomendada".
