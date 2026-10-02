# R+V Design: Hinweise für Claude

Dieses Repo ist das R+V-Design (Tokens, Web-Basis, PPTX-/DOCX-Vorlage, Design-System-Artefakt). Bei jeder Änderung Repo und Artefakt gemeinsam nachziehen (`scripts/build_design_system.py`, Artefakt https://claude.ai/artifact/46SH9r4rTB8rSRjfDpnJkN) und auf `claude/youthful-davinci-580q9o` pushen.

## PowerPoint-Präsentationen: Startseite und Inhaltsseiten

Vollständig: `docs/praesentationen.md`. Vorlage `templates/ruv.pptx`, neue Decks mit `scripts/new_deck.py`. Besonders auf die Startseite achten:
- Logo mit Claim (weiß) oben links und das GFG-Logo mit Deskriptor „Die Versicherung in der“ (weiß) unten links, an der Vorlage-Stelle und in Vorlage-Größe.
- Links auf Dunkelblau: Zeile in **Weiß** mit Ort, Datum und Referentin oder Referent; **Haupttitel in Orange**; **Untertitel in Weiß**.
- Rechts ein Bild, das **immer zum Thema** der Präsentation passt: geliefertes Bild verwenden. Ohne geliefertes Bild vorerst **kein Bild erstellen**, Platzhalter leer lassen und darauf hinweisen.
- Inhaltsseiten: Hauptheadline **blau**, Unterheadline **orange**, unten links Foliennummer, Titel der Präsentation und Datum, unten rechts das R+V-Logo.

## Texte immer nach dem R+V Corporate Wording

Gilt für jeden Text, den du für Web-Apps, Apps, Präsentationen, Dokumente, Social Media und andere Medien auf Basis dieses Designs schreibst (Beispieltexte, UI-Texte, Folien, Vorlagen eingeschlossen). Vollständig: `wording/README.md`. Vorher lesen, nachher mit `python3 scripts/check_wording.py <datei>` und der Checkliste dort prüfen.

Kernregeln:
- **Ton:** herzlich, wie mit guten Bekannten: freundlich, aufmerksam, unterstützend, auf Augenhöhe. Warm statt kalt, nie amtlich.
- **Ansprache:** Standard ist **Sie** (ruv.de, Anschreiben, Rechnungen, Verträge, Kundenbereiche). **Du** in Social Media, Karriere und Mitarbeitergewinnung, bei bestimmten Kampagnen, intern. Newsletter und Call-to-Actions: Sie oder Du nach Kampagne. Anredepronomen immer großschreiben (Du, Dein, Dir, Sie, Ihnen, Ihr, Euch).
- **Stil:** persönlich mit „wir“/„ich“ (nie „Wir von der R+V“, „unser Unternehmen“); aktiv; positiv; Verben statt Nomen; **höchstens 20 Wörter pro Satz**, höchstens ein Nebensatz; ein Gedanke pro Satz, ein Thema pro Absatz; Klartext statt Amtsdeutsch (kein „gemäß“, „diesbezüglich“, „nachfolgend“, „zur Verfügung stehen“); kein „leider“; Fachbegriffe umschreiben; englische Wörter nur, wenn eingebürgert; kein Kleingedrucktes, keine Fußnoten.
- **Empathie:** Mitgefühl zeigen, Fehler offen zugeben, Ablehnungen begründen und mit Hilfsangebot verbinden, Nutzen und nächste Schritte nennen, sagen, wenn nichts zu tun ist.
- **Keine** Ausrufezeichen, Emojis, Umgangssprache, Dialekt. Jugendsprache nur gezielt im Social Web.
- **Gendern:** nie Genderstern, Doppelpunkt, Unterstrich, Binnen-I oder Schrägstrich. Stattdessen direkt ansprechen, Doppelnennung („Kundinnen und Kunden“), Partizipien („Mitarbeitende“), neutrale Wörter. Feste Formen und Unternehmen nicht gendern (Kundenberatung, Versicherer). Rechtsdokumente (Bedingungen, Scheine, Anträge, Datenschutz) vorläufig nicht gendern, aber direkt ansprechen. Bei knappem Platz (Menü, Überschrift, Banner) pragmatisch bleiben.
- **UI-Texte:** Buttons nennen die Handlung („Jetzt berechnen“); Fehlermeldungen sagen, was passiert ist und wie es weitergeht; Erfolgsmeldungen warm und konkret.

Beispieltexte im Repo dürfen keine Lorem-ipsum- oder Platzhalterfloskeln sein, sondern folgen diesen Regeln.
