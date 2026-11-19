import os
from PIL import Image, ImageEnhance

src = r"C:\Users\frimo\Desktop\github-projects\GRANTON-ui\source-photo.jpg"
out = r"C:\Users\frimo\Desktop\github-projects\GRANTON-ui\granton-ascii.svg"

img = Image.open(src)
# Centered crop on Granton with hat, face, shoulders
crop = img.crop((40, 100, 727, 787))

# Optimize vibrance & facial brightness
im = ImageEnhance.Contrast(crop).enhance(1.15)
im = ImageEnhance.Color(im).enhance(1.22)
im = ImageEnhance.Brightness(im).enhance(1.08)
im = ImageEnhance.Sharpness(im).enhance(1.4)

COLS = 100
ROWS = 100
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()

CANVAS_W = 840
CANVAS_H = 880
TITLEBAR_H = 30
PAD_X = 20
ART_TOP = 38
CELL_SIZE = 8.0
ART_W = COLS * CELL_SIZE  # 800
ART_H = ROWS * CELL_SIZE  # 800

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"
CURSOR = "#39d353"

TOTAL_ANIM_DUR = 4.2
ROW_DUR = TOTAL_ANIM_DUR / ROWS

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)

parts.append('<defs>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
             f'fill="none" stroke="{FRAME}" stroke-width="1"/>')
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')

for i, dotcol in enumerate(['#ff5f56', '#ffbd2e', '#27c93f']):
    parts.append(f'<circle cx="{PAD_X + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">granton@github: ~$ ./portrait.sh</text>')

# Rows of dots
for ry in range(ROWS):
    row_y = ART_TOP + ry * CELL_SIZE
    cy = row_y + CELL_SIZE / 2.0
    delay = ry * ROW_DUR
    
    row_dots = []
    for rx in range(COLS):
        cx = PAD_X + rx * CELL_SIZE + CELL_SIZE / 2.0
        r, g, b = px[rx, ry][:3]
        lum = (0.299*r + 0.587*g + 0.114*b) / 255.0
        
        # Natural dot radius with good minimum presence
        rad = 1.3 + lum * 2.3
        color = f"#{r:02x}{g:02x}{b:02x}"
        row_dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="{color}"/>')

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD_X}" y="{row_y:.1f}" height="{CELL_SIZE}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{"".join(row_dots)}</g>')
    parts.append(
        f'<rect y="{row_y:.1f}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD_X}" to="{PAD_X+ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.9" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

# Footer
status_line_y = ART_TOP + ART_H + 4
status_y = status_line_y + 22
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(f'<text x="{PAD_X}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
             f'granton@github:~$ whoami <tspan fill="{INK}">Granton Mokua</tspan></text>')

status_chars = len('granton@github:~$ whoami Granton Mokua ')
parts.append(f'<rect x="{PAD_X + status_chars * 13 * 0.6:.1f}" y="{status_y-12:.1f}" width="8" height="14" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

parts.append('</svg>')
svg = "".join(parts)
with open(out, 'w', encoding='utf-8') as f:
    f.write(svg)

print(f"Generated {out} ({len(svg)/1024:.1f} KB; {CANVAS_W}x{CANVAS_H})")
