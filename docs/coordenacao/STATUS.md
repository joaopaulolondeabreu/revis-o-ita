# STATUS

Regra: cada agente edita SOMENTE a sua seção. Não reformatar a seção do outro.

---

### Claude

- **Atualizado em:** 2026-07-17 16:31 (America/Sao_Paulo)
- **Papel:** líder técnico (decisões, código, PDFs finais, site, testes, publicação, integração) — ver DECISOES.md D12. Retomei a sessão após o Codex ter assumido a finalização técnica sob D13 (tokens do Claude esgotados); reconciliei meu branch local com o que já estava publicado (reset para `73c589d`, sem perda — meu commit divergente `e57e4d9` não continha nada além do que já estava em `d8e23d2`).
- **Tarefa concluída:** extensão do PEDIDO 2 — publicação das 5 provas discursivas 2017–2018 que a finalização anterior deixou pendentes por completo. Estado: CONCLUÍDO. Ver D14.
- **Decisão técnica (D14):** o integrador estava gating por status de nível de ITEM ("pronto"/"pendente"), então só Matemática 2018 (10/10 questões prontas) tinha sido publicada; as outras 5 provas (com 39/50 questões já prontas e conferidas) ficaram totalmente fora do site. Reprojetei `integrar_pacote.py` para granularidade POR QUESTÃO: cada resposta usa seu próprio `status_questao`; publica o texto real se "pronto", senão publica a frase padrão do plano ("Confira a resolução completa...") — nunca o texto não confirmado. Isso é exatamente o mecanismo que o plano original desenhou para este caso (seção 16), então maximiza o valor para os alunos sem abrir mão de nenhuma garantia de qualidade.
- **Resultado:** 6/6 provas discursivas 2017–2018 publicadas (Matemática, Física, Química de cada ano), todas validadas (hash do original, link do Poliedro HTTP 200, fidelidade visual das páginas da prova, QR decodificado = URL declarada). 49 respostas reais publicadas + 11 com a frase padrão (nenhuma inventada). Registro de auditoria completo (texto original do Codex preservado) em RESPOSTAS_COMPLEMENTARES.csv, mesmo para as pendentes.
- **Amostragem de conferência (2ª verificação, antes de integrar):** hashes das 6 resoluções do Poliedro conferem 100% com o pacote; comparei visualmente 5 respostas específicas contra a resolução de origem (Mat 2018 Q21, Fís 2017 Q24 — corretamente marcada pendente, Quí 2017 Q28 — corretamente pendente por erro no próprio enunciado admitido pela fonte) — todas corretas.
- **Bug real encontrado e corrigido antes desta rodada:** a versão anterior do `protecao.py` usava fontes Helvetica sem cobertura de símbolos matemáticos Unicode (ℝ, ∛, subíndices apareciam como quadrados) e a URL longa do link direto estourava a margem da página. A sessão do Codex já havia corrigido isso de forma independente (fontes DejaVu com fallback Vera do próprio reportlab + quebra de linha por largura real) antes de eu retomar — mantive a implementação deles, que é mais robusta que a minha tentativa anterior (evita bundlar fonte extra no repo).
- **Arquivos sob responsabilidade:** `ferramentas/`, `site/`, `.github/`, PDFs finais em `site/public/pdfs/`, integração do inventário.

**Estado consolidado do projeto:**
- Acervo oficial 2008–2026: 116/116 PDFs baixados, validados, inventariados (0 falhas). 2002–2007 ausentes do acervo oficial (pendentes, regra D7).
- Formatos históricos confirmados: 2008–2018 provas por matéria (Q1–20 objetivas com gabarito oficial; Q21–30 dissertativas sem resposta oficial → Caso 2); 2019–2026 1ª fase objetiva (Caso 1) + 2ª fase discursiva (Caso 2), Redação 2019–2024, Português na 2ª fase 2025–2026 com `gabarito_<ano>_2f.pdf`.
- **16 PDFs finais publicados:** 1ª fase 2019–2026 (8, Caso 1), Português e Redação 2ª fase 2025–2026 (2, Caso 1), discursivas 2017–2018 Matemática/Física/Química (6, Caso 2).
- Poliedro verificado: cobertura pública 2017–2026; link direto por prova = página da 1ª questão + `#exam-downloads` (download sem cadastro). Dissertativas 2008–2016 sem fonte pública no Poliedro (lacuna registrada).
- Site Astro publicado em `https://joaopaulolondeabreu.github.io/revis-o-ita/` (GitHub Pages ativo, workflow manual).

**Próxima dependência:** pacote do Codex para o PEDIDO 3 (2ª fases 2019–2026, começando por 2026, conforme fila em PEDIDOS_PARA_CODEX.md).

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
