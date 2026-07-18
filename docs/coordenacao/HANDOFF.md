# HANDOFF — resumo para o próximo agente

- **Última atualização:** 2026-07-17 18:45 (America/Sao_Paulo) — Claude (líder técnico e, desde D15, também responsável pela preparação; Codex foi descontinuado pelo usuário)

## Como se situar (leia nesta ordem)

1. Este arquivo (visão geral).
2. `STATUS.md` — estado detalhado e decisões recentes.
3. `DECISOES.md` — D1 a D15 (arquitetura, regras, divisão de trabalho).
4. `PEDIDOS_PARA_CODEX.md` + `ENTREGAS_DO_CODEX.md` — histórico e checklist (hoje preenchidos só por Claude).
5. `INVENTARIO_ITA.csv` — fonte única da verdade dos materiais.
6. `pacotes/discursivas-2019-2026/pacote.json` — todas as respostas transcritas de 2024–2026 com evidência por questão.

## O QUE JÁ ESTÁ FEITO (publicado em https://joaopaulolondeabreu.github.io/revis-o-ita/)

- **Acervo oficial completo:** 116 PDFs de 2008–2026 baixados de vestibular.ita.br, validados (hash SHA-256, páginas renderizáveis) e inventariados. Auditados item a item (0 divergências).
- **48 PDFs finais publicados no site**, todos no formato prova intacta → página(s) de proteção → gabarito/respostas:
  - 1ª fase 2019–2026 (8, Caso 1 com gabarito oficial);
  - Português e Redação 2ª fase 2025–2026 (2, Caso 1 + observação de redação);
  - Português e Inglês 2008–2018 (22, Caso 1 — 100% objetivas);
  - Discursivas Mat/Fís/Quí 2017–2018 (6, Caso 2 com respostas do Poliedro);
  - Discursivas Mat/Fís/Quí 2024, 2025, 2026 (9, Caso 2 sem gabarito oficial — provas 100% dissertativas);
  - Redação 2024 (1, observação "produção textual").
- **Site Astro no ar** (GitHub Pages, workflow manual `publicar-site.yml`): home → ITA → 25 anos com filtro; botões "Abrir prova — gabarito no final"; selo "GABARITO NO FINAL"; favicon; 404. Checklist de testes do plano rodado com Playwright + axe-core: 0 falhas (mobile/desktop, acessibilidade WCAG2A/AA, console limpo, sem dados pessoais).
- **Qualidade das transcrições:** 2017–2018 = 49 respostas + 11 frase padrão; 2024–2026 = 81 respostas + 9 pendentes com motivo documentado (ver seção pendências). Toda resposta com URL da fonte + evidência de localização; registro completo de auditoria em `RESPOSTAS_COMPLEMENTARES.csv`.

## FERRAMENTAS PRONTAS (`ferramentas/`)

- `ingestao.py` — baixa/valida/registra material oficial.
- `montar_lote.py` — monta PDFs Caso 1 (idempotente; `--regerar` para forçar).
- `integrar_pacote.py` — consome `pacote.json` (formato D10) e monta Caso 2 completo: valida hash do original, checa URL do Poliedro (HTTP 200), monta com 2 proteções + QR, verifica fidelidade visual página a página e decodifica o QR de volta comparando com a URL. Granularidade POR QUESTÃO (`status_questao`): "pronto" publica o texto; qualquer outro publica a frase padrão ("Confira a resolução completa...").
- `catalogo.py` — INVENTARIO_ITA.csv → catálogo JSON do site (rodado automaticamente no build via `prebuild`).
- `relatorio.py`, `validar_pdf.py`, `teste_fundacao.py` (teste de fumaça completo).

## COMO CONTINUAR O PEDIDO 3 (próxima tarefa imediata)

Faltam as discursivas de **2023, 2022, 2021, 2020, 2019** (Mat/Fís/Quí; + Redação 2019–2023 como observação "produção textual", igual fiz para 2024).

Fluxo que usei para 2024–2026 (repetir por ano, mais recente primeiro):

1. Slugs do Poliedro por ano já mapeados em `URLS_CANDIDATAS.md` (padrão: `.../vestibulares/ita/<ano>/<slug-prova>/dissertativa-<n>-<materia>-<dia>-ita-<ano>`). Confirmar com `curl` (HTTP 200). Atenção: 2019–2023 têm 2 dias (dia 1 = Mat+Quí, dia 2 = Fís+Red), não 3-4 dias como 2025-2026.
2. **Formato da resolução varia por ano:** 2025–2026 = texto inline na página da questão (bloco `.ck-content`); 2024 e 2017–2018 = PDF de resolução baixável (URL no HTML, busque `exam-files`). Verifique qual é o caso antes de extrair.
3. Extração: baixar páginas com `curl` (o Chromium deste ambiente NÃO atravessa o proxy para internet externa — nunca navegue direto). Para texto inline: scripts no scratchpad da sessão anterior (`extrair_resolucao.js`, `screenshot_final.js` — recriar se necessário: Playwright com `page.setContent(html)` local + bloqueio de rede, ler `.ck-content`). Para PDF: baixar só para consulta local (NUNCA commitar), renderizar páginas com `pypdfium2` e ler visualmente.
4. **REGRA CRÍTICA aprendida:** a extração de texto perde o símbolo √ silenciosamente ("r=3" em vez de "r=√3"). TODA resposta numérica deve ser conferida visualmente (screenshot/render) antes de transcrever.
5. Adicionar itens ao `pacotes/discursivas-2019-2026/pacote.json` (seguir o formato dos itens existentes, com `status_questao` e `evidencia` por questão) e rodar `python integrar_pacote.py ../docs/coordenacao/pacotes/discursivas-2019-2026/pacote.json` (idempotente — reprocessa tudo sem duplicar).
6. Rebuild site (`cd site && npm run build`), rodar QA local (servir `dist/` com http.server local; o teste Playwright roda contra localhost), commit, push, disparar workflow `publicar-site.yml` via API do GitHub, confirmar HTTP 200 ao vivo.

## PENDÊNCIAS CONHECIDAS (não são "faltou fazer" — são registradas com motivo)

- **11 questões de 2024–2026 + as de 2017–2018 com frase padrão:** por fórmula complexa demais para transcrição segura (Fís 2025 Q2/Q3/Q8, Fís 2026 Q2), resposta só em desenho estrutural (Quí 2024 Q2/Q8), questão descritiva sem resultado curto (Quí 2025 Q9), inconsistência da PRÓPRIA fonte (Fís 2026 Q4 — Poliedro sugere anulação; Fís 2024 Q4 — duas resoluções divergentes), ou resultado não separável por item (Mat 2026 Q6). O usuário questionou se fui conservador demais nas de "fórmula longa" — pode valer re-tentar com captura ampliada (ver `zoom.js` da sessão anterior).
- **Dissertativas Mat/Fís/Quí 2008–2016 (questões 21–30):** sem gabarito oficial E sem resolução pública no Poliedro (cobertura pública começa em 2017). DECISÃO EDITORIAL EM ABERTO: publicar essas provas com gabarito parcial (só objetivas 1–20) + aviso, ou aguardar fonte? Não decidir sozinho sem registrar bem — ver STATUS.md.
- **2002–2007:** ausentes do acervo oficial. Pesquisa de fontes feita (pacote `fontes-2002-2007`): candidatos existem (Sótão da Química, Só Literatura) mas SEM procedência/autorização comprovadas — decisão registrada de NÃO ingerir. PEDIDO 5 (minuta de e-mail ao ITA) em espera, aguardando o usuário.
- **1ª fase 2008–2018:** não existe como caderno único no acervo (o modelo era prova por matéria) — nada a fazer; já coberto pelas provas por matéria.

## O QUE FALTA PARA CONCLUIR A ETAPA 1 (critérios do plano original)

1. Discursivas 2019–2023 (PEDIDO 3, em andamento — ver acima).
2. Decidir e executar o tratamento das dissertativas 2008–2016 (decisão em aberto acima).
3. Redações 2019–2023 (arquivos `redacao_<ano>_2f.pdf` já baixados; montar com observação "produção textual" — 5 PDFs rápidos, padrão da Redação 2024).
4. Passada final de controle de qualidade (checklist completo da seção CONTROLE DE QUALIDADE do plano) + atualizar contagens no inventário.
5. Roteiro de pré-visualização para o usuário testar (seção PUBLICAÇÃO do plano: ano recente, ano antigo, Caso 1, Caso 2, QR no celular etc.).
6. Aprovação explícita do usuário → aí sim divulgar o link aos colegas. **IME e outras instituições só com autorização explícita.**

## REGRAS INVIOLÁVEIS (resumo — detalhes em README.md e DECISOES.md)

- Nunca resolver/deduzir/redigir respostas; só transcrever resultado final explícito da fonte, com evidência.
- Nunca copiar/hospedar resoluções completas do Poliedro (PDFs de consulta ficam FORA do repositório).
- Gabarito oficial do ITA sempre prevalece; divergências registradas, nunca resolvidas pelo agente.
- Provas originais visualmente intactas (conferência por renderização, automática no integrador).
- Zero dados pessoais do usuário em qualquer lugar (commits com autoria neutra "Claude <noreply@anthropic.com>").
- Nada de formulários/termos/CAPTCHA em nome do usuário.

## AMBIENTE (armadilhas conhecidas)

- Rede: `vestibular.ita.br` e `poliedroresolve.sistemapoliedro.com.br` liberados no proxy; `curl` com `--cacert /root/.ccr/ca-bundle.crt` funciona. O Chromium headless NÃO atravessa o proxy — usar Playwright só com conteúdo local (`setContent` + rota bloqueando rede).
- `pip install cffi` pode ser necessário se `pypdf` falhar com `_cffi_backend` (ver PROBLEMAS.md).
- GitHub: usar tools MCP (`mcp__github__*`) para disparar o workflow; sem `gh` CLI.
- QA local: Playwright + axe-core instalados no scratchpad (fora do repo), site servido em localhost:8877 com um http.server custom que devolve 404.html corretamente.
