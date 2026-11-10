import json, os, time, datetime, urllib.request, urllib.parse
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TIPOS = "(meta-analysis[pt] OR systematic review[pt] OR review[pt] OR randomized controlled trial[pt] OR practice guideline[pt])"
DAYS = int(os.environ.get("DAYS") or 10)
MAX = 15

def get(path, **p):
    p.update(retmode="json", tool="movh-leituras")
    url = BASE + path + "?" + urllib.parse.urlencode(p)
    err = None
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "movh-leituras/1.0"}), timeout=40) as r:
                return json.load(r)
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    raise err

queries = json.load(open("queries.json", encoding="utf-8"))
seen = set(json.load(open("seen.json"))["pmids"])
hoje = datetime.date.today().isoformat()
blocos, novos = [], 0
for area, q in queries.items():
    r = get("esearch.fcgi", db="pubmed", term="(%s) AND %s" % (q, TIPOS), reldate=DAYS, datetype="edat", retmax=MAX, sort="date")
    ids = [i for i in r["esearchresult"].get("idlist", []) if i not in seen]
    time.sleep(0.5)
    if not ids:
        continue
    s = get("esummary.fcgi", db="pubmed", id=",".join(ids))["result"]
    time.sleep(0.5)
    linhas = []
    for i in ids:
        d = s.get(i)
        if not d:
            continue
        aut = (d.get("authors") or [{}])[0].get("name", "?")
        doi = next((a["value"] for a in d.get("articleids", []) if a.get("idtype") == "doi"), "")
        ano = (d.get("pubdate") or "")[:4]
        tipo = ", ".join(d.get("pubtype", [])[:2])
        linhas.append("- [ ] **%s** %s et al., %s (%s). %s. PMID %s%s. https://pubmed.ncbi.nlm.nih.gov/%s/" % (
            d.get("title", "").rstrip("."), aut, d.get("source", ""), ano, tipo, i, (" doi:" + doi) if doi else "", i))
        seen.add(i); novos += 1
    if linhas:
        blocos.append("### " + area + "\n" + "\n".join(linhas))
if blocos:
    atual = open("inbox.md", encoding="utf-8").read() if os.path.exists("inbox.md") else ""
    cab, _, corpo = atual.partition("\n---\n")
    if not cab.strip():
        cab = "# Inbox de leituras do MOVH\nCandidatas automáticas (PubMed; revisões, meta-análises, ensaios). Nada aqui é verificado: revisar com o professor, aprovar ou descartar e só então passar para `docs/base-teorica.md` do MovhGen."
    novo = "## %s (%d novas, últimos %d dias)\n%s" % (hoje, novos, DAYS, "\n\n".join(blocos))
    open("inbox.md", "w", encoding="utf-8").write(cab.rstrip() + "\n---\n" + novo + "\n\n" + corpo.lstrip("\n"))
    json.dump({"pmids": sorted(seen)}, open("seen.json", "w"))
print("novas:", novos)
