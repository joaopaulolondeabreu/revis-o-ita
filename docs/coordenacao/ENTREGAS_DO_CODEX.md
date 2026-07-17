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

## PACOTE discursivas-2019-2026 (lote 2025) — 2026-07-17 18:05 (America/Sao_Paulo)
- Preparado e integrado por: Claude
- Pedido atendido: PEDIDO 3 (ano 2025)
- Estado: CONCLUÍDO
- Itens: 3 provas (Matemática, Física, Química) / 30 questões / 26 prontas / 4 pendentes
- Método idêntico ao lote 2026. Lição aprendida e aplicada: a extração de texto (innerText) pode PERDER o símbolo de raiz (√) silenciosamente (ex.: 'r=3' em vez de 'r=√3'). A partir deste lote, toda resposta numérica "limpa" passou por captura de tela do trecho final antes da transcrição — não confiei mais só no texto extraído. Criado `screenshot_final.js`, que recorta e captura só a região final (onde fica o resultado) de cada resolução, para leitura visual eficiente sem depender de rede no Chromium.
- Pendências: Física 2025 Q2, Q3 e Q8 (fórmulas finais longas com radicais/expoentes aninhados, cortadas ou ambíguas na renderização disponível — marcadas pendentes por prudência, não por falta de conteúdo); Química 2025 Q9 (questão inteiramente descritiva, sem resultado curto separável); Matemática 2025 e Química 2025 tiveram pequenos itens pendentes dentro de questões majoritariamente prontas (ex.: desenho de isômeros).
- Validação: 6/6 PDFs finais (2026+2025) montados, fidelidade visual OK, QR decodificado = URL em todos.

## PACOTE discursivas-2019-2026 (lote 2024) — 2026-07-17 18:16 (America/Sao_Paulo)
- Preparado e integrado por: Claude
- Pedido atendido: PEDIDO 3 (ano 2024)
- Estado: CONCLUÍDO
- Itens: 3 provas (Matemática, Física, Química) / 30 questões / 27 prontas / 3 pendentes
- Método diferente dos lotes 2025/2026: em 2024 o Poliedro publica um PDF de resolução baixável por matéria (mesmo padrão de 2017/2018), não texto inline. Baixei os 3 PDFs (mat/fís/quí) só para consulta local (não commitados), renderizei cada página e li visualmente.
- Achado registrado, não corrigido pelo agente: Física 2024 Q4 tem duas resoluções alternativas apresentadas pela própria fonte que divergem por um fator 2 — mantive pendente em vez de escolher uma.
- Química 2024 Q2 e Q8: resolvidas inteiramente por desenho de fórmulas estruturais, sem texto equivalente — pendentes por não haver o que transcrever com segurança.
- Redação 2024 (arquivo separado da ITA) publicada com página de observação "Não possui resposta única — produção textual", sem envolver o Poliedro (mesmo padrão usado para Português 2025/2026).
- Validação: 9/9 PDFs finais (2026+2025+2024) montados, fidelidade visual OK, QR decodificado = URL em todos.

## PACOTE discursivas-2019-2026 (lote 2026) — 2026-07-17 17:50 (America/Sao_Paulo)
- Preparado e integrado por: Claude (papel único a partir de D15 — Codex descontinuado)
- Pedido atendido: PEDIDO 3 (início, ano 2026)
- Estado: CONCLUÍDO
- Caminho: docs/coordenacao/pacotes/discursivas-2019-2026/pacote.json (item 2026, 3 matérias)
- Itens: 3 provas (Matemática, Física, Química) / 30 questões / 28 prontas / 2 pendentes
- Método: páginas do Poliedro para 2026 publicam a resolução como texto HTML na própria página da questão (não há PDF de resolução separado nesse ano). Cada página foi baixada com curl e o texto extraído localmente com Playwright (sem depender de rede no navegador); notação ambígua (frações, radicais) foi conferida por captura de tela adicional antes da transcrição.
- Pendências: Matemática Q6 (sem resultado separável por item na fonte); Física Q2 (fórmulas longas + item b sem valores individuais, por prudência) e Q4 (a própria fonte do Poliedro recomenda a anulação da questão por premissa inconsistente).
- Bug corrigido durante a integração: a verificação automática de QR Code falhava para URLs longas (Química 2026) por causa da escala de renderização usada só no teste, não no QR em si — confirmado manualmente que o mesmo PNG decodifica corretamente em escala maior. Corrigido em `integrar_pacote.py` com tentativa em escalas crescentes.
- Validação: 3/3 PDFs finais montados sem gabarito oficial (provas 100% dissertativas), fidelidade visual das páginas da prova OK, QR decodificado = URL declarada nos 3.

## PACOTE discursivas-2017-2018 — 2026-07-17 01:10 (America/Sao_Paulo)
- Pedido atendido: PEDIDO 2
- Estado: CONCLUÍDO (com pendências documentadas)
- Caminho: docs/coordenacao/pacotes/discursivas-2017-2018/pacote.json
- Itens: 6 provas / 60 questões conferidas / 49 prontas / 11 pendentes ou parciais
- Evidências: seis páginas públicas e seis PDFs do Poliedro responderam HTTP 200; os PDFs têm 30 páginas cada, foram validados por SHA-256 e tiveram as páginas 21–30 renderizadas e conferidas visualmente. Cada resposta registra página/posição e URL exata.
- Pendências e lacunas: respostas exclusivamente gráficas, diagramáticas ou estruturais não foram copiadas; questões sem resultado separável, com resposta não única ou com inconsistência da própria fonte foram mantidas `pendente`. A lista individual está no pacote.
- Confirmação adicional: Inglês 1–20 e Português 21–40 de 2017–2018 são objetivos e constam do gabarito oficial; não há parte discursiva 21–30 nessas matérias. A redação separada foi registrada apenas com a frase padrão.
- Materiais de consulta: seis PDFs em `consulta/`, cobertos por `docs/coordenacao/pacotes/.gitignore` e não commitados.
- Commit: a entrega e este registro integram o mesmo commit; o hash é informado no handoff ao usuário.

## PUBLICAÇÃO GitHub Pages — 2026-07-17 02:29 (America/Sao_Paulo)
- Estado: CONCLUÍDO
- Ramo publicado: `claude/ita-vestibular-planning-bjhf6y`
- Conteúdo validado: árvore Git `6ab15f25a639eb7f5231c3706aba603a0f3cb686`; commit técnico publicado `fe86e65baea3a3c4ee7b58335f155085d81a7ed2`
- Workflow: `Publicar site #2`, execução `29557366174`; jobs `build` e `deploy` concluídos com sucesso
- URL pública: `https://joaopaulolondeabreu.github.io/revis-o-ita/`
- Evidências: página inicial e página `/ita/2018/` responderam HTTP 200; o PDF de Matemática 2018 respondeu HTTP 200, `application/pdf`, 286.161 bytes; conferência visual no navegador sem erros de console

## EXTENSÃO discursivas-2017-2018 (Claude, D14) — 2026-07-17 16:31 (America/Sao_Paulo)
- Pedido atendido: PEDIDO 2 (conclusão total, além do que já estava publicado)
- Estado: CONCLUÍDO
- O pacote do Codex já continha granularidade por questão (`status_questao`) para as 60 respostas; a integração anterior só publicou o item 100% completo (Matemática 2018). Reprojetei `integrar_pacote.py` para publicar por questão (ver DECISOES.md D14) e reintegrei o pacote inteiro.
- Resultado: 6/6 provas publicadas — Matemática, Física e Química de 2017 e 2018. 49 respostas reais + 11 com a frase padrão do plano (nenhuma inventada). Todas validadas: hash do original, link do Poliedro HTTP 200, fidelidade visual, QR decodificado = URL.
- Segunda conferência amostral antes de integrar: 6/6 hashes das resoluções do Poliedro conferem; 5 respostas comparadas visualmente contra a fonte (inclusive duas marcadas pendente, confirmando o critério do Codex estava correto).
- Site reconstruído (28 páginas); commit `0e78615` enviado; workflow `Publicar site` (run #3) disparado e concluído com sucesso. Confirmado ao vivo: `/ita/2017/` responde HTTP 200, e os PDFs de Física 2017 e Química 2018 respondem HTTP 200 `application/pdf`. As 6 provas discursivas 2017–2018 estão publicadas em `https://joaopaulolondeabreu.github.io/revis-o-ita/`.
