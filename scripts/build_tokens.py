#!/usr/bin/env python3
"""Erzeugt web/tokens.css aus tokens/tokens.json."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
t = json.loads((root / "tokens/tokens.json").read_text())
L = [":root {"]
for k, v in t["color"].items():
    L.append(f"  --ruv-{k}: {v['value'].lower()};")
L.append(f'  --ruv-font-sans: "RuV Sans", {t["font"]["sans"]["fallback"]};')
L.append(f'  --ruv-font-slab: "RuV Slab", {t["font"]["slab"]["fallback"]};')
L.append(f'  --ruv-radius: {t["radius"]["base"]};')
L.append("}")
(root / "web/tokens.css").write_text("/* GENERIERT aus tokens/tokens.json - nicht von Hand aendern */\n" + "\n".join(L) + "\n")
