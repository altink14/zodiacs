# Zodiacs

An interactive wheel of the twelve zodiac signs. Click any sign to open a page covering its dates, symbol, element, modality, ruling planet, polarity, constellation facts, myth, traditional character and compatibility.

**Live site:** https://altink14.github.io/zodiacs/

## Run locally

Plain HTML/CSS/JS — no build tools or dependencies. Open `index.html`, or serve the folder:

```bash
python3 -m http.server 8000
```

## Editing the content

All facts live in one file: `zodiac.json`. After editing it, regenerate the pages:

```bash
python3 build.py
```

This rewrites `index.html`, the twelve `<sign>.html` pages and `zodiac-data.js`.

## Accuracy notes

- **Dates** are the standard tropical (Western) sun-sign ranges. The exact changeover between signs shifts by about a day depending on the year and time zone, so people born on a boundary day should check an ephemeris for their birth year.
- **Element, modality, polarity and rulers** follow standard Western astrology. Where a sign has both a modern and a traditional ruler (Scorpio, Aquarius, Pisces), both are listed.
- **Constellation sizes and brightest stars** are astronomical facts about the constellations that share the signs' names. The pages explain that signs and constellations are not the same thing.
- **Personality traits, compatibility and myths** are traditional attributions and folklore. They are presented as such, not as facts about people. Things that vary widely between sources (lucky numbers, colours, daily horoscopes) were deliberately left out.

## Structure

```
index.html      the wheel
<sign>.html     one page per sign (generated)
style.css       shared styles
wheel.js        wheel behaviour
zodiac-data.js  data for the wheel (generated)
zodiac.json     single source of truth
build.py        generator
```

## Credits

Type: Cormorant Garamond, Manrope and Noto Sans Symbols via Google Fonts.

## License

MIT
