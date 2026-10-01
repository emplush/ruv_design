#!/usr/bin/env python3
"""Erzeugt templates/ruv.pptx (16:9) aus tokens/tokens.json. Schrift: Arial (Office-Fallback laut Markenportal)."""
import json, pathlib, re, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from lxml import etree

root = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((root / "tokens/tokens.json").read_text())
C = {k: v["value"].lstrip("#").upper() for k, v in T["color"].items()}
FONT = T["font"]["office-fallback"]["value"]
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
A = "{%s}" % NS["a"]

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
W, H = prs.slide_width, prs.slide_height
X = H // 14  # Rasterkante X = 1/14 der kuerzeren Seite
master = prs.slide_master

# ---- Theme: Farben + Schriften
tp = master.part.part_related_by(RT.THEME)
xml = tp.blob.decode("utf8")
scheme = {"dk1": C["primary"], "lt1": C["white"], "dk2": C["primary"], "lt2": C["sand"],
          "accent1": C["orange-dark"], "accent2": C["mint-dark"], "accent3": C["green-4"],
          "accent4": C["brown-3"], "accent5": C["blue-4"], "accent6": C["grey-5"],
          "hlink": C["mint-dark"], "folHlink": C["brown-4"]}
clr = '<a:clrScheme name="R+V">' + "".join(
    f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in scheme.items()) + "</a:clrScheme>"
xml = re.sub(r"<a:clrScheme.*?</a:clrScheme>", clr, xml, flags=re.S)
xml = re.sub(r'(<a:majorFont>\s*<a:latin typeface=")[^"]*', r"\g<1>" + FONT, xml)
xml = re.sub(r'(<a:minorFont>\s*<a:latin typeface=")[^"]*', r"\g<1>" + FONT, xml)
xml = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="R+V"', xml)
tp._blob = xml.encode("utf8")

def set_fill(sp_pr_parent, hexv):
    for tag in ("solidFill", "noFill"):
        for e in sp_pr_parent.findall(A + tag):
            sp_pr_parent.remove(e)

def set_bg(el, hexv):
    cSld = el._element.find("p:cSld", NS)
    for b in cSld.findall("p:bg", NS):
        cSld.remove(b)
    bg = etree.fromstring(f'<p:bg xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}"><p:bgPr><a:solidFill><a:srgbClr val="{hexv}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>')
    cSld.insert(0, bg)

def style_text(shape, size, bold, color, caps=False, face=None):
    """Setzt lstStyle lvl1 des Platzhalters."""
    tx = shape._element.find("p:txBody", NS)
    ls = tx.find("a:lstStyle", NS)
    for c in list(ls):
        ls.remove(c)
    f = f'<a:latin typeface="{face}"/>' if face else ""
    ls.append(etree.fromstring(
        f'<a:lvl1pPr xmlns:a="{NS["a"]}" marL="0" indent="0" algn="l"><a:buNone/>'
        f'<a:defRPr sz="{int(size*100)}" b="{1 if bold else 0}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{f}</a:defRPr></a:lvl1pPr>'))

def place(shape, l, t, w, h):
    shape.left, shape.top, shape.width, shape.height = int(l), int(t), int(w), int(h)

_id = [100]
def _sp(layout, name, l, t, w, h, fill=None, text=None, color=None):
    _id[0] += 1
    f = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
    body = ""
    if text:
        body = (f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/>'
                f'<a:p><a:r><a:rPr lang="de-DE" sz="2400" b="1"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr><a:t>{text}</a:t></a:r></a:p></p:txBody>')
    xml = (f'<p:sp xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}"><p:nvSpPr><p:cNvPr id="{_id[0]}" name="{name}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
           f'<p:spPr><a:xfrm><a:off x="{int(l)}" y="{int(t)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
           f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{f}<a:ln><a:noFill/></a:ln></p:spPr>{body}</p:sp>')
    layout._element.find("p:cSld/p:spTree", NS).append(etree.fromstring(xml))

def rect(layout, l, t, w, h, hexv):
    _sp(layout, "Akzent", l, t, w, h, fill=hexv)

def logo_box(layout, dark):
    """Logo-Platzhalter 4X breit, Ecke unten links (ohne Schutzzone)."""
    _sp(layout, "Logo-Platzhalter", X, H - 1.5 * X, 4 * X, 0.8 * X, text="R+V",
        color=C["white"] if dark else C["primary"])

# ---- Master: Default-Template ist 4:3, Platzhalter auf 16:9 skalieren
for sh in master.shapes:
    sh.left, sh.width = int(sh.left * W / 9144000), int(sh.width * W / 9144000)
# ---- Master: Hintergrund weiss, Titel/Body
set_bg(master, C["white"])
by = {l.name: l for l in prs.slide_layouts}
keep = ["Title Slide", "Title and Content", "Section Header", "Two Content", "Title Only", "Blank"]
ids = master._element.find("p:sldLayoutIdLst", NS)
for l in list(prs.slide_layouts):
    if l.name not in keep:
        prs.slide_layouts.remove(l)
names = {"Title Slide": "Titelfolie", "Title and Content": "Titel und Inhalt", "Section Header": "Kapitel",
         "Two Content": "Zwei Inhalte", "Title Only": "Nur Titel", "Blank": "Leer"}

for l in prs.slide_layouts:
    nm = l.name; l.name = names[nm]
    dark = nm in ("Title Slide", "Section Header")
    set_bg(l, C["primary"] if dark else C["white"])
    ph = {p.placeholder_format.type: p for p in l.placeholders}
    for p in l.placeholders:
        t = p.placeholder_format.type
        n = str(t)
        if "TITLE" in n and "SUBTITLE" not in n:  # TITLE / CENTER_TITLE
            if dark:
                place(p, X, 3*X, 10*X, 4*X)
                style_text(p, 44, True, C["white"])
                p._element.find("p:txBody/a:bodyPr", NS).set("anchor", "b")
            else:
                place(p, X, 0.8*X, W - 2*X, 1.6*X)
                style_text(p, 32, True, C["primary"])
                p._element.find("p:txBody/a:bodyPr", NS).set("anchor", "t")
        elif "SUBTITLE" in n or ("BODY" in n and dark):
            place(p, X, 7.3*X, 10*X, 2*X)
            style_text(p, 20, False, C["orange-light"], face=None)
        elif "OBJECT" in n or "BODY" in n:
            idx = p.placeholder_format.idx
            if nm == "Two Content":
                w = (W - 3*X) / 2
                place(p, X + (0 if idx == 1 else w + X), 3*X, w, 8*X)
            else:
                place(p, X, 3*X, W - 2*X, 8*X)
            style_text(p, 18, False, C["primary"])
        elif any(k in n for k in ("DATE", "FOOTER", "SLIDE_NUMBER")):
            p._element.getparent().remove(p._element)
    if nm != "Blank":
        logo_box(l, dark)
    if not dark and nm != "Blank":
        rect(l, 0, 0, X * 0.35, H, C["orange-dark"])  # Akzentstreifen links

# ---- Layout-Titel in Folien: Oberkante Topline-Konvention dokumentiert in README
prs.save(root / "templates/ruv.pptx")
print("ok")
