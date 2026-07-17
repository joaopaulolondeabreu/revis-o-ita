# Entregas do Codex

O Codex registra aqui cada pacote pronto. Claude valida antes de integrar.

Modelo de registro (copiar por entrega):

```
## PACOTE <nome> — <data e hora America/Sao_Paulo>
- Pedido atendido: PEDIDO <n>
- Estado: CONCLUÍDO | BLOQUEADO | AGUARDANDO_DECISÃO
- Caminho: docs/coordenacao/pacotes/<nome>/pacote.json
- Itens: <quantos prontos / quantos pendentes>
- Evidências: <como conferir rapidamente>
- Pendências e lacunas: <lista objetiva>
- Commit: <hash, se houver>
```

---

## PACOTE auditoria-2008-2026 — 2026-07-17 00:00 (America/Sao_Paulo)
- Pedido atendido: PEDIDO 1
- Estado: CONCLUÍDO
- Caminho: docs/coordenacao/pacotes/auditoria-2008-2026/pacote.json
- Itens: 116 auditados / 0 divergências
- Evidências: método descrito no pacote (hash + páginas + renderização das 116 primeiras páginas)
- Pendências e lacunas: nenhuma; aviso não fatal do pypdf em redacao_2021_2f.pdf documentado (não é divergência)
- Observação de integração: commits do Codex não puderam ser enviados ao GitHub (sem credencial); conteúdo transcrito ao repositório por Claude a partir do texto colado pelo usuário. **Validação do Claude: APROVADO** — contagens reconferidas (116/116) e 5 hashes amostrados conferem.

## PACOTE fontes-2002-2007 — 2026-07-17 00:20 (America/Sao_Paulo)
- Pedido atendido: PEDIDO 4
- Estado: CONCLUÍDO (com lacunas registradas)
- Caminho: docs/coordenacao/pacotes/fontes-2002-2007/pacote.json
- Itens: 6 anos pesquisados / 6 pendentes (nenhuma fonte pronta para ingestão)
- Evidências: 7 fontes documentadas com URL, situação e lacunas por ano
- Pendências e lacunas: procedência, fidelidade e autorização não comprovadas em nenhuma fonte; gabaritos oficiais 2002–2007 não localizados
- Observação de integração: transcrito por Claude (mesmo motivo acima). **Decisão do Claude (líder técnico): recomendação ACEITA** — nada será baixado ou integrado de 2002–2007 por ora; os 6 anos permanecem `pendente` no inventário e no site; Sótão da Química e Só Literatura ficam registrados apenas como referências de descoberta em FONTES.md.
