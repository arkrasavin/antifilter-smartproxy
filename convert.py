import re
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE = "https://community.antifilter.download/list/domains.txt"
OUTPUT = Path("public/antifilter.txt")

request = Request(SOURCE, headers={"User-Agent": "SmartProxy-Converter/1.0"})

with urlopen(request, timeout=30) as response:
    source_text = response.read().decode("utf-8-sig")

domains = set()

for line in source_text.splitlines():
    line = line.strip()

    if not line.startswith("*://*.") or not line.endswith("/*"):
        continue

    domain = line[len("*://*."):-len("/*")].lower()

    if re.fullmatch(r"(?:[a-z0-9-]+\.)+[a-z0-9-]+", domain):
        domains.add(domain)

if len(domains) < 100:
    raise RuntimeError("Too few domains. Source may be invalid.")

rules = [
    "[AutoProxy 0.2.9]",
    "! Title: Antifilter SmartProxy",
    "! Converted from Antifilter community edition",
    *[f"||{domain}" for domain in sorted(domains)],
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(rules) + "\n", encoding="utf-8")

print(f"Generated {len(domains)} proxy rules")
