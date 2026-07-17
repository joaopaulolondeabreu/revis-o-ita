# Decisões técnicas

## 2026-07-16 22:36 (America/Sao_Paulo) — Claude

### D1 — Site estático com Astro
Site gerado estaticamente (HTML puro) com Astro. Motivo: máxima velocidade no celular, custo zero, sem servidor/banco de dados para manter ou invadir, fácil manutenção por agentes. Arquitetura preparada para crescer (futuras instituições e, muito depois, simulados) sem refazer nada.

### D2 — Processamento de PDFs em Python
`pypdf` (anexação de páginas), `reportlab` (páginas de proteção e seção de respostas complementares), `qrcode` + `Pillow` (QR local, sem serviço externo), `pypdfium2` (renderização para conferência visual), `opencv-python-headless` (decodificação reversa dos QR Codes para teste), `hashlib` (SHA-256).

### D3 — Compromisso de fidelidade dos PDFs (ajuste do usuário, 2026-07-16)
Os PDFs **originais** são preservados intactos em `arquivos/originais/`, com SHA-256 no inventário. Os PDFs **finais montados** podem não ser byte a byte idênticos internamente; o compromisso é: páginas da prova **visualmente intactas**, sem corte, sem redigitação, sem alteração de conteúdo, com **conferência por renderização** (comparação visual das páginas do original × final).

### D4 — Hospedagem no GitHub Pages
Gratuito, sem nova conta, HTTPS automático, CDN. Publicação em duas etapas: pré-visualização (endereço não divulgado) → aprovação explícita do usuário → divulgação definitiva. Nenhum link é divulgado aos alunos antes da aprovação (ajuste do usuário, 2026-07-16).

### D5 — Armazenamento dos PDFs: decisão adiada até medição real (ajuste do usuário, 2026-07-16)
A decisão de manter os PDFs dentro do repositório GitHub **só será tomada após baixar os primeiros arquivos e medir o tamanho real** (estimativa extrapolada para as 25 edições). Se houver risco de repositório pesado, o armazenamento dos PDFs será separado do site desde cedo (por exemplo, Cloudflare R2), sem esperar chegar perto de 1 GB. O catálogo referencia os PDFs por URL, então a migração não altera site, IDs nem inventário.

**Fechamento (2026-07-17, Claude, após medição real):** os 116 PDFs oficiais de 2008–2026 somam **90 MB** (maior arquivo: 18 MB). Com os PDFs finais montados, a projeção do projeto ITA completo fica em ~200–250 MB — confortável para o repositório. **Decisão: manter os PDFs no GitHub.** A rota de migração para armazenamento separado continua documentada para quando outras instituições forem adicionadas.

### D6 — Fonte única de dados
`docs/coordenacao/INVENTARIO_ITA.csv` → `ferramentas/catalogo.py` → `site/src/data/catalogo.json` → páginas do site. Nada é cadastrado duas vezes.

### D7 — Anos 2002–2007 (ajuste do usuário, 2026-07-16)
Se o material não estiver no acervo oficial do ITA, priorizar fonte oficial ou cópia pública confiável da própria prova. Se a única fonte for o Poliedro, registrar origem e situação de autorização no inventário antes de hospedar qualquer PDF derivado. Resoluções completas do Poliedro nunca são hospedadas, em hipótese nenhuma.

### D8 — Identificadores estáveis
`ita-<ano>-<fase|materia>[-<dia>]` (ex.: `ita-2026-fase1`, `ita-2018-fisica`). Metadados por documento: instituição, ano, formato histórico, fase, dia, matéria, tipo, fontes (URLs, oficial/não, data, hash, páginas), situação, caso de gabarito (1 = só oficial / 2 = com Poliedro).

### D9 — Identidade de commits
Commits com autoria neutra ("Claude <noreply@anthropic.com>"), sem dados pessoais do usuário no histórico do Git (ajuste do usuário, 2026-07-16).

## 2026-07-17 (America/Sao_Paulo) — Claude

### D10 — Formato único dos pacotes do Codex
Cada pacote = uma pasta `docs/coordenacao/pacotes/<nome-do-pacote>/` contendo um único **`pacote.json`** (UTF-8) e, quando necessário, subpasta `consulta/` (materiais do Poliedro só para leitura — **nunca commitados**; cobertos por `.gitignore`). Esquema do `pacote.json`:

```json
{
  "pacote": "discursivas-2017-2018",
  "preparado_por": "Codex",
  "data": "2026-07-17T10:00-03:00",
  "itens": [
    {
      "id": "ita-2017-matematica",
      "ano": "2017", "fase": "prova por matéria", "dia": "", "materia": "Matemática",
      "pdf_original": "arquivos/originais/ita/2017/matematica_2017.pdf",
      "gabarito_oficial": "arquivos/originais/ita/2017/gabarito_2017.pdf",
      "sha256_original": "…", "num_paginas_original": 6,
      "url_pagina_origem": "https://www.vestibular.ita.br/provas.htm",
      "url_arquivo": "https://www.vestibular.ita.br/provas/matematica_2017.pdf",
      "poliedro": {
        "url_direta": "https://poliedroresolve.sistemapoliedro.com.br/vestibulares/ita/2017/matematica-7/questao-1-geral-matematica-ita-2017#exam-downloads",
        "http_status_verificado": 200,
        "verificado_em": "2026-07-17",
        "arquivo_consulta": "consulta/…pdf (não commitado)"
      },
      "respostas": [
        {"questao": "21", "resposta": "n = 100", "evidencia": "resolução, pág. 3, fim da questão 21", "url_fonte": "…", "conferida_por_codex": true, "obs": ""}
      ],
      "status": "pronto",
      "observacoes": ""
    }
  ],
  "pendencias": ["…"]
}
```
Campos de resposta seguem as regras da seção 16 do plano (transcrição mínima; frase padrão para questões sem resultado separável; "Não possui resposta única — produção textual." para redação). O QR Code é gerado e testado pelo pipeline do Claude a partir de `url_direta` — o Codex não precisa gerar PNG, apenas garantir que a URL é exata e responde 200.

### D11 — Redação e observações no PDF final
Provas cujo caderno inclui redação recebem, após o gabarito oficial, uma página de observação com título neutro (ex.: "OBSERVAÇÃO SOBRE A REDAÇÃO") registrando "Não possui resposta única — produção textual.". A seção com título "RESPOSTAS FINAIS COMPLEMENTARES — FONTE: POLIEDRO RESOLVE" fica reservada a conteúdo efetivamente conferido no Poliedro.

### D12 — Divisão de trabalho (definida pelo usuário em 2026-07-17)
Claude = líder técnico (código, PDFs finais, site, testes, publicação, integração, decisões). Codex = preparação (fontes, downloads permitidos, inventário, links diretos, respostas mínimas com evidência), sem alterar implementação. Esteira: Codex prepara N+1 enquanto Claude implementa N. Claude não interrompe tarefa técnica para caçar insumo: registra em PEDIDOS_PARA_CODEX.md e segue.
