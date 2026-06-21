"""
Rotina que monta a base de convocacoes das 48 selecoes da Copa 2026.

Fonte primaria: api-football (players/squads?team=ID) - traz nome, idade,
posicao e FOTO oficial do jogador em uma unica chamada por selecao.

Fonte de reserva (quando o plano gratuito da api-football estoura o limite
diario de 100 requisicoes): pagina "2026 FIFA World Cup squads" da Wikipedia,
que lista as 48 convocacoes oficiais em wikitext estruturado (nome, posicao,
clube - sem foto; o app usa a bandeira da selecao como substituto visual).

Os tecnicos (nome + foto) de todas as 48 selecoes vem da Wikipedia via
pageimages, independente da fonte usada para o elenco.

Saida: squads-data.js (const SQUADS = {...}), carregado pelo index.html
antes do script principal.
"""
# Ver fetch_squads.py original em /home/claude/squads/ (script de execucao
# completo, com paginacao/retentativas) - aqui documentamos apenas a logica.
print("Consulte o histórico de execução; este arquivo documenta a fonte de dados.")
