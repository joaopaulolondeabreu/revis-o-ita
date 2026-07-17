# Pedidos de Claude (líder técnico) para o Codex (preparação)

Formato obrigatório dos pacotes: ver DECISOES.md **D10** (JSON `pacote.json` em
`docs/coordenacao/pacotes/<nome-do-pacote>/`). Não alterar código, scripts,
site nem PDFs finais. Registrar cada entrega em `ENTREGAS_DO_CODEX.md`.

---

## PEDIDO 1 — Auditoria dos materiais 2008–2026 (sem novos downloads)
**Registrado em:** 2026-07-17 (America/Sao_Paulo) — Claude
**Prioridade:** alta • **Estado:** ATENDIDO (pacote auditoria-2008-2026; validado e aprovado por Claude em 2026-07-17)

Conferir, item a item do `INVENTARIO_ITA.csv`, se cada PDF em
`arquivos/originais/ita/<ano>/` corresponde mesmo à instituição/ano/fase/matéria
declarados (abrir e olhar a 1ª página; NÃO rebaixar nada). Saída: pacote
`auditoria-2008-2026` contendo somente a lista de divergências encontradas
(arquivo, campo errado, valor correto, evidência) ou a declaração "sem divergências".

## PEDIDO 2 — Pacote das discursivas ITA 2017 e 2018
**Registrado em:** 2026-07-17 (America/Sao_Paulo) — Claude
**Prioridade:** alta • **Estado:** ATENDIDO E TOTALMENTE INTEGRADO (pacote concluído em 2026-07-17; integrador reprojetado para granularidade por questão em 2026-07-17 — ver DECISOES.md D14 — e as 6 provas de Matemática/Física/Química 2017–2018 estão publicadas, com 49 respostas reais e 11 usando a frase padrão do plano)

Para cada prova por matéria de 2017 e 2018 (Matemática, Física, Química —
questões 21–30 dissertativas; conferir se Português/Inglês têm parte dissertativa):
1. URL direta do Poliedro no formato verificado
   `…/vestibulares/ita/<ano>/<slug>/<slug-da-primeira-questao>#exam-downloads`
   (slugs já mapeados em URLS_CANDIDATAS.md), testada com HTTP 200;
2. baixar a resolução do Poliedro APENAS para consulta local em
   `docs/coordenacao/pacotes/<pacote>/consulta/` — **esta pasta não pode ser
   commitada** (adicionar entrada no .gitignore do pacote); registrar URL e data;
3. tabela de respostas finais mínimas por questão (somente o resultado final
   explicitamente declarado pelo Poliedro; regras da seção 16 do plano; para
   "demonstre/prove" sem resultado separável usar exatamente a frase padrão);
4. para cada resposta: página/posição na resolução onde o resultado aparece
   (evidência para minha conferência visual);
5. status por item e pendências.

Saída: pacote `discursivas-2017-2018` no formato D10.

## PEDIDO 3 — Pacotes das 2ª fases 2019–2026 (após o PEDIDO 2)
**Registrado em:** 2026-07-17 — Claude • **Estado:** ABERTO (fila)

Mesmo formato do PEDIDO 2, um pacote por ano, começando por 2026 e voltando.
Atenção: casos "Resolução pendente" no Poliedro → item `pendente`, sem inventar.

## PEDIDO 4 — Pesquisa documentada 2002–2007
**Registrado em:** 2026-07-17 — Claude • **Estado:** ATENDIDO (pacote fontes-2002-2007; decisão do Claude: manter os 6 anos pendentes, nada de ingestão sem procedência/autorização comprovadas)

Procurar fonte oficial ou cópia pública confiável das PROVAS 2002–2007
(regra D7). Registrar cada página verificada, mesmo sem sucesso. Nada de
formulários/termos/bloqueios. Saída: pacote `fontes-2002-2007` com achados,
URLs, e lacunas objetivas.

## PEDIDO 5 — Contato com o ITA sobre o acervo 2002–2007 (baixa prioridade, aguardando decisão do usuário)
**Registrado em:** 2026-07-17 — Claude • **Estado:** EM ESPERA

Preparar (NÃO enviar) uma minuta de e-mail institucional para a organização do
vestibular do ITA perguntando se as provas de 2002–2007 podem ser
disponibilizadas ou autorizadas. O envio, se acontecer, será feito pelo
usuário, com os dados de contato dele — nunca pelos agentes.
