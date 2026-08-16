# Works out how many wrestlers each championship actually draws from, using EXACTLY the same
# rules the pickers use, and writes data/title_pools.json for the public book.
#
# Kenny 2026-08-16: Records & Stats was listing custom-roster BRANDS, so the main belts were
# missing entirely and DSEPW read 32 — the brand count — while the DSEPW Championship really
# draws from all 200 customs. The page says "Records & Stats", not "custom brands", so it lists
# every championship now and the numbers come from the same place the draws do.
import json, io, re, os

BOOK = r"F:\talkshow-podcast\wwe2k26\main_book"
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "title_pools.json")

sd  = json.load(io.open(BOOK + r"\app\season-tracker\season_data.json", encoding="utf-8"))
dr  = [w for w in json.load(io.open(BOOK + r"\default_roster.json", encoding="utf-8"))
       if not re.search(r" \(Lock\)$", w.get("name", ""))]
cu  = sd.get("customRoster") or []
rev = json.load(io.open(BOOK + r"\app\name-reviewer\reviewer_state.json", encoding="utf-8"))
eop = rev.get("empireOfPain") or []
st  = io.open(BOOK + r"\app\season-tracker\index.html", encoding="utf-8").read()

def name_list(const):
    m = re.search(r"const " + const + r"\s*=\s*\[([\s\S]*?)\];", st)
    if not m:
        return []
    return [a or b for a, b in re.findall(r"'([^']+)'|\"([^\"]+)\"", m.group(1))]

GIANTS = name_list("GIANTS_ROSTER")
FLYERS = name_list("HIGH_FLYERS_ROSTER")

teams = []
for p in (r"\app\wwe2k26tagteambuilder\teams_state.json", r"\teams_state.json"):
    try:
        teams = json.load(io.open(BOOK + p, encoding="utf-8"))
        break
    except Exception:
        pass

allr = dr + [c for c in cu if not any(d.get("name") == c.get("name") for d in dr)]
names = set(w.get("name") for w in allr)

OPEN = ["Undisputed WWE Championship", "WWE Intercontinental Championship",
        "WWE United States Championship", "Million Dollar Championship",
        "WWE Hardcore Championship"]
BRAND = {"Legends Championship": "Legend", "Horror Championship": "Horror",
         "Mortal Kombat Championship": "Mortal Kombat", "Princess Championship": "Princess",
         "Government Championship": "Government",
         "Superhero/Villain Championship": "Superhero/Villain",
         "Cartoons Championship": "Cartoons",
         "Internet Television Championship": "Internet Television",
         "Martial Arts Championship": "Martial Arts", "Elite Championship": "Elite"}

def pool_for(title):
    if title == "EOP Undisputed Ultraviolent Championship":
        return len(eop), "the Empire of Pain list"
    if title == "WWE Tag Team Championship":
        n = len([t for t in teams if t.get("name") and len(t.get("members") or []) >= 2])
        return n, "tag teams with two or more members"
    if title == "DSEPW Championship":
        return len([w for w in cu if w.get("brand") != "Tag Team"]), "every custom wrestler"
    if title == "Super Heavyweight Championship":
        return len([n for n in GIANTS if n in names]), "the Super Heavyweight list"
    if title == "Cruiserweight Championship":
        return len([n for n in FLYERS if n in names]), "the Cruiserweight list"
    if title in OPEN:
        return len([w for w in allr if w.get("brand") != "Tag Team"]), "open to the whole roster"
    b = BRAND.get(title)
    if b:
        return len([w for w in allr if w.get("brand") == b]), "the " + b + " brand"
    return len([w for w in allr if w.get("brand") != "Tag Team"]), "open to the whole roster"

rows = []
for c in sd.get("championships") or []:
    t = c.get("name")
    n, how = pool_for(t)
    rows.append({"title": t, "pool": n, "how": how})

io.open(OUT, "w", encoding="utf-8").write(json.dumps({"titles": rows}, ensure_ascii=False, indent=2))
print("Wrote %d championship pools to %s" % (len(rows), OUT))
for r in rows:
    print("   %-42s %4d   (%s)" % (r["title"], r["pool"], r["how"]))
