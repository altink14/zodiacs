# Zodiacs 生肖

An interactive wheel of the twelve Chinese zodiac animals. Click any animal to open a page covering its earthly branch, hours, month, direction, element, years (with heavenly-stem element and New Year start dates), its place in the Great Race legend, traditional character, and compatibility.

**Live demo:** enable GitHub Pages on this repo (Settings → Pages → Deploy from branch → `main` / root) and open the URL it gives you.

## Run locally

Plain HTML/CSS/JS — no build tools or dependencies. Open `index.html`, or serve the folder:

```bash
python3 -m http.server 8000
```

## Editing the content

All facts live in one file: `data/zodiac.json`. After editing it, regenerate the pages:

```bash
python3 build.py
```

This rewrites `index.html`, `signs/*.html` and `assets/zodiac-data.js`.

## Accuracy notes

- **Hours, months, directions, fixed element and yin/yang** follow the twelve earthly branches (地支), which is the classical basis for the zodiac. Months are given by solar terms (the traditional method) and are approximate to ±1 day depending on the year.
- **Years** begin at Chinese New Year, not January 1. Start dates for 1996–2031 are included; the year's element comes from the heavenly stem (year mod 10).
- **Compatibility** uses the classical 三合 (trines), 六合 (six harmonies) and 六冲 (six clashes) groupings.
- **Personality traits and the Great Race** are folklore. They are presented as traditional attributions, not facts. Things that vary widely between sources (lucky numbers, colours, flowers, yearly "horoscopes") were deliberately left out.

## Structure

```
index.html            the wheel
signs/<animal>.html   one page per sign (generated)
assets/style.css      shared styles
assets/wheel.js       wheel behaviour
assets/zodiac-data.js data for the wheel (generated)
data/zodiac.json      single source of truth
build.py              generator
```

## Credits

Type: Noto Serif SC and Manrope via Google Fonts. Design inspired by circular 十二地支 clock wheels.

## License

MIT
