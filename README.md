# movh-leituras
Busca semanal (segunda, 11h UTC) no PubMed por revisões, meta-análises e ensaios nas áreas do MOVH. Grava candidatas em `inbox.md`. Sem IA, sem custo.
- Áreas e buscas: `queries.json`. Rodar na hora: aba Actions → "Buscar leituras" → Run workflow (campo "dias").
- Curadoria mensal: colar o `inbox.md` na conversa do MOVH; aprovar/descartar; o aprovado vai para `docs/base-teorica.md` no MovhGen (com status de verificação). Regra nova só depois de entrar no CONTEXTO.md §0.

## Ativar a rotina semanal (1 passo, feito no site)
O token usado para criar este repo não tinha permissão de workflow. Abra `workflow/leituras.yml` → lápis (Edit) → no campo do nome troque para `.github/workflows/leituras.yml` → Commit. Depois: aba Actions → "Buscar leituras" → Run workflow (dias = 60) para a primeira carga.
