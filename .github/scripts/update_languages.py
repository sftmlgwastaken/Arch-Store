import os
import re

BASE = "lpak/English.lpak"
FILES = [f for f in os.listdir("lpak") if f.endswith(".lpak") and f != "English.lpak"]

def load_file(path):
    data = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                key, val = line.strip().split("|", 1)
                data[key] = val
    return data

english = load_file(BASE)

results = {}
for fname in FILES:
    other = load_file(os.path.join("lpak", fname))
    total = len(english)
    diff = sum(1 for k, v in english.items() if k in other and other[k] != v)
    percent = round((diff / total) * 100, 2) if total else 0
    results[fname.replace(".lpak", "")] = percent

# Costruisce tabella Markdown
table = ["| Language | Coverage |", "|----------|----------|"]
for lang, perc in sorted(results.items()):
    table.append(f"| {lang} | {perc}% |")
table_md = "\n".join(table)

# Testo fisso sotto Languages
intro = (
    "To change the language, start the program, go to settings and select the language from the list, "
    "then press confirm.  \n"
    "The interface will restart with the new language. Be careful to select the language from the list and not write it by hand.  \n"
    "If it is written by hand and there is an error, the configuration file will be restored to prevent errors during startup.\n\n"
)

new_section = f"## Languages\n\n{intro}{table_md}\n"

# Legge README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Sostituisce la sezione ### Trick: Change language
pattern = re.compile(r"### Trick: Change language[\s\S]*?(?=\n## |\Z)", re.MULTILINE)
if pattern.search(readme):
    readme = pattern.sub(new_section, readme)
else:
    # Se non trova, inserisce subito dopo "### Manual" (puoi modificare se vuoi un altro punto preciso)
    manual_pos = readme.find("### Manual")
    if manual_pos != -1:
        insert_pos = readme.find("\n", manual_pos) + 1
        readme = readme[:insert_pos] + "\n" + new_section + readme[insert_pos:]
    else:
        # fallback: alla fine
        readme += "\n\n" + new_section

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("✅ README.md aggiornato con la tabella di copertura delle lingue nella posizione corretta")
