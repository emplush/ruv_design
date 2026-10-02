#!/usr/bin/env python3
"""Erzeugt templates/ruv.pptx (16:9) aus tokens/tokens.json und assets/logo.
Aufruf: python3 scripts/build_pptx.py [--title "Titel der Präsentation"] [--out pfad.pptx]
Schrift: Arial (Office-Fallback laut Markenportal). Maße nach der R+V-Vorlage:
 Startseite: links Dunkelblau mit Logo + Claim, Zeile Ort/Datum (weiß), Haupttitel (orange), Untertitel (weiß);
             rechts Bild (Platzhalter). Inhaltsseiten: Hauptheadline blau, Unterheadline orange,
             unten links Foliennummer + Titel der Präsentation + Datum, unten rechts Logo."""
import argparse, json, pathlib, re
from pptx import Presentation
from pptx.util import Emu
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from lxml import etree

ap = argparse.ArgumentParser()
ap.add_argument("--title", default="Titel der Präsentation", help="Fußzeilentitel auf allen Inhaltsseiten")
ap.add_argument("--out", default=None)
args = ap.parse_args()

root = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((root / "tokens/tokens.json").read_text())
C = {k: v["value"].lstrip("#").upper() for k, v in T["color"].items()}
FONT = T["font"]["office-fallback"]["value"]
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
DECL = f'xmlns:p="{NS["p"]}" xmlns:a="{NS["a"]}" xmlns:r="{NS["r"]}"'

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
W, H = prs.slide_width, prs.slide_height
master = prs.slide_master

# ---- Theme: Farben + Schriften
tp = master.part.part_related_by(RT.THEME)
xml = tp.blob.decode("utf8")
scheme = {"dk1": C["primary"], "lt1": C["white"], "dk2": C["primary"], "lt2": C["sand"],
          "accent1": C["orange-dark"], "accent2": C["mint-dark"], "accent3": C["green-4"],
          "accent4": C["brown-3"], "accent5": C["blue-4"], "accent6": C["grey-5"],
          "hlink": C["mint-dark"], "folHlink": C["brown-4"]}
clr = '<a:clrScheme name="R+V">' + "".join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in scheme.items()) + "</a:clrScheme>"
xml = re.sub(r"<a:clrScheme.*?</a:clrScheme>", clr, xml, flags=re.S)
xml = re.sub(r'(<a:majorFont>\s*<a:latin typeface=")[^"]*', r"\g<1>" + FONT, xml)
xml = re.sub(r'(<a:minorFont>\s*<a:latin typeface=")[^"]*', r"\g<1>" + FONT, xml)
xml = re.sub(r'<a:fontScheme name="[^"]*"', '<a:fontScheme name="R+V"', xml)
tp._blob = xml.encode("utf8")

def set_bg(el, hexv):
    cSld = el._element.find("p:cSld", NS)
    for b in cSld.findall("p:bg", NS):
        cSld.remove(b)
    cSld.insert(0, etree.fromstring(f'<p:bg {DECL}><p:bgPr><a:solidFill><a:srgbClr val="{hexv}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'))

# Default-Template ist 4:3: Masterplatzhalter auf 16:9 skalieren, Hintergrund weiß
for sh in master.shapes:
    sh.left, sh.width = int(sh.left * W / 9144000), int(sh.width * W / 9144000)
set_bg(master, C["white"])

# ---- Layout-Bausteine (alle Maße in EMU, aus den R+V-Vorlagen übernommen)
_id = [100]
def nid():
    _id[0] += 1
    return _id[0]

def clear(layout):
    tree = layout._element.find("p:cSld/p:spTree", NS)
    for sp in tree.findall("p:sp", NS) + tree.findall("p:pic", NS):
        tree.remove(sp)
    return tree

def add(tree, xml):
    tree.append(etree.fromstring(xml))

def lvl(size, bold, color, ls=None):
    sp = f'<a:lnSpc><a:spcPct val="{ls}"/></a:lnSpc>' if ls else ""
    return (f'<a:lvl1pPr marL="0" indent="0" algn="l">{sp}<a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/>'
            f'<a:defRPr sz="{int(size*100)}" b="{int(bold)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:defRPr></a:lvl1pPr>')

def ph(tree, name, typ, idx, x, y, w, h, size, bold, color, prompt, anchor="t", ls=None):
    """Textplatzhalter mit Aufforderungstext. typ: ctrTitle|title|subTitle|body|obj"""
    attr = {"ctrTitle": 'type="ctrTitle"', "title": 'type="title"', "subTitle": f'type="subTitle" idx="{idx}"',
            "body": f'type="body" sz="quarter" idx="{idx}"', "obj": f'idx="{idx}"'}[typ]
    add(tree, f'<p:sp {DECL}><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph {attr}/></p:nvPr></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm></p:spPr>'
              f'<p:txBody><a:bodyPr lIns="36000" tIns="0" rIns="36000" bIns="0" anchor="{anchor}"><a:normAutofit/></a:bodyPr>'
              f'<a:lstStyle>{lvl(size, bold, color, ls)}</a:lstStyle><a:p><a:r><a:rPr lang="de-DE"/><a:t>{prompt}</a:t></a:r></a:p></p:txBody></p:sp>')

def pic_ph(tree, x, y, w, h):
    add(tree, f'<p:sp {DECL}><p:nvSpPr><p:cNvPr id="{nid()}" name="Bild"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="pic" idx="14"/></p:nvPr></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm></p:spPr>'
              f'<p:txBody><a:bodyPr anchor="ctr"/><a:lstStyle><a:lvl1pPr marL="0" indent="0" algn="ctr"><a:buNone/><a:defRPr sz="1400"><a:solidFill><a:srgbClr val="{C["white"]}"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>'
              f'<a:p><a:r><a:rPr lang="de-DE"/><a:t>Bild zum Thema der Präsentation einfügen</a:t></a:r></a:p></p:txBody></p:sp>')

def rect(tree, name, x, y, w, h, fill):
    add(tree, f'<p:sp {DECL}><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
              f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>')

def textbox(tree, name, x, y, w, h, runs, anchor="t"):
    """runs: Liste (Absatz) von (text|('fld', typ, text), size, bold, color)"""
    paras = ""
    for para in runs:
        inner = ""
        for item, size, bold, color in para:
            rpr = f'<a:rPr lang="de-DE" sz="{int(size*100)}" b="{int(bold)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>'
            if isinstance(item, tuple):
                inner += f'<a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B{nid():02d}}}" type="{item[1]}">{rpr}<a:t>{item[2]}</a:t></a:fld>'
            else:
                inner += f'<a:r>{rpr}<a:t>{item}</a:t></a:r>'
        paras += f'<a:p>{inner}</a:p>'
    add(tree, f'<p:sp {DECL}><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>'
              f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
              f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"/><a:lstStyle/>{paras}</p:txBody></p:sp>')

# Logo-Dateien enthalten die Schutzzone. Sichtbarer Anteil (aus dem PNG gemessen):
LOGO = {"ohne": dict(fw=791, fh=531, bb=(177, 176, 614, 355), f="assets/logo/ruv-logo_ohne-claim_{t}.png"),
        "claim": dict(fw=1062, fh=720, bb=(176, 177, 886, 544), f="assets/logo/ruv-logo_claim-links_{t}.png"),
        "gfg": dict(fw=1062, fh=554, bb=(190, 189, 869, 364), f="assets/logo-gfg/gfg-logo_deskriptor_links_{t}.png")}
def logo(layout, tree, kind, tone, vis_left, vis_top, vis_w):
    """Setzt das Logo so, dass der SICHTBARE Teil bei (vis_left, vis_top) mit Breite vis_w sitzt."""
    g = LOGO[kind]
    _, rid = layout.part.get_or_add_image_part(str(root / g["f"].format(t=tone)))
    bw = g["bb"][2] - g["bb"][0]
    s = vis_w / bw                      # EMU je Bildpixel
    w, h = g["fw"] * s, g["fh"] * s
    l, t = vis_left - g["bb"][0] * s, vis_top - g["bb"][1] * s
    add(tree, f'<p:pic {DECL}><p:nvPicPr><p:cNvPr id="{nid()}" name="Logo" descr="R+V Logo"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr userDrawn="1"/></p:nvPicPr>'
              f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
              f'<p:spPr><a:xfrm><a:off x="{int(l)}" y="{int(t)}"/><a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

PX = W / 1363           # Maße der Startfolie: Screenshot 1363 px breit
CX = W / 1357           # Maße der Inhaltsfolie: Screenshot 1357 px breit
PANEL_W = 683 * PX      # dunkle Fläche links, Bild rechts

def footer(tree, layout):
    """Unten links: Foliennummer, Titel der Präsentation, Datum; unten rechts: Logo."""
    textbox(tree, "Foliennummer", 58 * CX, 0.9055 * H, 40 * CX, 0.02 * H * 1.6, [[(("fld", "slidenum", "‹#›"), 11, True, C["primary"])]])
    textbox(tree, "Titel der Präsentation", 111 * CX, 0.9055 * H, 700 * CX, 0.0525 * H,
            [[(args.title, 11, True, C["primary"])], [(("fld", "datetime1", "01.01.2026"), 11, False, C["primary"])]])
    logo(layout, tree, "ohne", "positiv", 1228 * CX, 706 / 767 * H, 64 * CX)

# ---- Layouts: nur die gebrauchten behalten
names = {"Title Slide": "Startseite", "Section Header": "Kapitel", "Title and Content": "Titel und Inhalt",
         "Two Content": "Zwei Inhalte", "Title Only": "Nur Titel", "Blank": "Leer"}
for l in list(prs.slide_layouts):
    if l.name not in names:
        prs.slide_layouts.remove(l)

TXT_X = 57 * CX
for l in prs.slide_layouts:
    orig = l.name; l.name = names[orig]
    tree = clear(l)
    if orig == "Title Slide":
        set_bg(l, C["white"])
        rect(tree, "Dunkelblaue Fläche", 0, 0, PANEL_W, H, C["primary"])
        pic_ph(tree, PANEL_W, 0, W - PANEL_W, H)
        logo(l, tree, "claim", "negativ", 60 * PX, 62 / 775 * H, 215 * PX)
        ph(tree, "Ort, Datum, Referentin oder Referent", "body", 13, 59 * PX, 0.365 * H, 578 * PX, 0.04 * H, 20, False, C["white"], "Ort, Datum, Referentin oder Referent", "ctr")
        ph(tree, "Haupttitel", "ctrTitle", 0, 59 * PX, 0.4105 * H, 578 * PX, 0.136 * H, 36, True, C["orange-light"], "Haupttitel", "t", 95000)
        ph(tree, "Untertitel", "subTitle", 1, 59 * PX, 0.557 * H, 578 * PX, 0.134 * H, 32, True, C["white"], "Untertitel", "t", 95000)
        # "Die Versicherung in der" + Logo der Genossenschaftlichen Finanzgruppe (Deskriptor-Logo, weiß), unten links
        logo(l, tree, "gfg", "negativ", 60 * PX, 668 / 775 * H, 188 * PX)
    elif orig == "Section Header":
        set_bg(l, C["primary"])
        logo(l, tree, "claim", "negativ", 60 * PX, 62 / 775 * H, 215 * PX)
        ph(tree, "Haupttitel", "title", 0, 59 * PX, 0.4105 * H, 900 * PX, 0.136 * H, 36, True, C["orange-light"], "Kapitelüberschrift", "t", 95000)
        ph(tree, "Untertitel", "body", 13, 59 * PX, 0.557 * H, 900 * PX, 0.134 * H, 32, True, C["white"], "Untertitel", "t", 95000)
    elif orig == "Blank":
        set_bg(l, C["white"])
    else:
        set_bg(l, C["white"])
        ph(tree, "Hauptheadline", "title", 0, TXT_X, 30 / 767 * H, 1238 * CX, 45 / 767 * H, 28, True, C["primary"], "Hauptheadline", "b")
        ph(tree, "Unterheadline", "body", 13, TXT_X, 76 / 767 * H, 1238 * CX, 37 / 767 * H, 28, True, C["orange-dark"], "Unterheadline", "t")
        top, bh = 150 / 767 * H, 530 / 767 * H
        if orig == "Two Content":
            gap = 24 * CX; half = (1238 * CX - gap) / 2
            ph(tree, "Inhalt links", "obj", 1, TXT_X, top, half, bh, 18, False, C["primary"], "Inhalt")
            ph(tree, "Inhalt rechts", "obj", 2, TXT_X + half + gap, top, half, bh, 18, False, C["primary"], "Inhalt")
        elif orig == "Title and Content":
            ph(tree, "Inhalt", "obj", 1, TXT_X, top, 1238 * CX, bh, 18, False, C["primary"], "Inhalt")
        footer(tree, l)

prs.save(args.out or root / "templates/ruv.pptx")
print("ok")
