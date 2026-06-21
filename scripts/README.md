# Rotina de busca de fotos (Wikimedia)

`fetch_player_photos.py` consulta a API da Wikipedia/Wikimedia (que serve as imagens
diretamente do Wikimedia Commons, em `upload.wikimedia.org`) para cada artilheiro
cadastrado e retorna a URL da melhor foto disponível.

## Por que via Wikipedia e não busca direta no Commons?

A busca textual direta na API do Commons (`action=query&generator=search` no namespace
de arquivos) é ruidosa: para nomes comuns ela pode retornar fotos de outras pessoas,
times, ou arquivos sem relação alguma (ex.: já aconteceu de devolver uma foto de luta
livre para "Jonathan David"). Por isso a rotina usa o endpoint `pageimages` da própria
Wikipedia, que devolve a foto de capa (infobox) **curada pelos editores** para o artigo
daquela pessoa — e essa imagem já está hospedada nos servidores do Wikimedia Commons.
Antes de aceitar o resultado, o texto inicial do artigo é checado em busca de palavras
como "footballer"/"midfielder"/"forward" etc., para confirmar que é mesmo a pessoa certa
(evita pegar um homônimo).

## Como rodar

```bash
python3 fetch_player_photos.py
```

Gera `results2.json` com `{ "Nome do Jogador": { "photo": "url...", "wiki_title": "..." } }`.
O resultado consolidado de todos os 24 artilheiros está em `data/player_photos.json`,
na raiz do repositório — é o "banco de dados" usado pelo app: apenas a URL da imagem é
armazenada, nunca o arquivo em si.

## Licença das imagens

Todas as imagens vêm do Wikimedia Commons, que só hospeda conteúdo de uso livre
(domínio público ou licenças Creative Commons). Ainda assim, ao reutilizar este projeto
publicamente, vale checar a página de cada arquivo (`wiki_title`) para conferir o crédito
exigido pela licença específica.
