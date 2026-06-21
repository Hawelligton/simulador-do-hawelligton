"""
Rotina que consulta a API do api-football (api-sports.io) pelo nome de cada
artilheiro e retorna a URL da foto de perfil oficial do jogador.

Endpoint usado: GET /players/profiles?search=<sobrenome>
Esse endpoint NAO tem a restricao de temporada que o endpoint de fixtures tem no
plano Free (que so libera temporadas 2022-2024) - dados de perfil/foto do jogador
funcionam normalmente mesmo no plano gratuito.

Como a busca por sobrenome pode retornar varios homonimos, o resultado e
filtrado por nacionalidade esperada (e checado manualmente quando ha duvida,
ex.: sobrenomes comuns como "Cunha", "Galarza", "Jimenez").

Armazena apenas a URL da foto (https://media.api-sports.io/football/players/<id>.png)
em data/player_photos_apifootball.json - nunca a imagem em si.
"""
import json, time, urllib.parse, urllib.request

API_KEY = "COLOQUE_SUA_CHAVE_AQUI"  # https://dashboard.api-football.com
HEADERS = {"x-apisports-key": API_KEY}

# nome usado no app -> termo de busca (sobrenome, sem acentos quando necessario) -> nacionalidade esperada
PLAYERS = [
    ("Lionel Messi", "Messi", "Argentina"),
    ("Jonathan David", "David", "Canada"),
    ("Kylian Mbappé", "Mbappe", "France"),
    ("Erling Haaland", "Haaland", "Norway"),
    ("Kai Havertz", "Havertz", "Germany"),
    ("Harry Kane", "Kane", "England"),
    ("Folarin Balogun", "Balogun", "USA"),
    ("Elijah Just", "Just", "New Zealand"),
    ("Yasin Ayari", "Ayari", "Sweden"),
    ("Matheus Cunha", "Cunha", "Brazil"),
    ("Vinícius Júnior", "Vinicius", "Brazil"),
    ("Ismael Saibari", "Saibari", "Morocco"),
    ("Brian Brobbey", "Brobbey", "Netherlands"),
    ("Cody Gakpo", "Gakpo", "Netherlands"),
    ("Deniz Undav", "Undav", "Germany"),
    ("Viktor Gyökeres", "Gyokeres", "Sweden"),
    ("Jamal Musiala", "Musiala", "Germany"),
    ("Cyle Larin", "Larin", "Canada"),
    ("Raúl Jiménez", "Jimenez", "Mexico"),
    ("Alexander Isak", "Isak", "Sweden"),
    ("Mohammad Mohebi", "Mohebi", "Iran"),
    ("Matías Galarza", "Galarza", "Paraguay"),
    ("Anthony Elanga", "Elanga", "Sweden"),
    ("Franck Kessié", "Kessie", "Ivory Coast"),
]


def search(term):
    url = f"https://v3.football.api-sports.io/players/profiles?search={urllib.parse.quote(term)}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    results = {}
    for name, term, expected_nat in PLAYERS:
        data = search(term)
        candidates = [c["player"] for c in data.get("response", [])]
        # prioriza nacionalidade esperada; senao pega o primeiro
        best = next((p for p in candidates if p.get("nationality") == expected_nat), None) or (candidates[0] if candidates else None)
        results[name] = best["photo"] if best else None
        print(name, "->", results[name])
        time.sleep(3.5)  # plano Free tem limite curto de requisicoes por minuto

    with open("../data/player_photos_apifootball.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
