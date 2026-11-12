#!/usr/bin/env python3
"""
Generate the KHUSHI.OS pastel panels for the profile README as lightweight SVGs:

  assets/boot.svg               animated boot sequence + hero line (plays once)
  assets/about-card.svg         RPG-style character panel (facts only, no levels)
  assets/tech-inventory.svg     skills as pastel chips, grouped by category
  assets/project-reconengine.svg  pixel thumbnail: ledger matching animation
  assets/project-campustrade.svg  pixel thumbnail: marketplace feed + chat pulse

Every number and claim here comes from the resume (the source of truth). Edit the
CONTENT blocks below to change text; the layout re-flows automatically.

GitHub renders these through <img>: SMIL and CSS animations run, scripts do not,
and no external fonts are loaded (everything falls back to system fonts).

Usage:  python scripts/make_khushios_assets.py            (writes into assets/)
        STATIC=1 python scripts/make_khushios_assets.py   (frozen end state)
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
STATIC = bool(os.environ.get("STATIC"))

# ---- KHUSHI.OS palette -----------------------------------------------------
CREAM = "#FFF9EE"
LAVENDER = "#DCCEFF"
MINT = "#BFE8D5"
BUTTER = "#FFF0A8"
PEACH = "#FFD6C2"
PLUM = "#382F4A"
MUTED = "#786A91"
OK_GREEN = "#2F8F6B"
PASTELS = [LAVENDER, MINT, BUTTER, PEACH]

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
SANS = "ui-rounded, 'Trebuchet MS', Verdana, Helvetica, Arial, sans-serif"
PIXEL = "'Press Start 2P', 'Courier New', monospace"   # remote font may fail; monospace fallback


def esc(s):
    return html.escape(s, quote=True)


def svg_open(w, h, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{esc(label)}">'
    )


def window_chrome(w, title, bar_h=34):
    """Rounded cream window with a lavender title bar and pastel window dots."""
    out = [
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{{h}}" rx="16" fill="{CREAM}" stroke="{PLUM}" stroke-width="1.5"/>',
        f'<path d="M0.75 16.75 a16 16 0 0 1 16 -16 H{w - 16.75} a16 16 0 0 1 16 16 V{bar_h} H0.75 Z" fill="{LAVENDER}"/>',
        f'<line x1="0.75" y1="{bar_h}" x2="{w - 0.75}" y2="{bar_h}" stroke="{PLUM}" stroke-width="1.5"/>',
    ]
    for i, c in enumerate([PEACH, BUTTER, MINT]):
        out.append(f'<circle cx="{18 + i * 16}" cy="{bar_h / 2}" r="5" fill="{c}" stroke="{PLUM}" stroke-width="1"/>')
    out.append(
        f'<text x="{w / 2}" y="{bar_h / 2 + 4.5}" fill="{PLUM}" font-family="{MONO}" font-size="12.5" '
        f'text-anchor="middle">{esc(title)}</text>'
    )
    return out


def finish(parts, h):
    body = "\n".join(parts).replace("{h}", str(h))
    return body + "\n</svg>\n"


def write(name, text):
    path = os.path.join(ASSETS, name)
    os.makedirs(ASSETS, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {path} ({len(text) // 1024 or 1} KB)")


# =============================================================================
#  1. BOOT SEQUENCE (hero)
# =============================================================================
BOOT_LINES = [
    ("", "KHUSHI.OS v1.0  ·  boot sequence", PLUM, True),
    ("[ OK ]", "mounting B.Tech Computer Engineering · PICT, Pune", PLUM, False),
    ("[ OK ]", "loading backend stack: Node.js · Express · FastAPI · PostgreSQL", PLUM, False),
    ("[ OK ]", "loading AI runtime: LangGraph · multi-agent orchestration", PLUM, False),
    ("[ OK ]", "6 months of backend development experience, shipping features", PLUM, False),
    ("[ OK ]", "CI/CD hooks armed: GitHub Actions · Docker", PLUM, False),
]
BOOT_HELLO = "Hello, World. I'm Khushi."
BOOT_TAGLINE = "Backend developer building reliable systems and practical AI-driven apps."


def make_boot():
    w, h = 860, 384
    bar_h = 34
    parts = [svg_open(w, h, "KHUSHI.OS boot sequence: Hello, World. I'm Khushi.")]
    parts.append("<defs>")
    parts.append(
        f'<linearGradient id="boot-bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{CREAM}"/><stop offset="1" stop-color="#F4ECFF"/></linearGradient>'
    )
    parts.append("</defs>")
    parts.append(f'<rect x="0" y="0" width="{w}" height="{{h}}" rx="16" fill="url(#boot-bg)"/>')
    parts.extend(window_chrome(w, "khushi@os: ~/boot", bar_h))

    y = bar_h + 36
    step = 27.5
    t = 0.35  # first line starts shortly after load
    for i, (tag, text, colour, bold) in enumerate(BOOT_LINES):
        clip_id = f"bl{i}"
        width = 14 + len(tag) * 8.4 + len(text) * 8.1
        dur = 0.5 + len(text) * 0.012
        parts.append(
            f'<clipPath id="{clip_id}"><rect x="28" y="{y - 20}" height="28" width="{0 if not STATIC else round(width)}">'
            f'<animate attributeName="width" from="0" to="{width:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            f"</rect></clipPath>"
        )
        weight = ' font-weight="700"' if bold else ""
        tag_part = (
            f'<tspan fill="{OK_GREEN}" font-weight="700">{esc(tag)} </tspan>' if tag else ""
        )
        parts.append(
            f'<g clip-path="url(#{clip_id})"><text x="28" y="{y}" font-family="{MONO}" font-size="16"{weight} '
            f'fill="{colour}">{tag_part}{esc(text)}</text></g>'
        )
        t += dur * 0.55
        y += step

    # progress bar
    bar_x, bar_w = 28, 560
    by = y + 6
    parts.append(
        f'<text x="28" y="{by + 14}" font-family="{MONO}" font-size="14" fill="{MUTED}">loading profile</text>'
    )
    parts.append(
        f'<rect x="150" y="{by + 2}" width="{bar_w}" height="14" rx="7" fill="#EFE7FD" stroke="{PLUM}" stroke-width="1"/>'
    )
    parts.append(
        f'<rect x="152" y="{by + 4}" width="{bar_w - 4}" height="10" rx="5" fill="{MINT}">'
        f'<animate attributeName="width" from="0" to="{bar_w - 4}" begin="{t:.2f}s" dur="1.6s" fill="freeze"/></rect>'
    )
    parts.append(
        f'<text x="{150 + bar_w + 14}" y="{by + 14}" font-family="{MONO}" font-size="14" fill="{PLUM}">100%</text>'
    )

    # hero line + tagline, after the bar fills
    hero_t = t + 1.8
    y2 = by + 46
    parts.append(
        f'<text x="28" y="{y2}" font-family="{SANS}" font-size="30" font-weight="800" fill="{PLUM}" opacity="{0 if not STATIC else 1}">'
        f'{esc(BOOT_HELLO)}'
        + ("" if STATIC else f'<animate attributeName="opacity" from="0" to="1" begin="{hero_t:.2f}s" dur="0.6s" fill="freeze"/>')
        + "</text>"
    )
    parts.append(
        f'<text x="28" y="{y2 + 28}" font-family="{SANS}" font-size="15.5" fill="{MUTED}" opacity="{0 if not STATIC else 1}">'
        f'{esc(BOOT_TAGLINE)}'
        + ("" if STATIC else f'<animate attributeName="opacity" from="0" to="1" begin="{hero_t + 0.4:.2f}s" dur="0.6s" fill="freeze"/>')
        + "</text>"
    )
    # blinking terminal cursor, parked at the end of the prompt line
    cur_y = y2 + 62
    parts.append(
        f'<text x="28" y="{cur_y}" font-family="{MONO}" font-size="16" fill="{PLUM}">&gt; ready</text>'
    )
    parts.append(
        f'<rect x="108" y="{cur_y - 15}" width="10" height="18" fill="{PLUM}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
        f"</rect>"
    )
    write("boot.svg", finish(parts, h))


# =============================================================================
#  2. ABOUT / CHARACTER CARD (RPG status panel, facts only)
# =============================================================================
ABOUT_ROWS = [
    ("NAME", "Khushi Parag Chakke"),
    ("CLASS", "Backend developer · AI-agent builder"),
    ("BASE", "Pune, Maharashtra, India"),
    ("SCHOOL", "B.Tech CE, PICT (expected 2028)"),
    ("CGPA", "9.87 / 10"),
    ("XP LOG", "6 mo backend · research intern"),
    ("FOCUS", "backend · databases · agentic AI"),
    ("RECORD", "SEBI TechSprint finalist · 400+ DSA"),
    ("LANG", "German · Goethe A1 certified"),
]
ABOUT_FOOTER = "interests: DSA · DBMS · OOP · CI/CD · database optimization"


def make_about():
    w, h = 520, 396
    parts = [svg_open(w, h, "Character card for Khushi Parag Chakke: backend developer, AI-agent builder, based in Pune")]
    parts.append(f'<rect x="0" y="0" width="{w}" height="{{h}}" rx="16" fill="{CREAM}"/>')
    parts.extend(window_chrome(w, "character.sheet", 34))
    y = 34 + 30
    parts.append(
        f'<text x="24" y="{y}" font-family="{SANS}" font-size="15" font-weight="800" fill="{PLUM}">KHUSHI · STATUS</text>'
    )
    parts.append(
        f'<rect x="{w - 130}" y="{y - 14}" width="106" height="22" rx="11" fill="{BUTTER}" stroke="{PLUM}" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="{w - 77}" y="{y + 1}" font-family="{MONO}" font-size="11.5" text-anchor="middle" fill="{PLUM}">PROFILE</text>'
    )
    y += 18
    parts.append(f'<line x1="24" y1="{y}" x2="{w - 24}" y2="{y}" stroke="{LAVENDER}" stroke-width="2"/>')
    row_h = 27
    for i, (key, val) in enumerate(ABOUT_ROWS):
        yy = y + 24 + i * row_h
        t = 0.2 + i * 0.12
        anim = "" if STATIC else f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.4s" fill="freeze"/>'
        grp_open = "<g>" if STATIC else '<g opacity="0">'
        parts.append(
            f'{grp_open}<text x="24" y="{yy}" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{MUTED}">{esc(key)}</text>'
            f'<text x="122" y="{yy}" font-family="{SANS}" font-size="14" fill="{PLUM}">{esc(val)}</text>'
            f"{anim}</g>"
        )
    fy = y + 24 + len(ABOUT_ROWS) * row_h + 4
    parts.append(f'<line x1="24" y1="{fy}" x2="{w - 24}" y2="{fy}" stroke="{LAVENDER}" stroke-width="2"/>')
    parts.append(
        f'<text x="24" y="{fy + 24}" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{esc(ABOUT_FOOTER)}</text>'
    )
    write("about-card.svg", finish(parts, h))


# =============================================================================
#  3. TECH INVENTORY (grouped pastel chips, no proficiency scores)
# =============================================================================
TECH_GROUPS = [
    ("Languages", ["C", "C++", "Java", "Python", "JavaScript", "SQL"]),
    ("Frontend", ["React.js"]),
    ("Backend", ["Node.js", "Express.js", "FastAPI", "REST APIs", "WebSockets"]),
    ("Databases", ["PostgreSQL", "MySQL", "MongoDB"]),
    ("AI / Agents", ["LangGraph", "Multi-agent orchestration", "Stateful workflows", "Conditional routing"]),
    ("Tools", ["Git", "GitHub", "GitHub Actions", "Docker", "Linux", "CI/CD", "Agile / Scrum", "OOP", "DSA", "DBMS",
               "Unit & regression testing", "API testing"]),
]


def make_tech():
    w = 860
    label_w = 150
    chip_h = 30
    gap_x, gap_y = 9, 10
    x0 = 24
    max_x = w - 24
    usable = max_x - (x0 + label_w)
    body = []
    y = 56
    for gi, (label, items) in enumerate(TECH_GROUPS):
        # pill for the category label
        body.append(
            f'<rect x="{x0}" y="{y}" width="{label_w - 14}" height="{chip_h}" rx="{chip_h / 2}" fill="{PASTELS[gi % 4]}" '
            f'stroke="{PLUM}" stroke-width="1"/>'
        )
        body.append(
            f'<text x="{x0 + (label_w - 14) / 2}" y="{y + 20}" font-family="{SANS}" font-size="13.5" font-weight="800" '
            f'text-anchor="middle" fill="{PLUM}">{esc(label)}</text>'
        )
        cx = x0 + label_w
        cy = y
        for ii, item in enumerate(items):
            cw = len(item) * 7.4 + 26
            if cx + cw > x0 + label_w + usable:
                cx = x0 + label_w
                cy += chip_h + gap_y
            t = 0.15 + (gi * 0.35) + ii * 0.05
            fill = PASTELS[(gi + ii) % 4]
            body.append(
                f'<g opacity="0"{"" if STATIC else ""}>'
                f'<rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="{chip_h}" rx="{chip_h / 2}" fill="{fill}" '
                f'stroke="{PLUM}" stroke-width="0.8" opacity="0.92"/>'
                f'<text x="{cx + cw / 2:.1f}" y="{cy + 20}" font-family="{SANS}" font-size="13.5" text-anchor="middle" '
                f'fill="{PLUM}">{esc(item)}</text>'
                + ("" if STATIC else f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.35s" fill="freeze"/>')
                + "</g>"
            )
            if STATIC:
                body[-1] = body[-1].replace('<g opacity="0">', "<g>", 1)
            cx += cw + gap_x
        y = cy + chip_h + 22
    h = y + 4
    parts = [svg_open(w, h, "Tech inventory: languages, frontend, backend, databases, AI and agent tooling, and dev tools")]
    parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="{CREAM}"/>')
    parts.append(f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="16" fill="none" stroke="{LAVENDER}" stroke-width="1.5"/>')
    parts.append(
        f'<text x="{x0}" y="32" font-family="{SANS}" font-size="15" font-weight="800" fill="{PLUM}">'
        f'INVENTORY · languages, frameworks and tools</text>'
    )
    parts.extend(body)
    write("tech-inventory.svg", finish(parts, h))


# =============================================================================
#  4. PROJECT THUMBNAILS (pixel-style, animated, no text)
# =============================================================================
def make_recon_thumb():
    w, h = 420, 220
    parts = [svg_open(w, h, "Pixel illustration of reconciliation: ledger rows matched across two columns, with one exception flagged")]
    parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="{CREAM}" stroke="{LAVENDER}" stroke-width="2"/>')
    # two ledgers
    left_x, right_x, pill_w, pill_h = 44, 262, 114, 22
    rows = [66, 98, 130, 162]
    for i, ry in enumerate(rows):
        parts.append(f'<rect x="{left_x}" y="{ry}" width="{pill_w}" height="{pill_h}" rx="6" fill="{LAVENDER}" stroke="{PLUM}" stroke-width="1"/>')
        parts.append(f'<rect x="{right_x}" y="{ry}" width="{pill_w}" height="{pill_h}" rx="6" fill="{MINT}" stroke="{PLUM}" stroke-width="1"/>')
    parts.append(f'<text x="{left_x}" y="54" font-family="{MONO}" font-size="12" font-weight="700" fill="{PLUM}">LEDGER</text>')
    parts.append(f'<text x="{right_x}" y="54" font-family="{MONO}" font-size="12" font-weight="700" fill="{PLUM}">SETTLEMENT</text>')
    # matches: rows 0,1,3 match; row 2 is an exception (peach)
    matches = [(0, 0.4), (1, 1.0), (3, 1.6)]
    for ri, t in matches:
        ax, ay = left_x + pill_w, rows[ri] + pill_h / 2
        bx, by = right_x, rows[ri] + pill_h / 2
        length = bx - ax
        begin = t if not STATIC else 0
        parts.append(
            f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="{OK_GREEN}" stroke-width="3" stroke-linecap="round" '
            f'stroke-dasharray="{length:.0f}" stroke-dashoffset="{0 if STATIC else round(length)}">'
            + ("" if STATIC else f'<animate attributeName="stroke-dashoffset" from="{length:.0f}" to="0" begin="{begin}s" dur="0.6s" fill="freeze"/>')
            + "</line>"
        )
    # exception: unmatched row flashes peach
    ex = rows[2]
    parts.append(
        f'<rect x="{left_x - 3}" y="{ex - 3}" width="{pill_w + 6}" height="{pill_h + 6}" rx="8" fill="{PEACH}" stroke="{PLUM}" stroke-width="1.5">'
        + ("" if STATIC else '<animate attributeName="opacity" values="1;0.35;1" dur="1.6s" begin="2s" repeatCount="indefinite"/>')
        + "</rect>"
    )
    # a little pixel "scanner" sweeping down the left column
    if not STATIC:
        parts.append(
            f'<rect x="{left_x - 14}" y="62" width="5" height="{rows[-1] - 62 + pill_h}" fill="{PLUM}" opacity="0.18">'
            f'<animate attributeName="x" values="{left_x - 14};{left_x + pill_w + 6};{left_x - 14}" dur="4s" repeatCount="indefinite"/></rect>'
        )
    parts.append(
        f'<text x="{left_x}" y="{h - 16}" font-family="{MONO}" font-size="12" fill="{MUTED}">exact · tolerance · reference · composite</text>'
    )
    write("project-reconengine.svg", finish(parts, h))


def make_campus_thumb():
    w, h = 420, 220
    parts = [svg_open(w, h, "Pixel illustration of a campus marketplace: item tiles in a feed, with a chat bubble")]
    parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="{CREAM}" stroke="{LAVENDER}" stroke-width="2"/>')
    # top nav bar
    parts.append(f'<rect x="16" y="16" width="{w - 32}" height="22" rx="8" fill="{LAVENDER}" stroke="{PLUM}" stroke-width="1"/>')
    parts.append(f'<rect x="26" y="22" width="90" height="10" rx="4" fill="{PLUM}" opacity="0.5"/>')
    parts.append(f'<rect x="{w - 110}" y="22" width="84" height="10" rx="4" fill="{PLUM}" opacity="0.25"/>')
    # 3x2 feed of item tiles
    tile_w, tile_h = 86, 60
    xs = [24, 24 + 96, 24 + 192]
    ys = [46, 116]
    fills = [MINT, BUTTER, PEACH, LAVENDER, MINT, BUTTER]
    for i, (ty) in enumerate(ys):
        for j, tx in enumerate(xs):
            k = i * 3 + j
            parts.append(f'<rect x="{tx}" y="{ty}" width="{tile_w}" height="{tile_h}" rx="10" fill="{fills[k]}" stroke="{PLUM}" stroke-width="1.2"/>')
            # pixel "item": a small block with a shadow
            parts.append(f'<rect x="{tx + 22}" y="{ty + 16}" width="42" height="26" rx="4" fill="{CREAM}" stroke="{PLUM}" stroke-width="1"/>')
            parts.append(f'<rect x="{tx + 28}" y="{ty + 46}" width="30" height="5" rx="2" fill="{PLUM}" opacity="0.35"/>')
    # chat bubble pulsing bottom-right
    bx, by = w - 150, h - 40
    parts.append(f'<rect x="{bx}" y="{by}" width="126" height="28" rx="14" fill="#FFFFFF" stroke="{PLUM}" stroke-width="1.5"/>')
    parts.append(f'<path d="M{bx + 16} {by + 26} l-6 8 l12 -4 z" fill="#FFFFFF" stroke="{PLUM}" stroke-width="1.5" stroke-linejoin="round"/>')
    for d in range(3):
        cx = bx + 34 + d * 26
        anim = "" if STATIC else (
            f'<animate attributeName="opacity" values="0.25;1;0.25" dur="1.2s" begin="{d * 0.2:.1f}s" repeatCount="indefinite"/>'
        )
        parts.append(f'<circle cx="{cx}" cy="{by + 14}" r="4" fill="{PLUM}" opacity="0.25">{anim}</circle>')
    parts.append(
        f'<text x="24" y="{h - 16}" font-family="{MONO}" font-size="12" fill="{MUTED}">live feed · realtime messages</text>'
    )
    write("project-campustrade.svg", finish(parts, h))


def main():
    make_boot()
    make_about()
    make_tech()
    make_recon_thumb()
    make_campus_thumb()


if __name__ == "__main__":
    main()
