# Coordenação entre agentes (Claude e Codex)

Regras de colaboração para todo agente que trabalhar neste repositório.

## Antes de iniciar qualquer trabalho

1. Ler toda a documentação desta pasta (`STATUS.md`, `DECISOES.md`, `PROBLEMAS.md`, `FONTES.md`, `HANDOFF.md`).
2. Verificar o estado atual do repositório (`git status`, `git log`).
3. Verificar alterações ainda não finalizadas.
4. Não refazer trabalho já concluído.
5. Registrar em `STATUS.md` a tarefa que pretende executar.

## A cada atualização, registrar

- data e hora no fuso **America/Sao_Paulo**;
- agente responsável: Claude ou Codex;
- tarefa realizada;
- arquivos alterados;
- resultado;
- problemas encontrados e como foram resolvidos;
- pendências;
- próxima ação recomendada.

## Regras invioláveis do projeto

1. **Dados pessoais:** nenhum nome, telefone ou e-mail do usuário em código, commits, logs, inventário, PDFs, site, capturas de tela ou documentação. Nenhuma senha, token ou chave em nenhum documento.
2. **Provas originais:** os PDFs de origem ficam intactos em `arquivos/originais/`, com SHA-256 registrado no inventário. Nos PDFs finais montados, as páginas da prova devem permanecer **visualmente intactas** — sem corte, sem redigitação, sem alteração de conteúdo, ordem ou numeração — com conferência por renderização (o arquivo final pode não ser byte a byte idêntico internamente; a fidelidade exigida é visual e de conteúdo).
3. **Gabarito oficial do ITA:** prioridade absoluta; anexado integralmente, nunca redigitado ou reformatado; divergências com outras fontes mantêm o oficial e são registradas.
4. **Poliedro Resolve:** nunca copiar ou hospedar resoluções completas, demonstrações, explicações, imagens, vídeos ou identidade visual. Uso permitido: transcrição mínima do resultado final explícito de discursivas não cobertas oficialmente, com crédito, link direto e QR Code. Nunca contornar cadastro/CAPTCHA/bloqueios nem aceitar termos em nome do usuário.
5. **Respostas:** nenhum agente resolve, deduz, resume ou redige respostas. Só transcrição fiel do resultado final explícito da fonte, com conferência visual caractere a caractere (nunca confiar só em OCR para fórmulas). Segunda conferência por outro agente apenas compara transcrição × fonte, sem resolver.
6. **Materiais ausentes:** tentativas razoáveis, registro das páginas verificadas, marcação `ausente`/`pendente` e seguir em frente. Nunca inventar arquivos, respostas ou URLs.
7. **Anos 2002–2007 (fora do acervo oficial):** priorizar fonte oficial ou cópia pública confiável da própria prova. Se a única fonte for o Poliedro, registrar claramente origem e situação de autorização no inventário **antes** de hospedar qualquer PDF derivado.
8. **Fonte única de dados:** `INVENTARIO_ITA.csv` alimenta o catálogo do site (`ferramentas/catalogo.py`). Não cadastrar as mesmas informações manualmente em outros lugares.
9. **Publicação:** primeiro pré-visualização para o usuário testar; publicação/divulgação definitiva somente após aprovação explícita dele. O IME e demais instituições só começam com autorização explícita.
10. **Escopo atual:** somente ITA 2026–2002. Não extrair questões individuais nesta etapa.

## Arquivos desta pasta

| Arquivo | Função |
|---|---|
| `STATUS.md` | Situação atual e próxima tarefa |
| `DECISOES.md` | Decisões técnicas e justificativas |
| `PROBLEMAS.md` | Erros, causas e soluções |
| `FONTES.md` | Fontes utilizadas e regras de atribuição |
| `INVENTARIO_ITA.csv` | Inventário completo dos materiais (fonte única da verdade) |
| `RESPOSTAS_COMPLEMENTARES.csv` | Registro interno das respostas finais transcritas |
| `HANDOFF.md` | Resumo para o próximo agente |
