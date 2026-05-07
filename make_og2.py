from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

FONTS = "/sessions/eloquent-quirky-bell/mnt/.claude/skills/canvas-design/canvas-fonts"
OUT   = "/sessions/eloquent-quirky-bell/mnt/outputs"

W, H = 1200, 630

NAVY   = (13, 30, 60)
NAVY2  = (8, 18, 42)
TEAL1  = (27, 186, 214)
TEAL2  = (154, 232, 248)
TEAL3  = (10, 100, 130)
TEAL4  = (18, 140, 175)
WHITE  = (255, 255, 255)
CREAM  = (232, 242, 248)

img = Image.new("RGB", (W, H), NAVY2)
draw = ImageDraw.Draw(img, "RGBA")

# ── BACKGROUND GRADIENT (top lighter, bottom darker) ──────
for y in range(H):
    t = y / H
    r = int(NAVY2[0] + (NAVY[0] - NAVY2[0]) * t + 6 * (1-t))
    g = int(NAVY2[1] + (NAVY[1] - NAVY2[1]) * t + 10 * (1-t))
    b = int(NAVY2[2] + (NAVY[2] - NAVY2[2]) * t + 22 * (1-t))
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── CONCENTRIC RIPPLES — origin at bottom-left of drop ────
cx, cy = 200, H + 20
rings  = 34

for i in range(rings, 0, -1):
    ratio = i / rings
    rx = int(90 + ratio * 920)
    ry = int(60 + ratio * 600)
    alpha = int(5 + (1 - ratio) ** 0.7 * 32)
    shift = ratio
    rc = int(TEAL3[0] + (TEAL4[0] - TEAL3[0]) * (1 - shift))
    gc = int(TEAL3[1] + (TEAL4[1] - TEAL3[1]) * (1 - shift))
    bc = int(TEAL3[2] + (TEAL4[2] - TEAL3[2]) * (1 - shift))
    draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=(rc, gc, bc, alpha), width=1)

# brighter accent rings every 5
for i in [30, 25, 20, 15, 10, 6, 3]:
    ratio = i / rings
    rx = int(90 + ratio * 920)
    ry = int(60 + ratio * 600)
    alpha = int(22 + (1 - ratio) * 45)
    draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=(*TEAL1, alpha), width=1)

# ── TRUE TEARDROP SHAPE ────────────────────────────────────
drop_cx, drop_cy = 238, 318
drop_rx = 122   # horizontal radius
drop_ry = 148   # vertical radius — taller than wide

def teardrop_pts(cx, cy, rx, ry, n=200):
    """True teardrop: circular bottom, pointed top via cardioid modifier."""
    pts = []
    for k in range(n):
        # θ goes from 0 (bottom) around full circle
        theta = 2 * math.pi * k / n - math.pi / 2   # start from bottom
        # base circle
        bx = cx + rx * math.cos(theta)
        by = cy + ry * math.sin(theta)
        # taper modifier: squeezes x as we approach the top (theta ≈ -π/2 i.e. top)
        # normalise: how close to top (sin(theta) = -1 at top)
        top_dist = (-math.sin(theta) + 1) / 2   # 0 at bottom, 1 at top
        taper = 1 - 0.92 * top_dist ** 2.4      # squeeze x near top
        pts.append((cx + (bx - cx) * taper, by))
    return pts

tdrop = teardrop_pts(drop_cx, drop_cy, drop_rx, drop_ry)

# glow halo
for gr in range(220, 0, -5):
    scale = gr / 220
    a_g = int(4 * (1 - scale) ** 1.5)
    pts_g = teardrop_pts(drop_cx, drop_cy,
                         int(drop_rx * (1 + 0.55 * scale)),
                         int(drop_ry * (1 + 0.45 * scale)))
    draw.polygon(pts_g, fill=(*TEAL3, a_g))

# main body: layered gradient ellipses clipped inside teardrop shape via mask
mask = Image.new("L", (W, H), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.polygon(tdrop, fill=255)

body = Image.new("RGBA", (W, H), (0,0,0,0))
body_draw = ImageDraw.Draw(body)

steps = 48
for s in range(steps):
    t = s / steps
    scale = 1 - t * 0.88
    off_x = -int(20 * t)
    off_y = -int(28 * t)
    pts_s = teardrop_pts(drop_cx + off_x, drop_cy + off_y,
                         drop_rx * scale, drop_ry * scale)
    rc = int(TEAL3[0] + (TEAL1[0] - TEAL3[0]) * t)
    gc = int(TEAL3[1] + (TEAL1[1] - TEAL3[1]) * t)
    bc = int(TEAL3[2] + (TEAL1[2] - TEAL3[2]) * t)
    body_draw.polygon(pts_s, fill=(rc, gc, bc, 215))

img_rgba = img.convert("RGBA")
img_rgba.paste(body, mask=body)
img = img_rgba.convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# thin outline around teardrop
draw.polygon(tdrop, outline=(*TEAL1, 50))

# inner highlight (small bright ellipse upper-left of center)
hi_cx = drop_cx - 38
hi_cy = drop_cy - 52
draw.ellipse([hi_cx-26, hi_cy-14, hi_cx+26, hi_cy+14], fill=(*TEAL2, 85))
draw.ellipse([hi_cx-14, hi_cy-7, hi_cx+14, hi_cy+7], fill=(*WHITE, 40))

# ── VERTICAL ACCENT LINE ──────────────────────────────────
vline_x = 436
draw.line([(vline_x, 220), (vline_x, 440)], fill=(*TEAL3, 100), width=1)

# ── TYPOGRAPHY ────────────────────────────────────────────
def load(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS, name), size)
    except:
        return ImageFont.load_default()

f_instituto = load("WorkSans-Regular.ttf",  11)
f_somos     = load("Gloock-Regular.ttf",    92)
f_agua      = load("Gloock-Regular.ttf",    92)
f_tagline   = load("WorkSans-Regular.ttf",  17)
f_location  = load("WorkSans-Regular.ttf",  13)

tx = 462
ty_inst = 228
ty_main = 268
ty_tag  = 410
ty_loc  = 444

# "I N S T I T U T O" — spaced label
draw.text((tx, ty_inst), "I N S T I T U T O", font=f_instituto, fill=(*TEAL1, 170))

# "Somos " in cream
somos_str = "Somos "
agua_str  = "Água"
# slight shadow
draw.text((tx+2, ty_main+2), somos_str + agua_str, font=f_somos, fill=(0, 8, 20, 100))
# cream "Somos "
draw.text((tx, ty_main), somos_str, font=f_somos, fill=(*CREAM, 250))
sw = int(f_somos.getlength(somos_str))
# teal "Água"
draw.text((tx + sw, ty_main), agua_str, font=f_agua, fill=(*TEAL2, 245))

# rule
draw.line([(tx, ty_tag - 8), (1150, ty_tag - 8)], fill=(*TEAL3, 55), width=1)

# tagline
draw.text((tx, ty_tag), "Certificação participativa de cuidado das Águas",
          font=f_tagline, fill=(*CREAM, 155))

# location
draw.text((tx, ty_loc + 10), "Ecovila Piracanga  ·  Sul da Bahia  ·  Brasil",
          font=f_location, fill=(*TEAL1, 120))

# ── CORNER WATERMARK (tiny drop icon top right) ───────────
ic_x, ic_y = 1152, 62
for r_ic in [22, 15, 9]:
    a_ic = {22: 25, 15: 40, 9: 60}[r_ic]
    draw.ellipse([ic_x-r_ic, ic_y-r_ic, ic_x+r_ic, ic_y+r_ic],
                 fill=(*TEAL1, a_ic))
draw.ellipse([ic_x-4, ic_y-9, ic_x+4, ic_y-1], fill=(*TEAL2, 70))

# ── VIGNETTE ─────────────────────────────────────────────
vig = Image.new("RGBA", (W, H), (0,0,0,0))
vd  = ImageDraw.Draw(vig)
steps_v = 160
for s in range(steps_v, 0, -2):
    a_v = int(55 * ((1 - s/steps_v) ** 1.6))
    vd.rectangle([s, s, W-s, H-s], outline=(0, 0, 0, a_v))

final = img.convert("RGBA")
final.alpha_composite(vig)
img = final.convert("RGB")

out_path = os.path.join(OUT, "og-image.png")
img.save(out_path, "PNG", optimize=True, quality=95)
print(f"✓ {out_path}  {W}×{H}px")
