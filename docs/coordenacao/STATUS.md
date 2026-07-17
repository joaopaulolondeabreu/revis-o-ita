# STATUS

Regra: cada agente edita SOMENTE a sua seção. Não reformatar a seção do outro.

---

### Claude

- **Atualizado em:** 2026-07-17 17:10 (America/Sao_Paulo)
- **Papel:** líder técnico (decisões, código, PDFs finais, site, testes, publicação, integração) — ver DECISOES.md D12. Retomei a sessão após o Codex ter assumido a finalização técnica sob D13 (tokens do Claude esgotados); reconciliei meu branch local com o que já estava publicado (reset para `73c589d`, sem perda — meu commit divergente `e57e4d9` não continha nada além do que já estava em `d8e23d2`).
- **Tarefa concluída:** extensão do PEDIDO 2 — publicação das 5 provas discursivas 2017–2018 que a finalização anterior deixou pendentes por completo. Estado: CONCLUÍDO. Ver D14.
- **Decisão técnica (D14):** o integrador estava gating por status de nível de ITEM ("pronto"/"pendente"), então só Matemática 2018 (10/10 questões prontas) tinha sido publicada; as outras 5 provas (com 39/50 questões já prontas e conferidas) ficaram totalmente fora do site. Reprojetei `integrar_pacote.py` para granularidade POR QUESTÃO: cada resposta usa seu próprio `status_questao`; publica o texto real se "pronto", senão publica a frase padrão do plano ("Confira a resolução completa...") — nunca o texto não confirmado. Isso é exatamente o mecanismo que o plano original desenhou para este caso (seção 16), então maximiza o valor para os alunos sem abrir mão de nenhuma garantia de qualidade.
- **Resultado:** 6/6 provas discursivas 2017–2018 publicadas (Matemática, Física, Química de cada ano), todas validadas (hash do original, link do Poliedro HTTP 200, fidelidade visual das páginas da prova, QR decodificado = URL declarada). 49 respostas reais publicadas + 11 com a frase padrão (nenhuma inventada). Registro de auditoria completo (texto original do Codex preservado) em RESPOSTAS_COMPLEMENTARES.csv, mesmo para as pendentes.
- **Amostragem de conferência (2ª verificação, antes de integrar):** hashes das 6 resoluções do Poliedro conferem 100% com o pacote; comparei visualmente 5 respostas específicas contra a resolução de origem (Mat 2018 Q21, Fís 2017 Q24 — corretamente marcada pendente, Quí 2017 Q28 — corretamente pendente por erro no próprio enunciado admitido pela fonte) — todas corretas.
- **Bug real encontrado e corrigido antes desta rodada:** a versão anterior do `protecao.py` usava fontes Helvetica sem cobertura de símbolos matemáticos Unicode (ℝ, ∛, subíndices apareciam como quadrados) e a URL longa do link direto estourava a margem da página. A sessão do Codex já havia corrigido isso de forma independente (fontes DejaVu com fallback Vera do próprio reportlab + quebra de linha por largura real) antes de eu retomar — mantive a implementação deles, que é mais robusta que a minha tentativa anterior (evita bundlar fonte extra no repo).
- **Arquivos sob responsabilidade:** `ferramentas/`, `site/`, `.github/`, PDFs finais em `site/public/pdfs/`, integração do inventário.

**Tarefa concluída nesta rodada — auditoria de qualidade do site + Português/Inglês 2008–2018:**
- Enquanto aguardo o pacote do PEDIDO 3, rodei pela primeira vez o checklist completo de testes do site (seção TESTES DO SITE do plano) contra o build publicado, usando Playwright + axe-core. **Importante sobre o ambiente:** o Chromium headless deste ambiente não consegue atravessar o proxy de rede para acessar internet externa (falha até para `example.com`/`anthropic.com`, apesar do `curl` funcionar) — troquei a estratégia para servir o `dist/` localmente (idêntico ao publicado) e testar contra `localhost`, sem depender do proxy; complementei com checagens HTTP diretas (`curl`) contra a URL pública para confirmar que o conteúdo ao vivo bate com o testado localmente.
- Cobertura do teste automatizado: home mobile/desktop, filtro de anos, botões/selo "gabarito no final", link do PDF resolvendo como `application/pdf`, ano com mistura Caso 1/Caso 2, ano pendente, página 404, foco de teclado visível, ausência de dados pessoais no HTML, e acessibilidade WCAG2A/AA via axe-core. **Resultado final: 0 falhas, 0 avisos.**
- **2 achados reais corrigidos:**
  1. Faltava favicon → toda página gerava um erro de console (404 em `/favicon.ico`), o que viola a regra "ausência de erros no console". Gerei um favicon simples (bloco azul com "R", cores do site) e liguei no layout.
  2. **Lacuna de cobertura:** Português e Inglês de 2008–2018 (22 provas) nunca tinham sido montados em PDF final, mesmo sendo 100% objetivos (conferido por amostragem — sem questões dissertativas) e cobertos pelo gabarito oficial único do ano — ou seja, elegíveis para Caso 1 sem depender de nenhum pacote do Codex. Estendi `montar_lote.py` e montei as 22 provas; todas validadas (PDF íntegro, fidelidade visual, sem falhas). O gabarito de 2014 tem 2 páginas oficiais (nota do ITA sobre questões anuladas) — preservado integralmente, não é erro.
- Não toquei no `package.json`/`package-lock.json` de produção do site para instalar ferramentas de teste — Playwright e axe-core foram instalados isolados no scratchpad, fora do repositório.

**Estado consolidado do projeto:**
- Acervo oficial 2008–2026: 116/116 PDFs baixados, validados, inventariados (0 falhas). 2002–2007 ausentes do acervo oficial (pendentes, regra D7).
- Formatos históricos confirmados: 2008–2018 provas por matéria (Q1–20 objetivas com gabarito oficial; Q21–30 dissertativas sem resposta oficial → Caso 2, exceto Português/Inglês que são 100% objetivos → Caso 1); 2019–2026 1ª fase objetiva (Caso 1) + 2ª fase discursiva (Caso 2), Redação 2019–2024, Português na 2ª fase 2025–2026 com `gabarito_<ano>_2f.pdf`.
- **38 PDFs finais publicados:** 1ª fase 2019–2026 (8, Caso 1), Português e Redação 2ª fase 2025–2026 (2, Caso 1), discursivas 2017–2018 Matemática/Física/Química (6, Caso 2), Português/Inglês 2008–2018 (22, Caso 1). Repositório de PDFs: ~71 MB.
- Poliedro verificado: cobertura pública 2017–2026; link direto por prova = página da 1ª questão + `#exam-downloads` (download sem cadastro). Dissertativas 2008–2016 sem fonte pública no Poliedro (lacuna registrada).
- Site Astro publicado em `https://joaopaulolondeabreu.github.io/revis-o-ita/` (GitHub Pages ativo, workflow manual). Checklist de testes do plano rodado e aprovado (ver acima). Commit `23a2675` publicado (workflow run 29599008982, sucesso); favicon e as 22 provas de Português/Inglês confirmados ao vivo por HTTP.

**2026-07-17 17:50 — Codex descontinuado (D15); Claude assume as duas funções.** O usuário decidiu parar de usar o Codex neste projeto. A partir de agora eu também pesquiso fontes, baixo materiais, mapeio links do Poliedro e transcrevo respostas — mantendo o mesmo rigor (segunda conferência por amostragem, hash, fidelidade visual, evidência por resposta). `PEDIDOS_PARA_CODEX.md`/`ENTREGAS_DO_CODEX.md` continuam como registro histórico e checklist, sem a etapa formal de "pedido/entrega" entre agentes.

**PEDIDO 3, ano 2026 concluído e publicado:** Matemática, Física e Química 2ª fase 2026 (30 questões dissertativas, sem gabarito oficial). Método: as páginas do Poliedro para 2026 publicam a resolução como texto na própria página da questão (não há mais PDF de resolução separado nesse ano) — baixei cada página com curl e extraí o texto localmente com Playwright (sem depender de rede no navegador para o Chromium, que não atravessa o proxy deste ambiente), conferindo notação ambígua por captura de tela antes de transcrever. Resultado: 28/30 prontas, 2 pendentes (Matemática Q6 sem resultado separável por item; Física Q4 porque a própria resolução do Poliedro recomenda anular a questão por premissa inconsistente). Encontrei e corrigi um bug real na verificação de QR Code (falhava para URLs longas por causa da escala de teste, não do QR em si). **38 → 41 PDFs finais publicados.**

**2026-07-17 18:05 — PEDIDO 3, ano 2025 concluído e publicado:** Matemática, Física e Química 2ª fase 2025 (26/30 prontas). Lição aprendida nesta rodada: a extração de texto pode perder o símbolo de raiz (√) silenciosamente — corrigi criando `screenshot_final.js`, que captura visualmente só a região final de cada resolução, e passei a confirmar visualmente toda resposta numérica antes de transcrever (não só as "obviamente ambíguas" como antes). **41 → 47 PDFs finais publicados.**

**2026-07-17 18:16 — PEDIDO 3, ano 2024 concluído e publicado:** Matemática, Física e Química 2ª fase 2024 (27/30 prontas) + Redação 2024 (arquivo separado, observação "produção textual"). Diferença notada: 2024 usa PDF de resolução baixável (padrão 2017/2018), não texto inline como 2025/2026. Achado real não corrigido por mim: Física 2024 Q4 tem duas resoluções alternativas na própria fonte, divergentes por um fator 2 — mantive pendente. **47 → 57 PDFs finais publicados.**

**Próxima dependência:** nenhuma — vou continuar sozinho pelo PEDIDO 3 (2023, 2022, 2021, 2020, 2019, nessa ordem) e depois retomar a decisão em aberto abaixo.

**Decisão em aberto (não executada ainda — registrando em vez de agir sozinho):** Mat/Fís/Quí 2008–2016 têm as dissertativas 21–30 sem gabarito oficial E sem fonte no Poliedro (lacuna confirmada). O plano não cobre explicitamente esse caso (ausência total de fonte, não apenas "Poliedro sem resultado separável"). Antes de publicar essas provas com um formato "gabarito parcial" (só 1–20), quero uma segunda opinião — não é uma tarefa mecânica que dá para simplesmente executar sozinho, é uma decisão editorial sobre o que os alunos veem. Registrado como pendência; não vou pausar o trabalho técnico esperando por isso, mas também não vou publicar nada nesse formato sem decidir com cuidado.

---

### Codex

- **Atualizado em:** 2026-07-17 02:29 (America/Sao_Paulo)
- **Papel nesta etapa:** finalização técnica assumida a pedido explícito do usuário após o encerramento da sessão do Claude; a seção do Claude foi preservada sem alterações.
- **Tarefa:** integrar o PEDIDO 2, corrigir bloqueios de publicação, validar e publicar o site.
- **Estado:** CONCLUÍDO E PUBLICADO. GitHub Pages ativado com fonte `GitHub Actions`; workflow `Publicar site #2` concluído com build e deploy em sucesso.
- **Integração do PEDIDO 2:** Matemática 2018, único item integralmente `pronto`, foi integrada em PDF final de 10 páginas. As outras cinco provas continuam pendentes porque contêm respostas exclusivamente gráficas/estruturais, ausência de resultado separável ou inconsistência da própria fonte; nada foi deduzido.
- **Correções técnicas:** compatibilidade do integrador com Windows; registros idempotentes; dependência `tzdata`; quebra de linhas e fontes Unicode nos PDFs; regeneração validada dos 10 PDFs finais anteriores; Astro atualizado para 7.1.0, com auditoria npm em 0 vulnerabilidades.
- **Validações:** teste de fumaça completo; fidelidade visual das páginas oficiais; QR decodificado; 11 PDFs finais válidos; build estático de 28 páginas; publicação pública em `https://joaopaulolondeabreu.github.io/revis-o-ita/`; página inicial, ano 2018 e PDF de Matemática 2018 respondendo HTTP 200; PDF servido como `application/pdf` com 286.161 bytes; navegador sem erros.
- **Próxima fila após a publicação:** PEDIDO 3, começando pelo pacote da 2ª fase de 2026.
