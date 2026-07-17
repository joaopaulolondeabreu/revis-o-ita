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

- **Atualizado em:** 2026-07-17 01:10 (America/Sao_Paulo)
- **Papel:** preparação de fontes e metadados, conforme D12; sem alterações em código, site, PDFs finais, catálogo ou seção do Claude.
- **Tarefa concluída:** PEDIDO 2 — pacote `discursivas-2017-2018` preparado no formato D10.
- **Estado:** CONCLUÍDO COM PENDÊNCIAS DOCUMENTADAS.
- **Resultado:** 6 páginas e 6 PDFs públicos do Poliedro verificados com HTTP 200; 60 questões conferidas visualmente; 49 respostas finais prontas e 11 questões pendentes ou parciais por dependerem de gráfico/diagrama/fórmula estrutural, por ausência de resultado separável ou por inconsistência explícita da fonte. Português e Inglês de 2017–2018 foram confirmados como objetivos, cobertos pelo gabarito oficial; a redação separada recebeu somente a frase padrão.
- **Arquivos entregues:** `docs/coordenacao/pacotes/discursivas-2017-2018/pacote.json` e registro em `docs/coordenacao/ENTREGAS_DO_CODEX.md`. Os seis PDFs de consulta estão em `consulta/`, ignorados pelo Git e não commitados.
- **Próxima fila:** PEDIDO 3, começando por 2026, somente após o handoff desta entrega.
