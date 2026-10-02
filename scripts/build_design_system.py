#!/usr/bin/env python3
"""Erzeugt den Projektordner fuer das Claude-Design-Artefakt (Design System) aus tokens/, web/, assets/.
Aufruf: python3 scripts/build_design_system.py <ausgabeordner>. Blob-IDs der Uploads: design-system/assets.json."""
import json, pathlib, shutil, datetime
import sys
R = pathlib.Path(__file__).resolve().parent.parent
D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ruv_ds") / "project"
shutil.rmtree(D.parent, ignore_errors=True); D.mkdir(parents=True)
(D/"fonts").mkdir(); (D/"components"/"Cover").mkdir(parents=True)
for c in ("Button","Card","TextField"): (D/"components"/c).mkdir()
(D/"assets"/"Logos").mkdir(parents=True); (D/"assets"/"KI-Label").mkdir()
w = lambda p, s: (D/p).write_text(s, encoding="utf8")

# ---------- fonts
fonts = []
for fam, pre in (("RuV Sans","RuVSans"),("RuV Slab","RuVSlab")):
    for n, wt in (("Light",300),("Regular",400),("Bold",700),("Black",900)):
        for it in ("", "Italic"):
            f = f"{pre}-{n}{it}.woff2"
            shutil.copy(R/"web/fonts"/f, D/"fonts"/f)
            fonts.append({"family": fam, "file": f"fonts/{f}", "weight": str(wt), "style": "italic" if it else "normal"})
shutil.copy(R/"web/fonts/RuV-Icons-v3.woff2", D/"fonts/RuV-Icons-v3.woff2")
fonts.append({"family": "RuV-Icons-v3", "file": "fonts/RuV-Icons-v3.woff2", "weight": "400", "style": "normal"})

# ---------- tokens
src = json.loads((R/"tokens/tokens.json").read_text())["color"]
raw_names = {  # repo key -> DS name, usage
 "primary": ("primary", "Dunkelblau, Fundament der Marke: Flächen, Text auf hellem Grund (15:1 auf Sand, 17:1 auf Weiß)."),
 "white": ("white", "Weiß: Grund und Text auf Dunkelblau."),
 "orange-light": ("orange-light", "Orange Hell: Highlight in Headlines auf dunklem Grund (7,3:1 auf Dunkelblau)."),
 "orange-dark": ("orange-dark", "Orange Dunkel: Highlight in Headlines auf hellem Grund. 3,3:1 auf Weiß: nur für Text ab 24 px oder fett ab 19 px."),
 "mint-light": ("mint-light", "Mint Hell: Interaktion auf dunklem Grund, Fläche von Call-to-Actions (9,6:1 mit Dunkelblau)."),
 "mint-dark": ("mint-dark", "Mint Dunkel: Interaktion auf hellem Grund, Fläche von Call-to-Actions. Als Text auf Weiß nur 3,3:1, daher Dunkelblau darauf setzen (5:1)."),
 "sand": ("sand", "Sand: warme Fläche, Tabellenzebra, Karten."),
 "brown-1": ("brown-1", "Braun 1: hellste Stufe der Sekundärfarbe, Innenseiten, Infografik."),
 "brown-2": ("brown-2", "Braun 2: Infografik, Hervorhebung auf Sand."),
 "brown-3": ("brown-3", "Braun 3: Infografik, Flächen."),
 "brown-4": ("brown-4", "Braun 4: Infografik; 4,9:1 auf Weiß, damit auch Text."),
 "brown-5": ("brown-5", "Braun 5: dunkelste Stufe, Text auf Braun 1 bis 3."),
 "green": ("green-0", "Grün (hellste Stufe): Fläche."),
 "green-1": ("green-1", "Grün 1: Infografik, Flächen."),
 "green-2": ("green-2", "Grün 2: Infografik, Flächen."),
 "green-3": ("green-3", "Grün 3: Infografik, Flächen."),
 "green-4": ("green-4", "Grün 4: Infografik."),
 "green-5": ("green-5", "Grün 5: dunkelste Stufe, Infografik."),
 "blue-1": ("blue-1", "Blau 1: nur Illustrationen und Infografiken."),
 "blue-2": ("blue-2", "Blau 2: nur Illustrationen und Infografiken."),
 "blue-3": ("blue-3", "Blau 3: nur Illustrationen und Infografiken."),
 "blue-4": ("blue-4", "Blau 4: nur Illustrationen und Infografiken."),
 "grey-1": ("grey-1", "Grau 1: UI-Struktur, hellster Hintergrund."),
 "grey-2": ("grey-2", "Grau 2: UI-Struktur, Trennflächen."),
 "grey-3": ("grey-3", "Grau 3: UI-Struktur, Rahmen und Linien (nur dekorativ, 1,7:1 auf Weiß)."),
 "grey-4": ("grey-4", "Grau 4: UI-Struktur, deaktivierte Zustände (3,5:1 auf Weiß)."),
 "grey-5": ("grey-5", "Grau 5: dunkelstes UI-Grau, Sekundärtext auf Weiß (4,95:1)."),
 "error": ("red-1", "Rot 1: Funktionsfarbe für Fehler auf hellem Grund, nur in Formularen und Tabellen. 3,3:1 auf Weiß: als Rahmen oder Icon, Text nicht darin setzen."),
 "error-soft": ("red-2", "Rot 2: Funktionsfarbe für Fehler auf dunklem Grund, nur in Formularen und Tabellen (7:1 auf Dunkelblau)."),
 "success": ("green-ok", "Grün für Bestätigungen auf hellem Grund, nur in Tabellen und Formularen. 3,3:1 auf Weiß: mit Wort oder Icon kennzeichnen."),
 "success-soft": ("green-ok-light", "Grün für Bestätigungen auf dunklem Grund (7,3:1 auf Dunkelblau)."),
}
tokens_c = []
for k, (n, u) in raw_names.items():
    tokens_c.append({"name": n, "value": src[k]["value"].lower(), "usage": u})
sem = [
 ("surface", "{white}", "{primary}", "Seitengrund. Hell: Weiß; dunkel: Dunkelblau, auf dem Headlines weiß mit Orange stehen."),
 ("surface-soft", "{sand}", "{primary}", "Abgesetzte Fläche (Karten, Tabellenzebra). Dunkel gibt es keine zweite Fläche; Dunkelblau bleibt."),
 ("ink", "{primary}", "{white}", "Text und Linien auf `surface` und `surface-soft` (17:1 / 15:1; dunkel 17:1)."),
 ("ink-muted", "{grey-5}", "#bdc4d4", "Sekundärtext, Fußnoten und Rahmen von Eingabefeldern auf `surface` (hell 4,95:1; dunkel 9:1)."),
 ("highlight", "{orange-dark}", "{orange-light}", "Highlight in Headlines und Topline, nur Text ab 24 px oder fett ab 19 px (hell 3,3:1, dunkel 7,3:1); Fokusring."),
 ("interactive", "{mint-dark}", "{mint-light}", "Fläche interaktiver Elemente (Button, aktiver Zustand). Text darauf: `on-interactive`."),
 ("interactive-hover", "{mint-light}", "#2ee6e6", "Hover-Fläche des Buttons; heller als `interactive`, Text bleibt `on-interactive` (9,6:1 und mehr)."),
 ("on-interactive", "{primary}", "{primary}", "Text auf `interactive` und `interactive-hover` (hell 5:1, dunkel 9,6:1)."),
 ("link", "#167b8a", "#5befef", "Textlinks im Fließtext, unterstrichen (hell 5:1 auf Weiß, dunkel 11:1 auf Dunkelblau)."),
 ("border", "{grey-3}", "#a2abc2", "Rahmen von Karten und Trennlinien, dekorativ (Informationen nie nur darüber tragen)."),
 ("error", "{red-1}", "{red-2}", "Rahmen und Icon bei Fehlern in Formularen. Meldungstext bleibt `ink` (Rot 1 hat nur 3,3:1 auf Weiß)."),
 ("success", "{green-ok}", "{green-ok-light}", "Bestätigung in Tabellen und Formularen, immer mit Wort oder Icon."),
]
for n, h, d, u in sem:
    tokens_c.append({"name": n, "value": {"hell": h, "dunkel": d}, "usage": u})
# Quellen der Werte, die nicht aus dem Portal-PDF stammen: link, ink-muted dunkel, border dunkel, interactive-hover dunkel (ruv.de style.css)
tokens = {
 "name": "R+V Design", "version": 1,
 "color": {"themes": [{"id": "hell", "name": "Hell"}, {"id": "dunkel", "name": "Dunkel"}], "tokens": tokens_c},
 "type": {
  "fonts": fonts,
  "families": {"sans": "\"RuV Sans\", Arial, Helvetica, sans-serif", "slab": "\"RuV Slab\", Georgia, serif", "icons": "\"RuV-Icons-v3\""},
  "groups": [
   {"name": "Sans", "family": "sans", "styles": [
     {"name": "headline-xl", "fontSize": "52px", "lineHeight": 1.15, "fontWeight": 700, "usage": "Hero-Headline; Highlight-Wörter in `highlight`."},
     {"name": "headline", "fontSize": "36px", "lineHeight": 1.15, "fontWeight": 700, "usage": "Abschnittsüberschrift."},
     {"name": "headline-s", "fontSize": "20px", "lineHeight": 1.2, "fontWeight": 700, "usage": "Kartentitel, Unterüberschrift."},
     {"name": "copy", "fontSize": "16px", "lineHeight": "24px", "fontWeight": 400, "usage": "Fließtext."},
     {"name": "copy-s", "fontSize": "14px", "lineHeight": "21px", "fontWeight": 400, "usage": "Kleintext, Fußnoten."},
     {"name": "emphasis", "fontSize": "16px", "lineHeight": "24px", "fontWeight": 900, "usage": "Hervorhebung im Fließtext (Black)."},
     {"name": "cta", "fontSize": "16px", "lineHeight": 1, "fontWeight": 700, "usage": "Beschriftung von Buttons und Call-to-Actions (Bold oder Black)."}]},
   {"name": "Slab", "family": "slab", "styles": [
     {"name": "topline", "fontSize": "18px", "lineHeight": 1.3, "fontWeight": 700, "usage": "Topline über der Headline (RuV Slab Bold)."}]}]},
 "spacing": {"tokens": [
   {"name": "space-1", "value": "4px", "usage": "Abstand Icon zu Text."},
   {"name": "space-2", "value": "8px", "usage": "Abstand Label zu Eingabefeld."},
   {"name": "space-3", "value": "16px", "usage": "Seitenrand mobil, Lücke zwischen Buttons."},
   {"name": "space-4", "value": "24px", "usage": "Innenabstand von Karten, Raster-Lücke."},
   {"name": "space-5", "value": "32px", "usage": "Abstand zwischen Textblöcken."},
   {"name": "space-6", "value": "48px", "usage": "Abschnitts-Innenabstand oben und unten."}]},
 "radius": {"tokens": [
   {"name": "radius-base", "value": "4px", "usage": "Buttons, Karten, Eingabefelder."},
   {"name": "radius-round", "value": "50%", "usage": "Runde Elemente (Störer, Avatare)."}]},
}
w("tokens.json", json.dumps(tokens, indent=1, ensure_ascii=False))

# ---------- README + Abschnitte
w("README.md", """Du bist nicht allein. Das ist die Haltung hinter jedem R+V-Auftritt: solide, nah, genossenschaftlich. Setze sie in Dunkelblau, Weiß, Orange und Mint um und lasse viel Fläche.

## Content Fundamentals

Alle Texte folgen dem R+V Corporate Wording (Abschnitt „Corporate Wording“). Das Wichtigste für jeden Text, der auf diesem Design entsteht:

- **Ton:** herzlich, wie mit guten Bekannten: freundlich, aufmerksam, unterstützend, auf Augenhöhe. Warm statt kalt, nie amtlich.
- **Ansprache:** Sie auf ruv.de, in Kundenbereichen, Anschreiben, Rechnungen und Verträgen; Du in Social Media, Karriere, bei bestimmten Kampagnen und intern. Anredepronomen immer großschreiben (Du, Dein, Sie, Ihnen).
- **Stil:** persönlich mit „wir“ oder „ich“, aktiv, positiv, Verben statt Nomen, höchstens 20 Wörter pro Satz, kein Amtsdeutsch, kein „leider“, keine Fußnoten. Fehler offen zugeben, Ablehnungen begründen.
- **Gendern:** direkt ansprechen, Doppelnennung („Kundinnen und Kunden“) oder Partizip („Mitarbeitende“). Nie Genderstern, Doppelpunkt, Unterstrich oder Schrägstrich. Menü und Überschrift pragmatisch („Privatkunden“).
- **UI-Texte:** Buttons nennen die Handlung („Jetzt berechnen“, „Jetzt informieren“); Fehlermeldungen sagen, was passiert ist und wie es weitergeht. Keine Ausrufezeichen, keine Emojis.
- Der Claim „Du bist nicht allein.“ gehört zum Logo und wird nie umformuliert, gesperrt oder in Versalien gesetzt.
- Headlines sind knapp und plakativ; die Topline darüber ordnet das Thema ein.

## Visual Foundations

- **Grund:** Dunkelblau (`primary`) ist das Fundament. Bilder reichen bei dunklen Layouts bis an mindestens einen Formatrand.
- **Headlines:** Auf Dunkelblau Weiß mit Wörtern in `orange-light`; auf Weiß oder Sand Dunkelblau mit `orange-dark`. In der Praxis über die Tokens `ink` und `highlight` setzen, sie schalten mit dem Theme um.
- **Interaktion:** Mint ist ausschließlich für Interaktion und Call-to-Actions. Button-Fläche `interactive`, Beschriftung `on-interactive` (Dunkelblau). Weiße Schrift auf `mint-dark` hat nur 3,3:1, nicht verwenden.
- **Sekundärfarben:** Braun und Grün (`brown-1` bis `brown-5`, `green-0` bis `green-5`) nur auf tieferer Markenebene: Innenseiten von Broschüren, Infografiken. Blau (`blue-1` bis `blue-4`) nur in Illustrationen und Infografiken.
- **Graustufen:** `grey-1` bis `grey-5` strukturieren Oberflächen. Informationen nie allein über `border` (`grey-3`, 1,7:1) tragen.
- **Funktionsfarben:** Rot und Grün nur für Fehler und Verfügbarkeit in Formularen und Tabellen, immer mit Wort oder Icon. Rot ist nirgends sonst erlaubt. Fehlertext in `ink` setzen, Rahmen und Icon in `error`.
- **Raster:** X ist 1/14 der kürzeren Formatseite (28×28 zur Feinteilung). Logo 6X mit Schutzzone, 4X ohne. Headlines 2X bis 4X, Fließtext ¾X bis 1X, Kleintext ½X. Extreme Formate: 1:2 bis 1:3,3 und breiter nutzen 10×14, 8×14, 6×14 Raster.
- **Radien:** `radius-base` (4 px) für Buttons, Karten, Felder; `radius-round` für runde Störer. Keine Schatten, keine Verläufe.
- **Fokus:** Fokusring 3 px in `highlight`, 2 px Abstand.
- **Themes:** `hell` ist der Standard. Wrappe dunkle Bereiche in `data-theme="dunkel"`; Tokens wie `ink`, `surface`, `highlight`, `interactive` schalten selbst um.

## Typography

- Topline: `topline` (RuV Slab Bold). Headline: `headline-xl`, `headline`, `headline-s` (RuV Sans Bold). Fließtext: `copy`, `copy-s` (Regular). Hervorhebung: `emphasis` (Black). Call-to-Action: `cta` (Bold oder Black).
- Fallback im Web: Arial. In Office (E-Mail, PowerPoint, Dokumente) ist Arial Regular, Italic, Bold, Bold Italic die Vorgabe.
- Fließtext höchstens etwa 65 Zeichen breit.

## Logo

- Schutzzone 1X rundum. Varianten: ohne Claim (Eckenlogo in Präsentationen, bei wenig Platz), Claim links, rechts oder zentriert (zentriert für Social Media und Motion), horizontal 1:1, 1:2, 1:3 (Video-Abbinder, Messe).
- Farben: Blau auf hellem Grund (`positiv`), Weiß auf dunklem Grund (`negativ`), Schwarz nur bei technischer Einschränkung wie Schwarzweißdruck.
- Logo und Claim nie trennen und weder Abstand, Farbe noch Schreibweise ändern. Das Logo nie neu zeichnen, immer die Dateien aus `assets/Logos` einsetzen.

## Iconography

- Icons stammen aus dem Iconfont `RuV-Icons-v3` (219 Piktogramme). Nutze Klassen mit Präfix `ruv-i-` auf einem `<i>` (z. B. `ruv-i-danger`, `ruv-i-infoCircleFilled`), `aria-hidden="true"` und daneben immer Text.
- Icons erben die Textfarbe. Keine Emojis, keine fremden Icon-Sätze.
- Das KI-/AI-Label (`assets/KI-Label`) kennzeichnet KI-generierte Inhalte; deutsch für DE, `AI` für englische Inhalte.

## Components

- `Button`: primär (Mint) für die eine Hauptaktion pro Bereich, `ghost` für Nebenaktionen.
- `Card`: Inhaltskarte, wahlweise auf `surface-soft`.
- `TextField`: Eingabefeld mit Label und Fehlermeldung.

Binde die Bibliothek ein, indem du `tokens.css`, `bundle.css`, React 18 und `bundle.js` lädst; Komponenten liegen dann unter `window.RuV`.
""")
w("Corporate-Wording.md", (R/"wording/README.md").read_text(encoding="utf8"))
w("Praesentationen.md", (R/"docs/praesentationen.md").read_text(encoding="utf8"))
w("Vorlagen.md", """# Vorlagen

PowerPoint- und Word-Vorlagen liegen im Repository `emplush/ruv_design` unter `templates/` und werden aus den gleichen Tokens gebaut.

- `ruv.pptx`: 16:9, Themefarben und -schrift (Arial), sechs Layouts: Startseite, Kapitel, Titel und Inhalt, Zwei Inhalte, Nur Titel, Leer. Details und Regeln im Abschnitt „Präsentationen“.
- `ruv.docx`: A4, Arial 11 pt in Dunkelblau, Formatvorlagen Titel (orange Linie), Überschrift 1 bis 3, Liste, Zitat; Tabelle mit dunkelblauer Kopfzeile und Sand-Zebra; Logo im Kopf, Seitenzahl in der Fußzeile.
- Neu bauen: `python3 scripts/build_tokens.py && python3 scripts/build_pptx.py && python3 scripts/build_docx.py`.
""")
logo_readme = """Logos von R+V, 2025, als SVG. Kopiere sie, zeichne sie nie nach.

- `ruv-logo_ohne-claim_*`: Logo ohne Claim, Eckenlogo in Präsentationen.
- `ruv-logo_claim-links|rechts|zentriert_*`: Logo mit Claim „Du bist nicht allein.“.
- `ruv-logo_claim-horizontal-1zu1|1zu2|1zu3_*`: horizontale Anordnung für Video-Abbinder und Messe.
- Tinte: `positiv` ist Dunkelblau (`primary`) und gehört auf hellen Grund; `negativ` ist Weiß und gehört auf Dunkelblau oder Bild; `schwarz` nur bei technischer Einschränkung (Schwarzweißdruck).
- Schutzzone 1X rundum; Eckenlogo 4X breit ohne, 6X mit Schutzzone.
"""
w("assets/Logos/README.md", logo_readme)
w("assets/KI-Label/README.md", """KI- und AI-Label 2026, Quadrat mit Funkelsymbol, zur Kennzeichnung KI-generierter Inhalte. `KI_*` für deutsche, `AI_*` für englische Inhalte.

- Tinte: `positiv` Dunkelblau mit weißem Schriftzug auf hellem Grund; `negativ` auf dunklem Grund. Das Label nie umfärben oder neu zeichnen.
""")

# ---------- components
w("components/bundle.css", """.ruv-btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 24px;border:2px solid transparent;border-radius:var(--radius-base);font:700 16px/1 var(--font-sans);text-decoration:none;cursor:pointer;transition:background .15s}
.ruv-btn--primary{background:var(--interactive);color:var(--on-interactive)}
.ruv-btn--primary:hover{background:var(--interactive-hover)}
.ruv-btn--ghost{background:transparent;color:var(--ink);border-color:var(--ink)}
.ruv-btn--ghost:hover{background:var(--ink);color:var(--surface)}
.ruv-btn:focus-visible,.ruv-field input:focus-visible{outline:3px solid var(--highlight);outline-offset:2px}
.ruv-btn[disabled]{background:var(--grey-2);color:var(--grey-5);border-color:transparent;cursor:not-allowed}
.ruv-card{background:var(--surface);color:var(--ink);border:1px solid var(--border);border-radius:var(--radius-base);padding:var(--space-4);font:400 16px/24px var(--font-sans)}
.ruv-card--soft{background:var(--surface-soft)}
.ruv-card__topline{margin:0 0 var(--space-2);font:700 18px/1.3 var(--font-slab);color:var(--highlight)}
.ruv-card__title{margin:0 0 var(--space-2);font:700 20px/1.2 var(--font-sans)}
.ruv-card__body{margin:0}
.ruv-field{display:flex;flex-direction:column;gap:var(--space-2);font-family:var(--font-sans);color:var(--ink)}
.ruv-field label{font:700 16px/1.2 var(--font-sans)}
.ruv-field input{padding:12px;border:1px solid var(--ink-muted);border-radius:var(--radius-base);background:var(--surface);color:var(--ink);font:400 16px/1.2 var(--font-sans)}
.ruv-field--error input{border:2px solid var(--error)}
.ruv-field__msg{font:700 14px/1.4 var(--font-sans);margin:0}
""")
w("components/bundle.js", """/* @ds-bundle: {"format":4,"namespace":"RuV","components":[{"name":"Button"},{"name":"Card"},{"name":"TextField"}]} */
(function () {
  var h = window.React.createElement;
  function Button(p) {
    var variant = p.variant || "primary";
    var cls = "ruv-btn ruv-btn--" + variant;
    var props = { className: cls, disabled: p.disabled, onClick: p.onClick, type: p.type || "button" };
    if (p.href) { return h("a", { className: cls, href: p.href }, p.children); }
    return h("button", props, p.children);
  }
  function Card(p) {
    return h("div", { className: "ruv-card" + (p.soft ? " ruv-card--soft" : "") },
      p.topline ? h("p", { className: "ruv-card__topline" }, p.topline) : null,
      p.title ? h("h3", { className: "ruv-card__title" }, p.title) : null,
      h("div", { className: "ruv-card__body" }, p.children));
  }
  function TextField(p) {
    var id = p.id || "ruv-" + String(p.label).toLowerCase().replace(/[^a-z0-9]+/g, "-");
    return h("div", { className: "ruv-field" + (p.error ? " ruv-field--error" : "") },
      h("label", { htmlFor: id }, p.label),
      h("input", { id: id, type: p.type || "text", defaultValue: p.defaultValue, placeholder: p.placeholder, "aria-invalid": p.error ? "true" : undefined, "aria-describedby": p.error ? id + "-msg" : undefined }),
      p.error ? h("p", { className: "ruv-field__msg", id: id + "-msg" }, "Fehler: " + p.error) : null);
  }
  window.RuV = { Button: Button, Card: Card, TextField: TextField };
})();
""")
w("components/index.d.ts", """export interface ButtonProps { variant?: "primary" | "ghost"; href?: string; disabled?: boolean; type?: "button" | "submit"; onClick?: () => void; children: React.ReactNode }
export interface CardProps { topline?: string; title?: string; soft?: boolean; children?: React.ReactNode }
export interface TextFieldProps { label: string; id?: string; type?: string; defaultValue?: string; placeholder?: string; error?: string }
""")
w("components/Button/README.md", """Button für Aktionen. Der primäre Button (Mint, Beschriftung Dunkelblau) steht einmal pro Bereich für die Hauptaktion; `ghost` für Nebenaktionen.

- Du lieferst `children` (kurze Handlung wie „Jetzt berechnen“) und optional `href` (rendert einen Link) oder `onClick`.
- Auf dunklem Grund `data-theme="dunkel"` am Container setzen; Farben schalten um.
- Nicht: weiße Schrift auf Mint Dunkel, mehr als ein primärer Button nebeneinander, Rot oder Orange als Button-Fläche.
""")
w("components/Card/README.md", """Karte für Produkte oder Ratgeber. Optional `topline` (RuV Slab Bold in `highlight`), `title`, Inhalt als `children`; `soft` setzt `surface-soft`.

- Du lieferst Text und höchstens einen Button oder Link.
- Rahmen und Fläche reichen; keine Schatten, keine Akzentkante.
""")
w("components/TextField/README.md", """Eingabefeld mit Label darüber. `error` zeigt Rahmen in `error` und eine Meldung mit „Fehler:“ in `ink`; Rot allein trägt die Information nie.

- Du lieferst `label` (Pflicht) und optional `defaultValue`, `placeholder`, `type`.
- Rote Fehlerfarbe nur hier und in Tabellen verwenden.
""")
pre = lambda g, h, body: f"""<!-- @dsCard group="{g}" height={h} -->
<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;font-family:var(--font-sans);background:var(--surface);color:var(--ink)}}.row{{display:flex;gap:var(--space-3);flex-wrap:wrap;padding:var(--space-4);background:var(--surface)}}.dark{{background:var(--surface);color:var(--ink)}}</style></head><body><div id="r"></div><script>
var R=window.RuV,h=window.React.createElement;
{body}
ReactDOM.createRoot(document.getElementById("r")).render(h("div",null,h("div",{{className:"row"}},h(Light)),h("div",{{className:"row dark","data-theme":"dunkel"}},h(Light))));
</script></body></html>
"""
w("components/Button/preview.html", pre("Aktionen", 190, 'function Light(){return h(window.React.Fragment,null,h(R.Button,null,"Jetzt berechnen"),h(R.Button,{variant:"ghost"},"Mehr erfahren"),h(R.Button,{disabled:true},"Nicht verfügbar"));}'))
w("components/Card/preview.html", pre("Inhalt", 330, 'function Light(){return h("div",{style:{display:"flex",gap:16,flexWrap:"wrap"}},h("div",{style:{width:240}},h(R.Card,{topline:"Haftpflicht",title:"Privathaftpflicht"},"Schützt Sie, wenn Sie versehentlich einen Schaden verursachen.")),h("div",{style:{width:240}},h(R.Card,{soft:true,title:"Hausrat"},"Für Ihr Hab und Gut zu Hause.")));}'))
w("components/TextField/preview.html", pre("Formulare", 270, 'function Light(){return h("div",{style:{display:"flex",gap:16,flexWrap:"wrap"}},h("div",{style:{width:240}},h(R.TextField,{label:"Name",defaultValue:"Anna Beispiel"})),h("div",{style:{width:240}},h(R.TextField,{label:"E-Mail",error:"Bitte geben Sie eine gültige Adresse an."})));}'))

# ---------- cover
w("components/Cover/preview.html", """<!-- @dsCard height=288 -->
<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0}
body{background:var(--surface);color:var(--ink)}
.cv{position:relative;width:960px;height:288px;overflow:hidden;background:var(--surface)}
.cv svg{position:absolute;left:480px;top:0}
.t{position:absolute;left:32px;bottom:24px;width:440px}
.t h1{margin:0;font:700 112px/.95 var(--font-sans);color:var(--ink)}
.t p{margin:8px 0 0;font:400 14px/20px var(--font-sans);color:var(--ink-muted)}
.o{fill:var(--orange-dark)}.i{fill:var(--ink)}.hl{fill:var(--highlight)}.mi{fill:var(--interactive)}
.ml{fill:var(--mint-light)}.ol{fill:var(--orange-light)}.sd{fill:var(--sand)}.g3{fill:var(--green-3)}
.bk{fill:var(--primary)}.wh{fill:var(--white)}
rect{rx:var(--radius-base)}
</style></head><body>
<div class="cv">
<svg width="480" height="288" viewBox="0 0 480 288" role="img" aria-label="Farbflächen mit Eckmarken">
<!-- Derivation
 blocks: ink 4x5 steps (192x240), highlight 2x3 (96x144), mint-light 3x2, interactive 3x2, sand 2x2, orange-light 2x2, green-3 1x3, mint-light 2x1 at 48px (space-6) steps.
 arrangement: staggered stack, ink slab bleeding off the top edge, blocks meeting at corners like the layout grid cells.
 pattern: R+V's orange corner marks (Eckmarken) in the ads: three L brackets, 8px (space-2) thick, 32px (space-5) arms, one per block corner.
 steps and radii: 48/32/8px from space-6, space-5, space-2; corners radius-base. -->
<rect class="i" x="0" y="0" width="192" height="240"/>
<rect class="hl" x="192" y="48" width="96" height="144"/>
<rect class="ml" x="288" y="0" width="144" height="96"/>
<rect class="mi" x="192" y="192" width="144" height="96"/>
<rect class="sd" x="336" y="96" width="96" height="96"/>
<rect class="ol" x="384" y="192" width="96" height="96"/>
<rect class="g3" x="432" y="0" width="48" height="144"/>
<rect class="ml" x="0" y="240" width="96" height="48"/>
<path class="o" transform="translate(184 232) rotate(180)" d="M0 0h32v8h-24v24h-8z"/>
<path class="bk" d="M344 104h32v8h-24v24h-8z"/>
<path class="wh" transform="translate(328 280) rotate(180)" d="M0 0h32v8h-24v24h-8z"/>
</svg>
<div class="t"><h1>R+V<br>Design</h1><p>Du bist nicht allein.</p></div>
</div>
</body></html>
""")

# ---------- index
base = "project/"
def rec(name, blob, size): return {"name": name, "blob": blob, "size": size, "type": "image/svg+xml"}
AS = json.loads((R/"design-system/assets.json").read_text())
L = {k: tuple(v) for k, v in AS["Logos"].items()}
K = {k: tuple(v) for k, v in AS["KI-Label"].items()}
order_logo = ["ruv-logo_ohne-claim_positiv.svg","ruv-logo_ohne-claim_negativ.svg","ruv-logo_ohne-claim_schwarz.svg"] + [k for k in L if "ohne-claim" not in k]
idx = {"v": 3, "layout": "files", "createdOnFiles": {"v": 1, "at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")},
 "title": "R+V Design", "namespace": "RuV", "libraries": [{"name": "react", "version": "18"}, {"name": "react-dom", "version": "18"}],
 "sections": {}, "groups": ["Logos", "KI-Label"],
 "assetGroups": {
  "Logos": {"name": "Logos", "tile": "l", "order": order_logo, "files": {k: rec(k, *L[k]) for k in order_logo}},
  "KI-Label": {"name": "KI-Label", "tile": "m", "order": list(K), "files": {k: rec(k, *v) for k, v in K.items()}}},
 "blobs": {}, "docs": {"readme": "project/README.md", "sections": []},
 "lastChange": {"by": "Claude", "at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "via": "Claude Code", "note": "Erstanlage aus Markenportal-Quellen"}}
w("design-system.json", json.dumps(idx, indent=1, ensure_ascii=False))
print(sorted(str(p.relative_to(D.parent)) for p in D.rglob("*") if p.is_file()).__len__(), "files")
