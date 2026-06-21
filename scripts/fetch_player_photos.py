import json, time, urllib.parse, urllib.request

PLAYERS = [
 ("Lionel Messi","ARG"),
 ("Jonathan David","CAN"),
 ("Kylian Mbappé","FRA"),
 ("Erling Haaland","NOR"),
 ("Kai Havertz","GER"),
 ("Harry Kane","ENG"),
 ("Folarin Balogun","USA"),
 ("Elijah Just","NZL"),
 ("Yasin Ayari","SWE"),
 ("Matheus Cunha","BRA"),
 ("Vinícius Júnior","BRA"),
 ("Ismael Saibari","MAR"),
 ("Brian Brobbey","NED"),
 ("Cody Gakpo","NED"),
 ("Deniz Undav","GER"),
 ("Viktor Gyökeres","SWE"),
 ("Jamal Musiala","GER"),
 ("Cyle Larin","CAN"),
 ("Raúl Jiménez","MEX"),
 ("Alexander Isak","SWE"),
 ("Mohammad Mohebi","IRN"),
 ("Matías Galarza","PAR"),
 ("Anthony Elanga","SWE"),
 ("Franck Kessié","CIV"),
]

HEADERS = {"User-Agent": "Simulador-Hawelligton-Copa2026/1.0 (educational project; contact: example@example.com)"}

def http_get_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))

VERIFY_WORDS = ["footballer","football player","midfielder","forward","defender","goalkeeper","striker","winger"]

def try_wikipedia(title, lang="en"):
    url = (f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}"
           "&prop=pageimages|extracts&exintro=1&explaintext=1&piprop=thumbnail|name&pithumbsize=500"
           "&redirects=1&format=json&origin=*")
    try:
        data = http_get_json(url)
    except Exception:
        return None
    pages = data.get("query", {}).get("pages", {})
    for pid, page in pages.items():
        if pid == "-1":
            return None
        extract = (page.get("extract") or "").lower()
        thumb = page.get("thumbnail", {}).get("source")
        if not thumb:
            return None
        verified = any(w in extract for w in VERIFY_WORDS)
        return {"thumb": thumb, "verified": verified, "title": page.get("title"), "extract_snip": extract[:140]}
    return None

results = {}
for name, code in PLAYERS:
    found = None
    for attempt_title in [name, f"{name} (footballer)"]:
        for lang in ["en"]:
            r = try_wikipedia(attempt_title, lang)
            if r and r["verified"]:
                found = r
                break
        if found:
            break
        time.sleep(0.2)
    if found:
        results[name] = {"photo": found["thumb"], "wiki_title": found["title"]}
        print(f"OK  {name:25s} -> {found['title']}  | {found['extract_snip'][:60]}")
    else:
        # tenta sem verificacao estrita como ultimo recurso, mas marca como nao verificado
        r2 = try_wikipedia(name, "en")
        if r2 and r2["thumb"]:
            results[name] = {"photo": r2["thumb"], "wiki_title": r2["title"], "unverified": True}
            print(f"?-  {name:25s} -> {r2['title']} (NAO VERIFICADO: {r2['extract_snip'][:70]})")
        else:
            results[name] = {"photo": None}
            print(f"--  {name:25s} -> nao encontrado")
    time.sleep(0.3)

with open("/home/claude/photo-fetch/results2.json","w",encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
