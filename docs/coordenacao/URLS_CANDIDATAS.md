# URLs candidatas (descobertas por busca na web — AINDA NÃO VERIFICADAS)

**Atenção:** tudo nesta página foi encontrado por busca na web em 2026-07-16/17
(America/Sao_Paulo), pois a rede do ambiente ainda bloqueia o acesso direto às
fontes. **Nenhuma URL daqui entra no inventário como `encontrado` sem download
direto, validação e hash.** Padrões podem variar entre anos.

## Acervo oficial do ITA — padrões observados

Base: `https://www.vestibular.ita.br/provas/`

| Material | Padrão observado | Exemplos confirmados pela busca |
|---|---|---|
| Prova 1ª fase | `<ano>_fase1.pdf` | `2026_fase1.pdf`, `2025_fase1.pdf`, `2024_fase1.pdf`, `2023_fase1.pdf`, `2021_fase1.pdf` |
| Prova 2ª fase por matéria | `<materia>_<ano>_2f.pdf` | `portugues_2026_2f.pdf` |
| Gabarito (geral/1ª fase ou por matéria) | `gabarito_<ano>.pdf` | `gabarito_2026.pdf`, `gabarito_2025.pdf`, `gabarito_2024.pdf`, `gabarito_2023.pdf`, `gabarito_2012.pdf` |
| Gabarito 2ª fase | `gabarito_<ano>_2fase.pdf` | `gabarito_2025_2fase.pdf` |

Conclusões provisórias (a confirmar no acesso direto):
- O acervo oficial cobre pelo menos até **2012** (existe `gabarito_2012.pdf`), coerente com a estimativa "2008–2026".
- A página índice é `https://www.vestibular.ita.br/provas.htm` — mapear a lista completa por lá, não por adivinhação de padrões.

## Poliedro Resolve — estrutura VERIFICADA (acesso direto em 2026-07-16/17)

- Página do ITA: `https://poliedroresolve.sistemapoliedro.com.br/vestibulares/ita`
- **Cobertura pública: ITA 2017 a 2026.** Não há listagem pública de 2016 para trás — lacuna registrada para as dissertativas de 2008–2016.
- A URL `…/ita/<ano>/<slug-da-prova>/` SEM o slug de questão responde **404**. A página funcional é a da questão: `…/ita/<ano>/<slug-da-prova>/<slug-da-questao>`.
- Cada página de questão contém a seção **Downloads** (âncora `#exam-downloads`) com a prova original e as **resoluções em PDF por matéria**, para download imediato e **sem cadastro**.
- **Formato do link direto para o Caso 2** (testado e funcionando):
  `…/ita/<ano>/<slug-da-prova>/<slug-da-primeira-questao>#exam-downloads`
  Exemplo verificado (ITA 2024, 2ª fase dia 1): a seção Downloads lista "ITA 2024 - 2ª Fase Dia 1 - Resoluções - Matemática.pdf" e "…Química.pdf".
- Observação: em provas muito recentes pode aparecer "Resolução pendente" (o Poliedro ainda não publicou) — nesse caso o item fica `pendente` no nosso inventário.
- Slugs por prova (capturados da página do ITA em 2026-07-16): 2017–2018 por matéria (`matematica-7`, `fisica-5`, `portugues-e-ingles`, …); 2019–2026 por fase/dia (`ita-1-fase-…`, `ita-2-fase-dia-1-…`, …). Lista completa no histórico desta sessão e recuperável da própria página do ITA.
- Os PDFs de resolução podem ser **consultados** para transcrever resultados finais, mas **nunca** hospedados ou copiados para o repositório (regra FONTES.md).

## Fontes terciárias vistas na busca (usar só como último recurso, com registro de autorização)

- `cosseno.com/provas-anteriores/ITA`
- `quimicaparaovestibular.com.br` e `sotaodaquimica.com.br` (afirmam colaboração com COMAER/ITA)
- `projetoagathaedu.com.br` (anos ~2010–2023)

Para 2002–2007: priorizar fonte oficial ou cópia pública confiável da própria prova (regra D7 em DECISOES.md).
