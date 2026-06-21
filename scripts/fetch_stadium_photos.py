"""
Rotina que consulta a API da Wikipedia (imagens hospedadas no Wikimedia Commons)
pelo nome de cada estadio da Copa 2026 e retorna a URL da foto principal do
artigo (curada pelos editores, no infobox).

Antes de aceitar a foto, o texto inicial do artigo e checado em busca de
palavras como "stadium"/"arena"/"estadio", para confirmar que e mesmo o local
certo. Armazena apenas a URL em data/stadium_photos.json - nunca a imagem em si.
"""
import json, time, urllib.parse, urllib.request

HEADERS = {"User-Agent": "Simulador-Hawelligton-Copa2026/1.0 (educational project; contact: example@example.com)"}

STADIUMS = [
    "MetLife Stadium", "AT&T Stadium", "SoFi Stadium", "Mercedes-Benz Stadium",
    "Lumen Field", "Levi's Stadium", "Lincoln Financial Field", "Arrowhead Stadium",
    "NRG Stadium", "Hard Rock Stadium", "Gillette Stadium", "Estadio Azteca",
    "Estadio Akron", "Estadio BBVA", "BC Place", "BMO Field",
]

VERIFY_WORDS = ["stadium", "arena", "ballpark", "stade", "estadio", "estádio"]


def http_get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch(title, lang="en"):
    url = (f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}"
           "&prop=pageimages|extracts&exintro=1&explaintext=1&piprop=thumbnail&pithumbsize=900"
           "&redirects=1&format=json&origin=*")
    data = http_get_json(url)
    pages = data.get("query", {}).get("pages", {})
    for pid, page in pages.items():
        if pid == "-1":
            return None
        extract = (page.get("extract") or "").lower()
        thumb = page.get("thumbnail", {}).get("source")
        if not thumb:
            return None
        if any(w in extract for w in VERIFY_WORDS):
            return thumb
    return None


def main():
    results = {}
    for name in STADIUMS:
        results[name] = fetch(name)
        print(name, "->", "OK" if results[name] else "NAO ENCONTRADO")
        time.sleep(0.5)
    with open("../data/stadium_photos.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
