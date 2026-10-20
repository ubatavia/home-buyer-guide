#!/usr/bin/env python3
"""Build a single-file HTML comparison report from research files.

Reads the YAML-style frontmatter of every builder/community file in a folder
and the affordability calculator, and writes a self-contained HTML page.

    python3 scripts/build_report.py examples/calgary demo/report.html
"""
import glob
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from affordability import analyse, load_rules  # noqa: E402


def parse_frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return None
    block = text.split("---", 2)[1]
    data, in_sources = {}, False
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.startswith("sources:"):
            in_sources, data["sources"] = True, []
            continue
        if in_sources and line.lstrip().startswith("- "):
            data["sources"].append(line.strip()[2:])
            continue
        if ":" in line and not line.startswith(" "):
            in_sources = False
            k, v = line.split(":", 1)
            v = v.split("#")[0].strip() if not v.strip().startswith('"') else v.strip()
            try:
                data[k.strip()] = json.loads(v)
            except ValueError:
                data[k.strip()] = v
    return data


def money(v):
    return "unknown" if v is None else f"${v:,.0f}"


def rng(v):
    return "unknown" if not v or None in v else f"${v[0]:,.0f} to ${v[1]:,.0f}"


CSS = """
:root{--bg:#fafaf7;--fg:#1c1c1a;--mut:#6b6b66;--card:#fff;--line:#e4e4de;--acc:#1f5c4a;--warn:#9a5b00}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#ecece6;--mut:#a0a09a;--card:#1e1e1b;--line:#33332f;--acc:#6fcfae;--warn:#f0b35c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 system-ui,sans-serif;padding:2rem 1rem}
main{max-width:960px;margin:auto}h1{font-size:1.7rem;margin:0 0 .3rem}h2{font-size:1.1rem;margin:2rem 0 .6rem}
.sub{color:var(--mut);margin:0 0 1.5rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem}
.card h3{margin:0 0 .4rem;font-size:1rem}.k{color:var(--mut);font-size:.8rem}.v{font-weight:600}
.badge{display:inline-block;font-size:.75rem;padding:.1rem .5rem;border-radius:99px;border:1px solid var(--line);color:var(--warn)}
.badge.high{color:var(--acc)}table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line)}
td,th{padding:.5rem .7rem;border-bottom:1px solid var(--line);text-align:left}th{font-size:.8rem;color:var(--mut)}
.wrap{overflow-x:auto}.note{color:var(--mut);font-size:.85rem}a{color:var(--acc)}
"""


def build(folder, out):
    files = [parse_frontmatter(p) for p in sorted(glob.glob(os.path.join(folder, "*.md")))]
    files = [f for f in files if f and f.get("type")]
    comms = [f for f in files if f["type"] == "community"]
    blds = [f for f in files if f["type"] == "builder"]

    def card(f):
        conf = f.get("data_confidence", "low")
        rows = [("Starting price", money(f.get("price_starting"))), ("Price range", rng(f.get("price_range")))]
        if f["type"] == "builder":
            rows += [("Floorplans matched", ", ".join(f.get("matching_floorplans") or []) or "none recorded"),
                     ("Build quality", f.get("build_quality_reputation", "unknown"))]
        else:
            rows += [("Builders", ", ".join(f.get("builders_present") or []) or "unknown"),
                     ("Commute", f"{f['commute_minutes']} min (builder claim)" if f.get("commute_minutes") else "unknown"),
                     ("Residents' Association fee", f"${f['community_fee_annual']:,.2f}/yr" if f.get("community_fee_annual") else "unknown")]
        body = "".join(f'<div class="k">{html.escape(k)}</div><div class="v">{html.escape(str(v))}</div>' for k, v in rows)
        n = len(f.get("sources", []))
        return (f'<div class="card"><h3>{html.escape(f["name"])}</h3>'
                f'<span class="badge {conf}">data confidence: {conf}</span>{body}'
                f'<div class="note">{n} sources &middot; updated {html.escape(str(f.get("last_updated")))}</div></div>')

    fp_path = os.path.join(folder, "floorplans.json")
    fp_html = ""
    if os.path.exists(fp_path):
        fp = json.load(open(fp_path))
        rows_fp = ""
        for p in fp["plans"]:
            lo, hi = p["sqft"]
            size = f"{lo:,}" if lo == hi else f"{lo:,} to {hi:,}"
            rows_fp += (f"<tr><td>{html.escape(p['builder'])}</td><td><b>{html.escape(p['name'])}</b></td><td>{size} sq ft</td>"
                        f"<td>{html.escape(p['beds'])} bed / {html.escape(p['baths'])} bath</td><td>{html.escape(p['garage'])}</td>"
                        f"<td class='note'>{html.escape(p['price_note'])}</td></tr>")
        fp_html = ("<h2>Floor plans by size</h2><div class='wrap'><table><tr><th>Builder</th><th>Plan</th><th>Size</th><th>Rooms</th>"
                   "<th>Garage</th><th>Price signal</th></tr>" + rows_fp + "</table></div>"
                   "<p class='note'>Prices are not like for like: different communities, GST treatment and dates. See floorplan-comparison.md.</p>")
    rules = load_rules()
    s = rules["stress_test"]
    rate = 4.0
    stress = max(rate + s["buffer_pct"], s["floor_pct"])
    rows = ""
    for label, price in [("Paired, low $500Ks (assumed 520,000)", 520000),
                         ("Laned, from $660Ks (assumed 665,000)", 665000),
                         ("Front-drive, low $700Ks (assumed 725,000)", 725000)]:
        r = analyse(price, max(price * 0.10, 0), rate, 25, stress, 12500, insured=True, first_time=True, rules=rules)
        rows += (f"<tr><td>{html.escape(label)}</td><td>{money(r['mortgage'])}</td>"
                 f"<td>{money(r['monthly_payment'])}</td><td>{money(r['stress_payment'])}</td>"
                 f"<td>{r['stress_to_income_pct']:.1f}%</td></tr>")

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Home Buyer Guide: Glacier Ridge example</title>
<style>{CSS}</style></head><body><main>
<h1>Glacier Ridge, Calgary</h1>
<p class="sub">Generated from research files by the Home Buyer Guide agents. Public data, retrieved 2026-10-19.</p>
<h2>Community</h2><div class="grid">{''.join(card(f) for f in comms)}</div>
<h2>Builders</h2><div class="grid">{''.join(card(f) for f in blds)}</div>
{fp_html}
<h2>Affordability (illustrative household)</h2>
<div class="wrap"><table><tr><th>Option</th><th>Mortgage incl. insurance</th><th>Monthly at 4.0%</th>
<th>At qualifying rate {stress:.2f}%</th><th>Stressed payment / income</th></tr>{rows}</table></div>
<p class="note">Assumes 10% down, 25-year amortization, 4.0% contract rate, $150,000 household income. All assumed, none real.
Excludes property tax, utilities, legal fees and GST rebates. Rules snapshot: {rules['last_checked']}, secondary sources, re-verify.</p>
<h2>What this report does not know</h2>
<p class="note">Upgrade pricing, deposit schedules, transit, Catholic school plans and superintendent-level quality
are unknown, so the scorer leaves them blank instead of guessing. Review evidence is a small sample. Not financial advice.</p>
</main></body></html>"""
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
