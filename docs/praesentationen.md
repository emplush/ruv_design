# Präsentationen

Regeln für PowerPoint-Präsentationen auf Basis des R+V-Designs. Vorlage: `templates/ruv.pptx` (Layouts Startseite, Kapitel, Titel und Inhalt, Zwei Inhalte, Nur Titel, Leer). Neue Präsentation mit Startseite: `python3 scripts/new_deck.py --title … --subtitle … --line … --image … --out …`. Maße stehen in `scripts/build_pptx.py`. Texte folgen dem Corporate Wording.

## Startseite: besonders sorgfältig prüfen

Die Startseite ist geteilt: links eine dunkelblaue Fläche (`primary`, etwa die halbe Breite), rechts ein Bild bis an den Folienrand.

**Logos**
- Oben links in Weiß das R+V-Logo mit Claim „Du bist nicht allein.“ (`ruv-logo_claim-links_negativ`). Sichtbare Breite etwa 16 % der Folienbreite, linke Kante etwa 4,4 % der Folienbreite, Oberkante etwa 8 % der Folienhöhe. Logo nie verzerren, umfärben, beschneiden oder neu zeichnen; die Schutzzone bleibt frei.
- Unten links das GFG-Logo mit Deskriptor (`gfg-logo_deskriptor_links_negativ`): „Die Versicherung in der“ mit dem Logo der Genossenschaftlichen Finanzgruppe Volksbanken Raiffeisenbanken, in Weiß. Es sitzt an der Vorlage-Position (linksbündig mit dem R+V-Logo oben) und in Vorlage-Größe. Nie als Text nachbauen.

**Textfolge links, von oben nach unten**
1. Eine Zeile in **weißer** Schrift mit Ort, Datum und Referentin oder Referent („Wiesbaden, 02.10.2026, Anna Beispiel“). Nicht „Referent/-in“: der Gendern-Leitfaden verbietet Sparschreibungen.
2. **Haupttitel in Orange** (`orange-light`), fett, höchstens zwei Zeilen.
3. **Untertitel in Weiß**, fett.

**Bild rechts**
- Das Bild passt immer zum Thema der Präsentation.
- Wird ein Bild geliefert, wird genau dieses Bild verwendet.
- Wird kein Bild geliefert, wird vorerst **kein Bild erstellt** und auch kein beliebiges Fremdbild eingesetzt. Der Bildplatzhalter der Startseite bleibt leer, und es wird darauf hingewiesen, dass das Bild fehlt.
- Das Bild füllt die rechte Fläche randlos, wird zugeschnitten statt verzerrt und liegt vollständig im Folienrand.

## Inhaltsseiten

- Oben links die **Hauptheadline** in Dunkelblau (`primary`), fett, 28 pt.
- Darunter die **Unterheadline** in Orange (`orange-dark`), fett, 28 pt.
- **Unten links** die Foliennummer, daneben der **Titel der Präsentation** (Dunkelblau, fett, 11 pt) und darunter das **Datum**.
- **Unten rechts** das R+V-Logo (ohne Claim, positiv) in Vorlage-Größe.
- Dazwischen der Inhalt in Dunkelblau, 18 pt. Ein Gedanke pro Folie, kurze Sätze, keine Fußnoten.
- Den Titel der Präsentation in der Fußzeile an den Titel der Startseite angleichen (`--title`). Das Datum aktualisiert sich automatisch.

## Kapitelfolien

Dunkelblau, Logo mit Claim oben links, Kapitelüberschrift in Orange, Untertitel in Weiß.

## Vor der Abgabe prüfen

- Logos vorhanden (R+V mit Claim und GFG-Logo auf der Startseite, R+V unten rechts auf Inhaltsseiten), an der richtigen Stelle, in der richtigen Größe, unverzerrt.
- Startseite: Zeile Ort/Datum weiß, Haupttitel orange, Untertitel weiß, Bild (sofern geliefert) passt zum Thema und füllt die rechte Fläche; fehlt es, ist das benannt.
- Inhaltsseiten: Hauptheadline blau, Unterheadline orange, unten links Foliennummer, Titel der Präsentation und Datum, unten rechts Logo.
- Texte mit `python3 scripts/check_wording.py` und der Checkliste im Corporate Wording geprüft.
