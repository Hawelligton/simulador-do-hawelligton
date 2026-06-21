# Rotinas de busca de fotos dos artilheiros

Duas rotinas disponíveis para preencher `data/player_photos*.json` (o app lê
apenas a URL da foto desses arquivos — nunca a imagem em si):

## 1. `fetch_player_photos_apifootball.py` (fonte ativa no app)

Consulta `GET /players/profiles?search=<sobrenome>` na API do api-football
(api-sports.io). Esse endpoint não tem a restrição de temporada que os jogos
têm no plano Free (que só libera 2022–2024) — perfil e foto do jogador
funcionam mesmo no plano gratuito. Como a busca por sobrenome pode trazer
homônimos, o resultado é filtrado pela nacionalidade esperada de cada
artilheiro. Requer uma chave de API (`x-apisports-key`) — configure em
`API_KEY` no topo do script.

## 2. `fetch_player_photos.py` (fonte alternativa)

Consulta a API da Wikipedia (que serve fotos hospedadas no Wikimedia
Commons). Não exige chave/cadastro. O texto inicial do artigo é checado em
busca de palavras como "footballer" antes de aceitar a foto, pra evitar
pegar um homônimo.

## Como rodar

```bash
python3 fetch_player_photos_apifootball.py
# ou
python3 fetch_player_photos.py
```

## Licença das imagens

- api-football: fotos de uso editorial dentro dos termos do serviço da API.
- Wikimedia Commons: domínio público ou licenças Creative Commons.
