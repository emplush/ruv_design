# R+V Design

Quelle: [ruv-markenportal.de](https://www.ruv-markenportal.de) (Farben, Typografie, Logo, Designsystem) und ruv.de (CSS-Variablen, Radius, Komponenten).

| Pfad | Inhalt |
|---|---|
| `tokens/tokens.json` | Einzige Wahrheit: Farben, Schriften, Radius, Raster |
| `web/` | `tokens.css` (generiert), `base.css`, `index.html` (Demo) |
| `templates/ruv.pptx` | 16:9, Theme-Farben/-Schrift, 6 Layouts (Titel, Kapitel dunkel; Inhalt, 2 Inhalte, Nur Titel, Leer) |
| `templates/ruv.docx` | A4, Formatvorlagen Titel/Überschriften/Liste/Zitat, Tabelle, Kopf-/Fußzeile |
| `scripts/` | `build_tokens.py`, `build_pptx.py`, `build_docx.py` (Abhängigkeiten: `python-pptx`, `python-docx`) |

Neu bauen: `python3 scripts/build_tokens.py && python3 scripts/build_pptx.py && python3 scripts/build_docx.py`

## Regeln, die umgesetzt sind
- Headlines: Weiß + Orange Hell auf Dunkelblau, Dunkelblau + Orange Dunkel auf hellem Grund. Interaktiv: Mint Hell auf dunkel, Mint Dunkel auf hell.
- Raster X = 1/14 der kürzeren Formatseite; Logo 4X (ohne) / 6X (mit Schutzzone) in der Ecke (PPTX-Layouts nutzen X).
- Office: Arial als Ersatzschrift (Vorgabe Markenportal); Web: RuV Sans/Slab mit Arial/Georgia-Fallback.

## Offen
- **RuV Sans** liegt in `web/fonts/` (Light, Regular, Bold, Black, jeweils mit Italic) und ist per `@font-face` eingebunden. **RuV Slab, Iconfont und Logo** fehlen noch; die Vorlagen enthalten ein Text-Logo „R+V" als Platzhalter.
- Farben sind gegen `Farben.pdf` (Markenportal) abgeglichen, inkl. CMYK/Pantone. Funktionsfarben bestätigt: Rot 1 `FF4C4C` für helle, Rot 2 `FF8484` für dunkle Hintergründe; Grün `759A03` hell / `8EBC27` dunkel. Rot nur für Fehler in Formularen/Tabellen verwenden; `FF4C4C` als Text auf Weiß erreicht keinen WCAG-AA-Kontrast.
- Adobe-Farbbibliotheken (`RuV_Farben_RGB_2025.ase`, `_CMYK_2025.ase`) liegen im Portal und fehlen im Repo.
