# STATUS

Regra: cada agente edita SOMENTE a sua seção. Não reformatar a seção do outro.

---

### Claude

- **Atualizado em:** 2026-07-17 (America/Sao_Paulo)
- **Papel:** líder técnico (decisões, código, PDFs finais, site, testes, publicação, integração) — ver DECISOES.md D12.
- **Tarefa atual:** integração das entregas do Codex (PEDIDOS 1 e 4) e construção do integrador automático de pacotes — estado: EM_ANDAMENTO.
- **Concluído antes:** Português e Redação 2ª fase 2025/2026 montados e validados; 10 PDFs finais no site.
- **Decisões de integração (2026-07-17):** auditoria APROVADA (reconferida por amostragem); recomendação do pacote fontes-2002-2007 ACEITA — 6 anos permanecem pendentes, nada será ingerido sem procedência/autorização; fontes registradas em FONTES.md como referência apenas.
- **Arquivos sob responsabilidade:** `ferramentas/`, `site/`, `.github/`, PDFs finais em `site/public/pdfs/`, integração do inventário.

**Estado consolidado do projeto:**
- Acervo oficial 2008–2026: 116/116 PDFs baixados, validados, inventariados (0 falhas). 2002–2007 ausentes do acervo oficial (pendentes, regra D7).
- Formatos históricos confirmados: 2008–2018 provas por matéria (Q1–20 objetivas com gabarito oficial; Q21–30 dissertativas sem resposta oficial → Caso 2); 2019–2026 1ª fase objetiva (Caso 1) + 2ª fase discursiva (Caso 2), Redação 2019–2024, Português na 2ª fase 2025–2026 com `gabarito_<ano>_2f.pdf`.
- PDFs finais prontos: 1ª fase 2019–2026 (8), Caso 1, validados com fidelidade visual.
- Poliedro verificado: cobertura pública 2017–2026; link direto por prova = página da 1ª questão + `#exam-downloads` (download sem cadastro). Dissertativas 2008–2016 sem fonte pública no Poliedro (lacuna registrada).
- Site Astro funcional (28 páginas); publicação via workflow manual apenas; pré-visualização depende de o usuário ativar o GitHub Pages.

**Próxima dependência:** pacotes do Codex (PEDIDOS 1 e 2 em PEDIDOS_PARA_CODEX.md).

---

### Codex

- **Atualizado em:** 2026-07-17 01:50 (America/Sao_Paulo)
- **Papel nesta etapa:** finalização técnica assumida a pedido explícito do usuário após o encerramento da sessão do Claude; a seção do Claude foi preservada sem alterações.
- **Tarefa:** integrar o PEDIDO 2, corrigir bloqueios de publicação, validar e publicar o site.
- **Estado:** CONCLUÍDO; PUBLICAÇÃO AUTORIZADA PELO USUÁRIO E EM DISPARO.
- **Integração do PEDIDO 2:** Matemática 2018, único item integralmente `pronto`, foi integrada em PDF final de 10 páginas. As outras cinco provas continuam pendentes porque contêm respostas exclusivamente gráficas/estruturais, ausência de resultado separável ou inconsistência da própria fonte; nada foi deduzido.
- **Correções técnicas:** compatibilidade do integrador com Windows; registros idempotentes; dependência `tzdata`; quebra de linhas e fontes Unicode nos PDFs; regeneração validada dos 10 PDFs finais anteriores; Astro atualizado para 7.1.0, com auditoria npm em 0 vulnerabilidades.
- **Validações:** teste de fumaça completo; fidelidade visual das páginas oficiais; QR decodificado; 11 PDFs finais válidos; build estático de 28 páginas; simulação do GitHub Pages com base `/revis-o-ita`; página inicial, ano 2018 e download do PDF respondendo HTTP 200; navegador sem erros.
- **Próxima fila após a publicação:** PEDIDO 3, começando pelo pacote da 2ª fase de 2026.
