#!/usr/bin/env python3
"""Generate an animated GitHub contribution heatmap SVG in the KHUSHI.OS pastel theme.

Squares pop in one by one (CSS keyframes, plays on load, then holds). The card
has its own cream background so it reads the same on light and dark GitHub.
Respects prefers-reduced-motion. GitHub renders this SVG via <img>, where
CSS animations run but JavaScript does not.

Data source, in order:
  1. the public contributions API (third-party, no token needed)
  2. data/contributions.json (written by fetch_contributions.py) as a fallback

Usage: python scripts/generate_streak_svg.py [username] [output.svg]
"""
import datetime
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_PROFILE_USER", "Khushi-426")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "contrib-heatmap.svg")


def _levels_from_count(cnt):
    return 0 if cnt == 0 else (1 if cnt <= 3 else (2 if cnt <= 6 else (3 if cnt <= 12 else 4)))


def get_data(user):
    url = f"https://github-contributions-api.jogruber.de/v4/{user}?y=last"
    try:
        with urllib.request.urlopen(url, timeout=25) as r:
            return json.loads(r.read().decode())
    except Exception as e:  # network / third-party outage: fall back to local data
        fallback = os.path.join(HERE, "..", "data", "contributions.json")
        if not os.path.exists(fallback):
            raise
        print(f"API failed ({e}); using local {fallback}")
        raw = json.load(open(fallback, encoding="utf-8"))
        days = raw.get("days", [])
        contribs = [
            {"date": d["date"], "count": d.get("count", 0), "level": _levels_from_count(d.get("count", 0))}
            for d in days
        ]
        return {
            "contributions": contribs,
            "total": {"lastYear": raw.get("total_contributions", sum(c["count"] for c in contribs))},
            "_local": raw,
        }


data = get_data(USER)
contribs = data["contributions"]
total = data["total"]["lastYear"]
local = data.get("_local", {})
active_days = local.get("active_days", sum(1 for c in contribs if c["count"] > 0))
longest = local.get("longest_streak", {}).get("length")
current = local.get("current_streak", {}).get("length")

# ---- layout ---------------------------------------------------------------
CELL, GAP, RAD = 13, 3, 3
LEFT, TOP = 50, 46
CARD_PAD = 18

# KHUSHI.OS pastel ramp: empty -> strongest. Mint to lavender, reads on cream.
COLORS = ["#F1EAFB", "#D6F2E4", "#B2E6CE", "#84D2AE", "#4FB58E"]
FLASH = "#FFF0A8"           # butter flash on pop
CARD_BG = "#FFF9EE"
CARD_BORDER = "#DCCEFF"
INK = "#382F4A"
MUTED = "#786A91"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

n = len(contribs)
NW = (n + 6) // 7
GRID_W = NW * (CELL + GAP)
W = LEFT + GRID_W + CARD_PAD
H = TOP + 7 * (CELL + GAP) + 58

# timing (seconds)
REVEAL, DUR = 3.2, 0.55
maxorder = (NW - 1) + 6 * 0.55

labels = []
sd = datetime.date.fromisoformat(contribs[0]["date"])
last_m = None
for wk in range(NW):
    d = sd + datetime.timedelta(days=wk * 7)
    if d.month != last_m:
        last_m = d.month
        labels.append(f'<text class="lbl" x="{LEFT + wk * (CELL + GAP)}" y="{TOP - 12}">{MONTHS[d.month - 1]}</text>')
for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
    labels.append(f'<text class="lbl" x="{CARD_PAD - 2}" y="{TOP + r * (CELL + GAP) + CELL - 2}">{name}</text>')

rects = []
for i, c in enumerate(contribs):
    wk, row, lvl = i // 7, i % 7, c["level"]
    x = LEFT + wk * (CELL + GAP)
    y = TOP + row * (CELL + GAP)
    delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
    cls = "c g" if lvl >= 1 else "c e"
    rects.append(
        f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
        f'fill="{COLORS[lvl]}" style="animation-delay:{delay}s"/>'
    )

stats = [f"{total:,} contributions in the last year"]
if active_days:
    stats.append(f"{active_days} active days")
if longest is not None:
    stats.append(f"longest streak {longest} days")
footer = "  ·  ".join(stats)

legend_y = H - 16
legend = []
lx = W - CARD_PAD - (len(COLORS) * (CELL + 4)) - 60
legend.append(f'<text class="lbl" x="{lx - 40}" y="{legend_y + 9}">Less</text>')
for i, col in enumerate(COLORS):
    legend.append(
        f'<rect x="{lx + i * (CELL + 4)}" y="{legend_y - 4}" width="{CELL}" height="{CELL}" rx="{RAD}" fill="{col}"/>'
    )
legend.append(f'<text class="lbl" x="{lx + len(COLORS) * (CELL + 4) + 4}" y="{legend_y + 9}">More</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-rounded,'Trebuchet MS',Verdana,Helvetica,Arial,sans-serif" role="img" aria-label="Contribution graph for {USER}: {total} contributions in the last year">
<style>
  text.lbl {{ fill:{MUTED}; font-size:12px; font-weight:600; }}
  text.total {{ fill:{INK}; font-size:14px; font-weight:700; }}
  .c {{ transform-box:fill-box; transform-origin:center; animation:pop {DUR}s ease-out both; }}
  .g {{ animation:pop {DUR}s ease-out both, flash {DUR + 0.15}s ease-out both; }}
  @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.1)}} 100%{{opacity:1;transform:scale(1)}} }}
  @keyframes flash {{ 0%{{filter:brightness(1.35) saturate(1.6)}} 45%{{filter:brightness(1.35) saturate(1.6)}} 100%{{filter:none}} }}
  @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1.5"/>
{''.join(labels)}
{''.join(rects)}
<text class="total" x="{CARD_PAD}" y="{H - 16}">{footer}</text>
{''.join(legend)}
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Wrote {OUT}: {n} days, {total:,} contributions, {len(svg) // 1024} KB")
