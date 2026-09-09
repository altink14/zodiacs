#!/usr/bin/env python3
"""Build the Zodiacs site from data/zodiac.json.

    python3 build.py

Writes index.html, signs/<sign>.html and assets/zodiac-data.js.
No dependencies beyond the Python standard library.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data" / "zodiac.json").read_text(encoding="utf-8"))
SIGNS = DATA["signs"]
META = DATA["meta"]
BY_ID = {s["id"]: s for s in SIGNS}
CURRENT_YEAR = 2026  # the sign whose year this is gets a highlight

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700'
         '&family=Noto+Serif+SC:wght@400;700&display=swap" rel="stylesheet">')

ICON_PREV = '<svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>'
ICON_NEXT = '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>'
ICON_PAUSE = '<svg class="icon-pause" viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
ICON_PLAY = '<svg class="icon-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'


def stem_for(year: int):
    name, char = META["stems"][year % 10]
    return name, char


def years_for(sign):
    start = META["baseYear"] + (sign["order"] - 1)
    return [y for y in range(start, 2032, 12)]


def mini(sign, cls=""):
    return (f'<span class="mini {cls}" style="--c:{sign["color"]};--ci:{sign["ink"]}">'
            f'{sign["branch"]}</span>')


def chip(sign):
    return f'<a class="chip" href="{sign["id"]}.html">{mini(sign)}{sign["name"]}</a>'


def build_index():
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zodiacs — the twelve Chinese zodiac signs</title>
<meta name="description" content="An interactive wheel of the twelve Chinese zodiac animals. Pick a sign to learn its hours, element, years, legend and compatibility.">
{FONTS}
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="bar">
  <a class="brand" href="./">Zodiacs<span class="cn">生肖</span></a>
  <nav><a href="signs/rat.html">Signs</a><a href="https://github.com/">GitHub</a></nav>
</header>

<main class="stage">
  <div class="wheel" aria-label="Wheel of the twelve zodiac signs">
    <div class="ring" id="ring"></div>
    <div class="center">
      <p class="glyph cn" id="glyph" aria-live="polite">子</p>
      <div class="who" id="who"></div>
      <div class="pill" id="pill"></div>
      <a class="open" id="open" href="signs/rat.html">Read about the Rat</a>
    </div>
  </div>
  <div class="controls">
    <button id="prev" aria-label="Previous sign">{ICON_PREV}</button>
    <button id="play" class="play" aria-label="Pause">{ICON_PAUSE}{ICON_PLAY}</button>
    <button id="next" aria-label="Next sign">{ICON_NEXT}</button>
  </div>
</main>
<p class="hint">Click any animal to open its page. The wheel starts on the sign that rules the current hour.</p>

<script src="assets/zodiac-data.js"></script>
<script src="assets/wheel.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def build_sign(sign, i):
    prev_s = SIGNS[(i - 1) % 12]
    next_s = SIGNS[(i + 1) % 12]
    trine = [BY_ID[t] for t in sign["trine"]]
    harmony = BY_ID[sign["harmony"]]
    clash = BY_ID[sign["clash"]]

    years_html = []
    for y in years_for(sign):
        stem, char = stem_for(y)
        starts = META["newYearStarts"].get(str(y))
        sub = f"{stem} {char}{sign['branch']}" + (f" · from {starts}" if starts else "")
        cls = " now" if y == CURRENT_YEAR else ""
        years_html.append(f'<div class="year{cls}"><b>{y}</b><span>{sub}</span></div>')

    strengths = "".join(f"<li>{t}</li>" for t in sign["traits"]["strengths"])
    weaknesses = "".join(f"<li>{t}</li>" for t in sign["traits"]["weaknesses"])

    all_html = "".join(
        f'<a href="{s["id"]}.html" class="{"here" if s["id"] == sign["id"] else ""}" aria-label="{s["name"]}">{mini(s)}</a>'
        for s in SIGNS)

    ordinals = ["first", "second", "third", "fourth", "fifth", "sixth",
                "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth"]

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{sign["name"]} {sign["cn"]} — Zodiacs</title>
<meta name="description" content="The {sign["name"]} in the Chinese zodiac: hours, element, years, the Great Race legend, traditional character and compatibility.">
{FONTS}
<link rel="stylesheet" href="../assets/style.css">
<style>:root{{--accent:{sign["color"]};--accent-ink:{sign["ink"]};}}</style>
</head>
<body class="sign-page">
<header class="bar">
  <a class="brand" href="../">Zodiacs<span class="cn">生肖</span></a>
  <nav>
    <a class="neighbor" href="{prev_s["id"]}.html"><span class="dot" style="--c:{prev_s["color"]}"></span>{prev_s["name"]}</a>
    <a class="neighbor" href="{next_s["id"]}.html">{next_s["name"]}<span class="dot" style="--c:{next_s["color"]}"></span></a>
  </nav>
</header>

<section class="hero">
  <div class="disk" aria-hidden="true"><span class="b cn">{sign["branch"]}</span><span class="a cn">{sign["cn"]}</span></div>
  <div>
    <h1>{sign["name"]}<span class="cn">{sign["cn"]} {sign["pinyin"]}</span></h1>
    <p class="tagline">{sign["tagline"]}</p>
    <span class="pill"><span class="cn">{sign["branch"]}时</span>{sign["hours"]}</span>
    <span class="pill">{sign["polarity"]} {sign["element"]}</span>
  </div>
</section>

<div class="wrap">

<section class="block">
  <h2>At a glance <span class="cn">地支 · {sign["branch"]} {sign["branchPinyin"]}</span></h2>
  <p class="lede">The {sign["name"]} is the {ordinals[i]} of the twelve signs and is paired with the earthly branch {sign["branch"]} ({sign["branchPinyin"]}). The branch fixes its two-hour slot, its month, its compass point and its element.</p>
  <ul class="facts">
    <li><div class="k">Position</div><div class="v">{sign["order"]} of 12</div></li>
    <li><div class="k">Earthly branch</div><div class="v">{sign["branch"]} {sign["branchPinyin"]}</div></li>
    <li><div class="k">Hours</div><div class="v">{sign["hours"]}<small>{sign["branch"]}时 — the {sign["name"]} hour</small></div></li>
    <li><div class="k">Month</div><div class="v">{sign["month"].split(" (")[0]}<small>{sign["month"].split(" (")[1][:-1]}, by solar terms</small></div></li>
    <li><div class="k">Direction</div><div class="v">{sign["direction"]}</div></li>
    <li><div class="k">Fixed element</div><div class="v">{sign["element"]}</div></li>
    <li><div class="k">Polarity</div><div class="v">{sign["polarity"]}</div></li>
    <li><div class="k">Season</div><div class="v">{sign["season"]}</div></li>
  </ul>
</section>

<section class="block">
  <h2>Years of the {sign["name"]} <span class="cn">{sign["cn"]}年</span></h2>
  <p class="lede">A zodiac year starts at Chinese New Year (late January to mid-February), not on January 1 — so people born in early January or February belong to the previous animal. Each year also carries one of the five elements from the ten heavenly stems, which is why the same animal returns as a different element every twelve years and the full cycle is sixty.</p>
  <div class="years">{"".join(years_html)}</div>
</section>

<section class="block">
  <h2>The Great Race <span class="cn">十二生肖的传说</span></h2>
  <div class="legend">
    <div class="rank cn">{sign["order"]}<small>place in the race</small></div>
    <p>{sign["legend"]}</p>
  </div>
</section>

<section class="block">
  <h2>Traditional character <span class="cn">性格</span></h2>
  <p class="lede">In Chinese folk tradition, people born in a {sign["name"]} year are said to share the animal's temperament. These are cultural attributions, not predictions.</p>
  <div class="traits">
    <div class="plus"><h3>Said to be</h3><ul>{strengths}</ul></div>
    <div><h3>Watch out for</h3><ul>{weaknesses}</ul></div>
  </div>
</section>

<section class="block">
  <h2>Compatibility <span class="cn">三合 · 六合 · 六冲</span></h2>
  <div class="compat">
    <div class="group"><h3>Best allies (三合 sān hé)</h3><p>The three signs 120° apart on the wheel form a harmonious trine.</p><div class="chips">{chip(trine[0])}{chip(trine[1])}</div></div>
    <div class="group"><h3>Secret friend (六合 liù hé)</h3><p>A quieter, one-to-one harmony pairing.</p><div class="chips">{chip(harmony)}</div></div>
    <div class="group"><h3>Clash (六冲 liù chōng)</h3><p>The sign directly opposite — traditionally the hardest match.</p><div class="chips">{chip(clash)}</div></div>
  </div>
</section>

<section class="block">
  <h2>All twelve</h2>
  <div class="all">{all_html}</div>
</section>

<nav class="pager">
  <a class="prev" href="{prev_s["id"]}.html">{mini(prev_s)}<span><span class="lbl">Previous</span><br><span class="nm">{prev_s["name"]} {prev_s["cn"]}</span></span></a>
  <a class="next" href="{next_s["id"]}.html">{mini(next_s)}<span><span class="lbl">Next</span><br><span class="nm">{next_s["name"]} {next_s["cn"]}</span></span></a>
</nav>

<footer class="note">Hours, months, directions, elements and polarity follow the twelve earthly branches (地支). New Year dates are from the Chinese lunisolar calendar. Personality and compatibility notes are traditional folk attributions.</footer>
</div>
</body>
</html>
"""
    (ROOT / "signs" / f"{sign['id']}.html").write_text(html, encoding="utf-8")


def main():
    (ROOT / "signs").mkdir(exist_ok=True)
    (ROOT / "assets" / "zodiac-data.js").write_text(
        "window.ZODIAC = " + json.dumps(DATA, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    build_index()
    for i, s in enumerate(SIGNS):
        build_sign(s, i)
    print(f"Built index.html and {len(SIGNS)} sign pages.")


if __name__ == "__main__":
    main()
