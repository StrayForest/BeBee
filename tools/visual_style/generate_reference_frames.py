#!/usr/bin/env python3
"""Generate deterministic BB-P007 SVG style-reference frames using only stdlib."""
from __future__ import annotations

import argparse
import json
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "visual-style.json"
DEFAULT_OUT = Path(tempfile.gettempdir()) / "bebee-bbp007-reference-frames"


def attrs(values: dict[str, object]) -> str:
    return " ".join(f'{k}="{escape(str(v), quote=True)}"' for k, v in values.items())


def el(name: str, values: dict[str, object], body: str = "") -> str:
    return f"<{name} {attrs(values)}>{body}</{name}>"


def self_el(name: str, values: dict[str, object]) -> str:
    return f"<{name} {attrs(values)}/>"


class Scene:
    def __init__(self, width: int, height: int, palette: dict[str, str]):
        self.w = width
        self.h = height
        self.p = palette
        self.parts: list[str] = []
        self.sx = width / 1280
        self.sy = height / 720
        self.s = min(self.sx, self.sy)

    def X(self, x: float) -> float: return round(x * self.sx, 2)
    def Y(self, y: float) -> float: return round(y * self.sy, 2)
    def S(self, x: float) -> float: return round(x * self.s, 2)

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, sw=0, opacity=1):
        a = {"x": self.X(x), "y": self.Y(y), "width": self.X(w), "height": self.Y(h), "fill": fill, "opacity": opacity}
        if rx: a["rx"] = self.S(rx)
        if stroke: a.update(stroke=stroke, **{"stroke-width": self.S(sw)})
        self.parts.append(self_el("rect", a))

    def circle(self, x, y, r, fill, stroke=None, sw=0, opacity=1):
        a = {"cx": self.X(x), "cy": self.Y(y), "r": self.S(r), "fill": fill, "opacity": opacity}
        if stroke: a.update(stroke=stroke, **{"stroke-width": self.S(sw)})
        self.parts.append(self_el("circle", a))

    def ellipse(self, x, y, rx, ry, fill, opacity=1, stroke=None, sw=0):
        a = {"cx": self.X(x), "cy": self.Y(y), "rx": self.S(rx), "ry": self.S(ry), "fill": fill, "opacity": opacity}
        if stroke: a.update(stroke=stroke, **{"stroke-width": self.S(sw)})
        self.parts.append(self_el("ellipse", a))

    def line(self, x1, y1, x2, y2, stroke, sw=2, opacity=1):
        self.parts.append(self_el("line", {"x1": self.X(x1), "y1": self.Y(y1), "x2": self.X(x2), "y2": self.Y(y2), "stroke": stroke, "stroke-width": self.S(sw), "stroke-linecap": "round", "opacity": opacity}))

    def text(self, value, x, y, size=24, weight=700, fill=None, anchor="start"):
        fill = fill or self.p["ink"]
        self.parts.append(el("text", {"x": self.X(x), "y": self.Y(y), "font-family": "Arial,Helvetica,sans-serif", "font-size": self.S(size), "font-weight": weight, "fill": fill, "text-anchor": anchor, "dominant-baseline": "middle"}, escape(str(value))))

    def shadow(self, x, y, rx=38, ry=14, opacity=.2):
        self.ellipse(x, y, rx, ry, "#30402F", opacity)

    def island(self, dormant=False):
        self.rect(0, 0, 1280, 720, "#BFEAF0")
        self.rect(55, 72, 1170, 620, "#4D8C59", 56)
        self.rect(55, 38, 1170, 620, self.p["dormant_ground"] if dormant else self.p["grass"], 56)
        if not dormant:
            for x, y, rx, ry in [(160, 130, 115, 45), (510, 98, 145, 48), (900, 130, 150, 42), (250, 465, 180, 65), (870, 490, 200, 60)]:
                self.ellipse(x, y, rx, ry, "#66B957", .65)

    def tree(self, x, y, dormant=False):
        self.shadow(x, y + 48, 45, 13, .14)
        self.rect(x - 8, y + 4, 16, 58, "#79513A", 6)
        leaf = "#747F63" if dormant else "#4E9C55"
        for dx, dy, r in [(0, 0, 42), (-28, 12, 30), (27, 14, 31), (2, -28, 28)]: self.circle(x + dx, y + dy, r, leaf)

    def decor(self, dormant=False):
        for x, y in [(175, 170), (1040, 160), (1060, 515), (195, 520)]: self.tree(x, y, dormant)

    def flower(self, x, y, kind="daisy", scale=1.0, closed=False):
        self.shadow(x, y + 17, 16 * scale, 6 * scale, .14)
        self.line(x, y + 19, x, y - 5, self.p["grass_dark"], 3 * scale)
        if closed:
            self.ellipse(x, y - 12, 12 * scale, 18 * scale, self.p["locked"], .96, self.p["ink"], 1.5)
            return
        colors = {
            "daisy": ("#FFF8E9", "#F8C64A"),
            "clover": ("#E777A8", "#F5B5CE"),
            "lavender": ("#A789DE", "#CBBBF0"),
            "lily": ("#E4D5FF", "#F5C36A"),
        }
        petal, center = colors[kind]
        offsets = [(0,-16),(12,-10),(16,2),(10,13),(0,17),(-11,13),(-16,2),(-12,-10)]
        if kind == "lily": offsets = [(0,-18),(15,-9),(15,10),(0,18),(-15,10),(-15,-9)]
        for dx, dy in offsets: self.ellipse(x+dx*scale, y+dy*scale, 7*scale, 11*scale, petal, 1, self.p["ink"], .9)
        self.circle(x, y, 6 * scale, center)

    def patch(self, cx, cy, kind="daisy", count=9, closed=False):
        pts=[(-64,-28),(-28,-52),(12,-46),(52,-24),(-51,14),(-12,10),(31,10),(67,18),(-6,47),(45,52),(-75,51)]
        for i,(dx,dy) in enumerate(pts[:count]): self.flower(cx+dx, cy+dy, kind, .92+(i%3)*.07, closed)

    def bee(self, x, y, scale=1.0, active=False):
        self.shadow(x, y+47*scale, 40*scale, 14*scale, .2)
        self.ellipse(x-28*scale, y-26*scale, 28*scale, 17*scale, "#ECFAFF", .78, self.p["ink"], 2)
        self.ellipse(x+28*scale, y-26*scale, 28*scale, 17*scale, "#ECFAFF", .78, self.p["ink"], 2)
        self.ellipse(x, y+4*scale, 40*scale, 47*scale, "#F8C548", 1, self.p["ink"], 3)
        self.line(x-34*scale, y+2*scale, x+34*scale, y+2*scale, self.p["ink"], 8*scale)
        self.line(x-29*scale, y+22*scale, x+29*scale, y+22*scale, self.p["ink"], 8*scale)
        self.circle(x-14*scale, y-9*scale, 4.5*scale, self.p["ink"])
        self.circle(x+14*scale, y-9*scale, 4.5*scale, self.p["ink"])
        if active:
            self.circle(x, y, 61*scale, "none", self.p["active"], 3)

    def pill(self, x, y, w, h, fill, stroke=None): self.rect(x, y, w, h, fill, h/2, stroke, 2 if stroke else 0)

    def hud(self, objective="Pollinate the daisies", honey=120):
        self.pill(34,30,410,70,"#FFF7E8", "#C99567")
        self.text(objective,68,65,25,700)
        self.pill(1004,30,238,70,"#FFF7E8", "#C99567")
        self.circle(1046,65,18,self.p["honey"]); self.circle(1046,60,7,self.p["honey_dark"])
        self.text(honey,1080,65,30,800,self.p["honey_dark"])

    def svg(self, label: str) -> str:
        meta = f"<!-- BB-P007 deterministic reference: {label}; generated by tools/visual_style/generate_reference_frames.py -->"
        body = "\n  ".join(self.parts)
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="BeBee {escape(label)} reference frame">\n{meta}\n  {body}\n</svg>\n'''


def frame_gameplay(sc: Scene):
    sc.island(); sc.decor(); sc.hud(); sc.patch(380,330,"daisy",10); sc.patch(860,420,"clover",8); sc.patch(870,215,"lavender",7); sc.bee(610,360,1.04)

def frame_pollination(sc: Scene):
    sc.island(); sc.decor(); sc.hud("Pollinate: Daisy Patch",136); sc.patch(655,360,"daisy",10)
    pts=[(-78,-12),(-56,-46),(-25,-67),(8,-76),(44,-58),(70,-24),(82,9),(54,43),(19,67),(-20,61),(-55,39)]
    for i,(dx,dy) in enumerate(pts): sc.circle(640+dx,345+dy,5+(i%3)*2, sc.p["honey"] if i%2 else sc.p["active"], opacity=.35+(i%4)*.1)
    sc.bee(585,330,1.04,True); sc.pill(490,565,300,54,"#493B32"); sc.text("Bloom 68%",640,592,22,800,"#FFFDF7","middle")

def frame_locked(sc: Scene):
    sc.island(); sc.decor(); sc.hud("Reach Buzz 2",120); sc.patch(820,330,"lily",8,True); sc.bee(610,365,1.04)
    sc.circle(820,330,110,"none",sc.p["locked"],4); sc.pill(752,190,136,58,"#FFF7E8","#C99567")
    sc.rect(773,209,24,20,sc.p["ink"],4); sc.circle(785,208,9,"none",sc.p["ink"],4); sc.text("Buzz 2",815,220,20,800)

def frame_dormant(sc: Scene):
    sc.island(True); sc.decor(True); sc.hud("Wake the meadow",48); sc.bee(560,385,1.02)
    for x,y in [(350,300),(780,310),(900,460)]: sc.ellipse(x,y,95,48,"#806E56",.75); sc.patch(x,y,"daisy",4,True)

def frame_restored(sc: Scene):
    sc.island(); sc.decor(); sc.hud("Meadow restored",188); sc.patch(350,300,"daisy",10); sc.patch(770,315,"clover",10); sc.patch(930,470,"lavender",9); sc.patch(555,510,"lily",6); sc.bee(585,375,1.02)
    for x,y in [(470,180),(760,540),(980,270)]: sc.circle(x,y,5,sc.p["honey"],opacity=.6)

def frame_hive(sc: Scene):
    sc.island(); sc.rect(0,0,1280,720,"#1E2D24",opacity=.32); sc.rect(180,90,920,540,"#FFF7E8",36,"#C99567",3); sc.text("Hive",240,145,38,800); sc.text("Improve what you feel while flying",240,188,22,500,"#6E5A4D"); sc.bee(360,360,1.3)
    sc.rect(520,235,470,110,"#FFFDF7",24,"#C99567",2); sc.text("Flight",560,275,28,800); sc.text("Faster movement, same control",560,315,19,500,"#6E5A4D")
    sc.rect(520,380,470,110,"#FFFDF7",24,"#C99567",2); sc.text("Buzz",560,420,28,800); sc.text("Pollinate harder flowers",560,460,19,500,"#6E5A4D")
    sc.pill(765,525,225,68,sc.p["honey"]); sc.text("Improve · 80",877,560,24,800,sc.p["honey_dark"],"middle")

def seed_card(sc: Scene, x, label, color, owned=True):
    sc.rect(x,458,250,160,"#FFFDF7",24,"#C99567",2); sc.circle(x+52,498,23,color); sc.text(label,x+92,498,24,800); sc.text("Owned" if owned else "40 Honey",x+92,532,18,600, sc.p["grass_dark"] if owned else sc.p["honey_dark"]); sc.pill(x+28,562,194,38,sc.p["success"] if owned else "#E8D3B8"); sc.text("Plant" if owned else "Unlock",x+125,581,18,800,sc.p["ink"],"middle")

def frame_seeds(sc: Scene):
    sc.island(); sc.decor(); sc.hud("Choose what blooms here",140); sc.bee(620,280,1.03); sc.rect(0,392,1280,328,"#1E2D24",opacity=.22); sc.rect(105,395,1070,250,"#FFF7E8",30,"#C99567",2); sc.text("Shape this recovering patch",155,430,28,800); seed_card(sc,155,"Daisy","#F8C64A",True); seed_card(sc,515,"Clover","#E777A8",True); seed_card(sc,875,"Lavender","#A789DE",False)

def frame_mobile(sc: Scene):
    sc.island(); sc.decor(); sc.hud("Pollinate daisies",92); sc.patch(410,350,"daisy",8); sc.patch(930,330,"lavender",6); sc.bee(655,370,1.02); sc.rect(1070,535,150,110,"#FFF7E8",34,"#C99567",2); sc.circle(1145,590,25,"none",sc.p["ink"],5)

FRAMES = {
    "gameplay_default": frame_gameplay,
    "pollination_active": frame_pollination,
    "hard_flower_locked": frame_locked,
    "meadow_dormant": frame_dormant,
    "meadow_restored": frame_restored,
    "hive_improvement": frame_hive,
    "seed_choice": frame_seeds,
    "mobile_gameplay": frame_mobile,
}


def generate(config_path: Path, out_dir: Path) -> list[Path]:
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    palette = cfg["palette"]
    out_dir.mkdir(parents=True, exist_ok=True)
    made=[]
    for spec in cfg["approved_frames"]:
        frame_id=spec["id"]
        if frame_id not in FRAMES: raise SystemExit(f"unknown frame id in config: {frame_id}")
        width,height=map(int,spec["viewport"])
        sc=Scene(width,height,palette)
        FRAMES[frame_id](sc)
        target=out_dir/f"{frame_id}.svg"
        target.write_text(sc.svg(frame_id),encoding="utf-8")
        made.append(target)
    return made


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args=parser.parse_args()
    made=generate(args.config,args.out)
    for path in made: print(path)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
