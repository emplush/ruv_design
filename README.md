# R+V Design

Quelle: [ruv-markenportal.de](https://www.ruv-markenportal.de) (Farben, Typografie, Logo, Designsystem) und ruv.de (CSS-Variablen, Radius, Komponenten).

| Pfad | Inhalt |
|---|---|
| `tokens/tokens.json` | Einzige Wahrheit: Farben, Schriften, Radius, Raster |
| `web/` | `tokens.css` (generiert), `base.css`, `index.html` (Demo) |
| `web/icons.css`, `web/fonts/RuV-Icons-v3.*` | Iconfont v3 (219 Icons, Klassen `ruv-i-*`; TTF zur Desktop-Installation) |
| `assets/logo/` | Logo 2025, RGB (SVG, PNG): ohne Claim, Claim links/rechts/zentriert, horizontal 1:1/1:2/1:3; je positiv/negativ/schwarz |
| `assets/ki-label/` | KI-/AI-Label 2026, positiv/negativ: RGB (SVG, PNG), CMYK (PDF) |
| `wording/README.md`, `scripts/check_wording.py`, `CLAUDE.md` | R+V Corporate Wording (Ton, Du/Sie, Schreibstil, 12 Sprachleitplanken, Gendern, Medien-Anwendung, Checkliste); Prüfskript; Pflichtregeln für alle Texte auf Basis des Designs |
| `fonts/ttf/`, `docs/` | RuV Type TTF (Desktop), Specimen-PDF |
| `templates/ruv.pptx` | 16:9, Theme-Farben/-Schrift, 6 Layouts (Titel, Kapitel dunkel; Inhalt, 2 Inhalte, Nur Titel, Leer) |
| `templates/ruv.docx` | A4, Formatvorlagen Titel/Überschriften/Liste/Zitat, Tabelle, Kopf-/Fußzeile |
| `scripts/` | `build_tokens.py`, `build_pptx.py`, `build_docx.py` (Abhängigkeiten: `python-pptx`, `python-docx`) |

Neu bauen: `python3 scripts/build_tokens.py && python3 scripts/build_pptx.py && python3 scripts/build_docx.py`

## Regeln, die umgesetzt sind
- Texte: nach `wording/README.md` (Sie als Standard, herzlicher Ton, höchstens 20 Wörter pro Satz, kein „leider“, Gendern ohne Sonderzeichen). Vor jeder Abgabe `python3 scripts/check_wording.py <datei>`.
- Headlines: Weiß + Orange Hell auf Dunkelblau, Dunkelblau + Orange Dunkel auf hellem Grund. Interaktiv: Mint Hell auf dunkel, Mint Dunkel auf hell.
- Raster X = 1/14 der kürzeren Formatseite; Logo 4X (ohne) / 6X (mit Schutzzone) in der Ecke (PPTX-Layouts nutzen X).
- Office: Arial als Ersatzschrift (Vorgabe Markenportal); Web: RuV Sans/Slab mit Arial/Georgia-Fallback.

## Offen
- **RuV Type v1.0** (Sans + Slab, je Light/Regular/Bold/Black mit Italic): WOFF2 in `web/fonts/`, TTF zur Desktop-Installation in `fonts/ttf/`, Specimen in `docs/`. Variable Fonts und die im Paket enthaltene `RuVSerif` (im Specimen nicht aufgeführt) sind bewusst nicht im Repo. Office-Vorlagen bleiben bei Arial (Vorgabe Markenportal).
- Farben sind gegen `Farben.pdf` (Markenportal) abgeglichen, inkl. CMYK/Pantone. Funktionsfarben bestätigt: Rot 1 `FF4C4C` für helle, Rot 2 `FF8484` für dunkle Hintergründe; Grün `759A03` hell / `8EBC27` dunkel. Rot nur für Fehler in Formularen/Tabellen verwenden; `FF4C4C` als Text auf Weiß erreicht keinen WCAG-AA-Kontrast.
- Adobe-Farbbibliotheken (`RuV_Farben_RGB_2025.ase`, `_CMYK_2025.ase`) liegen im Portal und fehlen im Repo.

## Claude-Design-Artefakt
Das Design System liegt als Artefakt unter https://claude.ai/artifact/46SH9r4rTB8rSRjfDpnJkN. Es wird aus diesem Repo erzeugt (`python3 scripts/build_design_system.py <ordner>`, Upload-IDs in `design-system/assets.json`). Änderungen an Tokens, Schriften, Logos oder Vorlagen werden im Repo und im Artefakt nachgezogen.
