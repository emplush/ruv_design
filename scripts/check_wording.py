#!/usr/bin/env python3
"""Mechanische Vorpruefung nach dem R+V Corporate Wording (wording/README.md).
Aufruf: python3 scripts/check_wording.py datei [datei ...]   (.html, .md, .txt; '-' liest stdin)
FEHLER (Exit 1): Gender-Sonderzeichen, kleingeschriebenes Du, verbotene Woerter.
HINWEIS: Satzlaenge > 20 Woerter, Ausrufezeichen, moegliches Passiv, moegliches generisches Maskulinum.
Ersetzt kein Korrekturlesen und prueft keine Tonalitaet."""
import re, sys, html

FEHLER = [
 (r"\w[*_:]in(nen)?\b|\w[*_:]innen\b", "Gender-Stern/Unterstrich/Doppelpunkt im Wort (Gendern-Leitfaden)"),
 (r"\b[A-Za-zÄÖÜäöü]+/-?(in|innen)\b", "Sparschreibung mit Schraegstrich (Gendern-Leitfaden)"),
 (r"[a-zäöü]I(nnen)?\b(?<!Kunden)", "Binnen-I (Gendern-Leitfaden)"),
 (r"\b(du|dir|dich|dein|deine|deinen|deinem|deiner|euch|euer|eure)\b", "Anredepronomen kleingeschrieben (Ansprache: immer gross)"),
 (r"(?i:\bleider\b)", "Floskel \"leider\" (Schreibstil: Empathie ohne Floskel)"),
 (r"(?i:\b(gemäß|gegenstandslos|gewähren|diesbezüglich|nachfolgend|in Anbetracht|verbleiben|zu Diensten|zukommen lassen)\b)", "verstaubtes Amtsdeutsch (Schreibstil)"),
 (r"(?i:\bzur Verfügung stehen\b)", "verstaubtes Amtsdeutsch (Schreibstil)"),
 (r"(?i:\b(abändern|vorankündigen|Rückantwort|anmieten|einsparen|aufzeigen|übersenden)\b)", "ueberfluessige Vorsilbe/Wortteil (Schreibstil: kuerzere Form)"),
 (r"(?i:\b(Deadline|Cash|checken)\b)", "unueblicher englischer Begriff (Frist, Bargeld, pruefen)"),
 (r"\b(unsere Firma|unser Haus|unser Unternehmen|Wir von der R\+V)\b", "gestrichene Eigenbezeichnung (Schreibstil)"),
]
GM = re.compile(r"\b(Kunden|Mitarbeiter|Nutzer|Teilnehmer|Antragsteller|Besucher|Leser|Kollegen)\b")

def text_of(raw, name):
    if name.endswith((".html", ".htm")):
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        raw = re.sub(r"(?s)<!--.*?-->", " ", raw)
        raw = re.sub(r"<[^>]+>", "\n", raw)
        raw = html.unescape(raw)
    return raw

def check(name, raw):
    n_err = 0
    lines = text_of(raw, name).splitlines()
    for i, line in enumerate(lines, 1):
        t = line.strip()
        if not t or t.startswith(("```", "|---")):
            continue
        for rx, msg in FEHLER:
            for m in re.finditer(rx, t):
                print(f"{name}:{i}: FEHLER  {msg}: \"{m.group(0)}\""); n_err += 1
        if "!" in t:
            print(f"{name}:{i}: HINWEIS Ausrufezeichen gehoeren zur Umgangssprache, meist weglassen")
        for sent in re.split(r"(?<=[.?!:])\s+", t):
            if len(re.findall(r"\w+", sent)) > 20:
                print(f"{name}:{i}: HINWEIS Satz mit mehr als 20 Woertern: \"{sent[:60]}...\"")
        if re.search(r"\b(wird|werden|wurde|wurden)\b.*\bge\w+(t|en)\b", t):
            print(f"{name}:{i}: HINWEIS moegliches Passiv, aktiv formulieren")
        if GM.search(t) and not re.search(r"innen|Mitarbeitende|Teilnehmende", t):
            print(f"{name}:{i}: HINWEIS moegliches generisches Maskulinum, Doppelnennung/Partizip pruefen")
    return n_err

def main(argv):
    if not argv:
        print(__doc__); return 2
    errs = 0
    for f in argv:
        raw = sys.stdin.read() if f == "-" else open(f, encoding="utf8").read()
        errs += check("stdin" if f == "-" else f, raw)
    print(f"{errs} Fehler")
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
