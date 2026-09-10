#!/usr/bin/env python3
"""Build the Zodiacs site from zodiac.json.

    python3 build.py

Writes index.html, <sign>.html and zodiac-data.js (flat layout for GitHub Pages).
Standard library only.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "zodiac.json").read_text(encoding="utf-8"))
SIGNS = DATA["signs"]
META = DATA["meta"]
BY_ID = {s["id"]: s for s in SIGNS}
REPO = "https://github.com/altink14/zodiacs"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700'
         '&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500'
         '&family=Noto+Sans+Symbols&display=swap" rel="stylesheet">')

ICON_PREV = '<svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>'
ICON_NEXT = '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>'
ICON_PAUSE = '<svg class="icon-pause" viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
ICON_PLAY = '<svg class="icon-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'

ORDINALS = ["first", "second", "third", "fourth", "fifth", "sixth",
            "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth"]


def mini(sign, cls=""):
    return (f'<span class="mini sym {cls}" style="--c:{sign["color"]};--ci:{sign["ink"]}">'
            f'{sign["glyph"]}</span>')


def chip(sign):
    return f'<a class="chip" href="{sign["id"]}.html">{mini(sign)}{sign["name"]}</a>'


def head(title, desc, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{FONTS}
<link rel="stylesheet" href="style.css">
{extra}
</head>"""


def build_index():
    html = head("Zodiacs — the twelve zodiac signs",
                "An interactive wheel of the twelve zodiac signs. Pick a sign to learn its dates, element, ruling planet, myth, traits and compatibility.") + f"""
<body>
<header class="bar">
  <a class="brand" href="index.html">Zodiacs</a>
  <nav><a href="aries.html">Signs</a><a href="{REPO}">GitHub</a></nav>
</header>

<main class="stage">
  <div class="wheel" aria-label="Wheel of the twelve zodiac signs">
    <div class="ring" id="ring"></div>
    <div class="center">
      <p class="glyph sym" id="glyph" aria-live="polite">♈</p>
      <div class="who" id="who"></div>
      <div class="pill" id="pill"></div>
      <a class="open" id="open" href="aries.html">Read about Aries</a>
    </div>
  </div>
  <div class="controls">
    <button id="prev" aria-label="Previous sign">{ICON_PREV}</button>
    <button id="play" class="play" aria-label="Pause">{ICON_PAUSE}{ICON_PLAY}</button>
    <button id="next" aria-label="Next sign">{ICON_NEXT}</button>
  </div>
</main>
<p class="hint">Click any sign to open its page. The wheel starts on today's sign.</p>

<script src="zodiac-data.js"></script>
<script src="wheel.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def build_sign(sign, i):
    prev_s = SIGNS[(i - 1) % 12]
    next_s = SIGNS[(i + 1) % 12]
    opposite = BY_ID[sign["opposite"]]
    same_element = [s for s in SIGNS if s["element"] == sign["element"] and s["id"] != sign["id"]]
    partner_el = {"Fire": "Air", "Air": "Fire", "Earth": "Water", "Water": "Earth"}[sign["element"]]
    complementary = [s for s in SIGNS if s["element"] == partner_el]
    same_modality = [s for s in SIGNS if s["modality"] == sign["modality"] and s["id"] != sign["id"]]

    strengths = "".join(f"<li>{t}</li>" for t in sign["traits"]["strengths"])
    weaknesses = "".join(f"<li>{t}</li>" for t in sign["traits"]["weaknesses"])
    all_html = "".join(
        f'<a href="{s["id"]}.html" class="{"here" if s["id"] == sign["id"] else ""}" aria-label="{s["name"]}">{mini(s)}</a>'
        for s in SIGNS)

    ruler = sign["ruler"] + (f"<small>Traditional ruler: {sign['tradRuler']}</small>" if sign["tradRuler"] else "")

    html = head(f'{sign["name"]} — Zodiacs',
                f'{sign["name"]}, {sign["symbol"]}: dates, element, ruling planet, myth, traits and compatibility.',
                f'<style>:root{{--accent:{sign["color"]};--accent-ink:{sign["ink"]};}}</style>') + f"""
<body class="sign-page">
<header class="bar">
  <a class="brand" href="index.html">Zodiacs</a>
  <nav>
    <a class="neighbor" href="{prev_s["id"]}.html"><span class="dot" style="--c:{prev_s["color"]}"></span>{prev_s["name"]}</a>
    <a class="neighbor" href="{next_s["id"]}.html">{next_s["name"]}<span class="dot" style="--c:{next_s["color"]}"></span></a>
  </nav>
</header>

<section class="hero">
  <div class="disk" aria-hidden="true"><span class="b sym">{sign["glyph"]}</span><span class="a">{sign["symbol"]}</span></div>
  <div>
    <h1>{sign["name"]}</h1>
    <p class="tagline">{sign["tagline"]}</p>
    <span class="pill">{sign["dates"]}</span>
    <span class="pill">{sign["modality"]} {sign["element"]}</span>
  </div>
</section>

<div class="wrap">

<section class="block">
  <h2>At a glance</h2>
  <p class="lede">{sign["name"]} is the {ORDINALS[i]} sign of the zodiac, symbolised by {sign["symbol"].lower()}. It is a {sign["modality"].lower()} {sign["element"].lower()} sign — {META["elements"][sign["element"]]}, and among the {sign["modality"].lower()} signs, the {META["modalities"][sign["modality"]].split(" — ")[0]}.</p>
  <ul class="facts">
    <li><div class="k">Sun in {sign["name"]}</div><div class="v">{sign["dates"]}<small>Exact changeover shifts by a day some years</small></div></li>
    <li><div class="k">Symbol</div><div class="v">{sign["symbol"]} <span class="sym">{sign["glyph"]}</span></div></li>
    <li><div class="k">Element</div><div class="v">{sign["element"]}<small>{META["elements"][sign["element"]]}</small></div></li>
    <li><div class="k">Modality</div><div class="v">{sign["modality"]}<small>{META["modalities"][sign["modality"]].split(" — ")[1]}</small></div></li>
    <li><div class="k">Ruling planet</div><div class="v">{ruler}</div></li>
    <li><div class="k">Polarity</div><div class="v">{sign["polarity"]}</div></li>
    <li><div class="k">Season</div><div class="v">{sign["season"]}</div></li>
    <li><div class="k">Body part (traditional)</div><div class="v">{sign["bodyPart"]}</div></li>
  </ul>
</section>

<section class="block">
  <h2>In the sky</h2>
  <p class="lede">The sign shares its name with a constellation, but the two are not the same thing. Astrological signs are twelve equal 30° slices of the Sun's yearly path measured from the spring equinox; the constellations are irregular in size and, because of the slow wobble of Earth's axis, the Sun now passes through the constellation {sign["name"]} roughly a month after the dates above.</p>
  <ul class="facts">
    <li><div class="k">Constellation size</div><div class="v">{sign["constellationSize"]}</div></li>
    <li><div class="k">Brightest star</div><div class="v">{sign["brightestStar"]}</div></li>
    <li><div class="k">Zodiac position</div><div class="v">{(i)*30}° – {(i+1)*30}°<small>of the ecliptic</small></div></li>
  </ul>
</section>

<section class="block">
  <h2>The myth</h2>
  <div class="legend">
    <div class="rank sym">{sign["glyph"]}<small>{sign["symbol"]}</small></div>
    <p>{sign["myth"]}</p>
  </div>
</section>

<section class="block">
  <h2>Traditional character</h2>
  <p class="lede">In astrology, people born with the Sun in {sign["name"]} are said to share these qualities. They are traditional attributions, not predictions or facts about any individual.</p>
  <div class="traits">
    <div class="plus"><h3>Said to be</h3><ul>{strengths}</ul></div>
    <div><h3>Watch out for</h3><ul>{weaknesses}</ul></div>
  </div>
</section>

<section class="block">
  <h2>Compatibility</h2>
  <div class="compat">
    <div class="group"><h3>Same element</h3><p>Fellow {sign["element"].lower()} signs — traditionally the easiest, most natural matches.</p><div class="chips">{"".join(chip(s) for s in same_element)}</div></div>
    <div class="group"><h3>Complementary element</h3><p>{sign["element"]} pairs naturally with {partner_el.lower()} — similar polarity, different style.</p><div class="chips">{"".join(chip(s) for s in complementary)}</div></div>
    <div class="group"><h3>Opposite sign</h3><p>Directly across the wheel — the classic "attract and challenge" pairing.</p><div class="chips">{chip(opposite)}</div></div>
    <div class="group"><h3>Same modality</h3><p>Shares the {sign["modality"].lower()} approach; traditionally a source of friction as much as understanding.</p><div class="chips">{"".join(chip(s) for s in same_modality)}</div></div>
  </div>
</section>

<section class="block">
  <h2>All twelve</h2>
  <div class="all">{all_html}</div>
</section>

<nav class="pager">
  <a class="prev" href="{prev_s["id"]}.html">{mini(prev_s)}<span><span class="lbl">Previous</span><br><span class="nm">{prev_s["name"]}</span></span></a>
  <a class="next" href="{next_s["id"]}.html">{mini(next_s)}<span><span class="lbl">Next</span><br><span class="nm">{next_s["name"]}</span></span></a>
</nav>

<footer class="note">Dates are for the tropical zodiac used in Western astrology; the changeover between signs can shift by a day depending on the year and your time zone. Element, modality, polarity and rulers follow standard Western astrology; constellation sizes and brightest stars are from astronomy. Personality and compatibility notes are traditional attributions.</footer>
</div>
</body>
</html>
"""
    (ROOT / f"{sign['id']}.html").write_text(html, encoding="utf-8")


def main():
    (ROOT / "zodiac-data.js").write_text(
        "window.ZODIAC = " + json.dumps(DATA, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    build_index()
    for i, s in enumerate(SIGNS):
        build_sign(s, i)
    print(f"Built index.html and {len(SIGNS)} sign pages.")


if __name__ == "__main__":
    main()
