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
