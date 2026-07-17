# Problemas, causas e soluções

## 2026-07-16 — Claude — Rede do ambiente bloqueia as fontes
- **Problema:** a política de rede do ambiente de execução nega conexão a `www.vestibular.ita.br` e `poliedroresolve.sistemapoliedro.com.br` (proxy responde 403 ao CONNECT).
- **Causa:** política de rede do ambiente Claude Code (não é bloqueio dos sites).
- **Solução:** o usuário precisa liberar os dois domínios (ou acesso amplo) nas configurações do ambiente em claude.ai/code. Instruções já enviadas ao usuário.
- **Situação:** pendente — bloqueia a verificação do acervo e toda a ingestão; não bloqueia a fundação do projeto.

## 2026-07-16 — Claude — `pypdf` falhava ao importar (`_cffi_backend` ausente)
- **Problema:** `import pypdf` quebrava com `ModuleNotFoundError: No module named '_cffi_backend'` (pacote `cryptography` do sistema Debian sem o backend cffi).
- **Solução:** `pip install --upgrade cffi cryptography` (o aviso de que o `cryptography` do Debian não pôde ser desinstalado é inofensivo — o `cffi` novo resolve).
- **Situação:** resolvido; teste de fumaça (`ferramentas/teste_fundacao.py`) passa por completo.
