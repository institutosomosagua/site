from PIL import Image, ImageDraw, ImageFont
import math, os

FONTS = "/sessions/eloquent-quirky-bell/mnt/.claude/skills/canvas-design/canvas-fonts"
OUT   = "/sessions/eloquent-quirky-bell/mnt/outputs"

W, H = 1200, 630

# ── PALETTE ──────────────────────────────────────────────
NAVY   = (13, 30, 60)        # #0d1e3c
TEAL1  = (27, 186, 214)      # #1BBAD6
TEAL2  = (154, 232, 248)     # #9AE8F8
TEAL3  = (10, 122, 150)      # #0A7A96
WHITE  = (255, 255, 255)
CREAM  = (235, 242, 246)

img = Image.new("RGB", (W, H), NAVY)
draw = ImageDraw.Draw(img, "RGBA")

# ── SUBTLE GRADIENT WASH (navy → slightly lighter navy at top) ──
for y in range(H):
    t = y / H
    r = int(13 + 8 * (1 - t))
    g = int(30 + 12 * (1 - t))
    b = int(60 + 25 * (1 - t))
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── CONCENTRIC RIPPLE RINGS from lower-left origin ──────
cx, cy = 210, H + 60   # origin below and left
rings = 28
for i in range(rings, 0, -1):
    ratio = i / rings
    rx = int(120 + ratio * 860)
    ry = int(80  + ratio * 560)
    alpha = int(6 + (1 - ratio) * 28)
    # color shifts from deep teal to lighter as rings expand
    teal_shift = ratio
    rc = int(TEAL3[0] + (TEAL1[0] - TEAL3[0]) * (1 - teal_shift))
    gc = int(TEAL3[1] + (TEAL1[1] - TEAL3[1]) * (1 - teal_shift))
    bc = int(TEAL3[2] + (TEAL1[2] - TEAL3[2]) * (1 - teal_shift))
    bbox = [cx - rx, cy - ry, cx + rx, cy + ry]
    draw.ellipse(bbox, outline=(rc, gc, bc, alpha), width=1)

# slightly thicker, brighter every 4th ring
for i in range(rings, 0, -4):
    ratio = i / rings
    rx = int(120 + ratio * 860)
    ry = int(80  + ratio * 560)
    alpha = int(18 + (1 - ratio) * 38)
    bbox = [cx - rx, cy - ry, cx + rx, cy + ry]
    draw.ellipse(bbox, outline=(*TEAL1, alpha), width=2)

# ── WATER-DROP SHAPE (left focal mass) ──────────────────
# Teardrop: circle bottom, pointed top
drop_cx, drop_cy = 260, 320
drop_r = 130

# soft glow behind drop
for g_r in range(200, 0, -4):
    a_glow = int(3 * (1 - g_r / 200))
    draw.ellipse(
        [drop_cx - g_r, drop_cy - g_r, drop_cx + g_r, drop_cy + g_r],
        fill=(*TEAL3, a_glow)
    )

# main drop body using polygon (teardrop)
n = 120
points = []
for k in range(n):
    ang = 2 * math.pi * k / n - math.pi / 2
    # squash upward to form teardrop
    squeeze = 1.0 + 0.55 * math.sin(ang + math.pi / 2) ** 2 if math.sin(ang) > 0 else 1.0
    r = drop_r / squeeze
    px = drop_cx + r * math.cos(ang)
    py = drop_cy + r * 1.12 * math.sin(ang)
    points.append((px, py))

# gradient fill via layered ellipses
for layer in range(40):
    t = layer / 40
    lr = int(drop_r * (1 - t * 0.85))
    off_x = int(-18 * t)
    off_y = int(-22 * t)
    rc = int(TEAL3[0] + (TEAL1[0] - TEAL3[0]) * t)
    gc = int(TEAL3[1] + (TEAL1[1] - TEAL3[1]) * t)
    bc_col = int(TEAL3[2] + (TEAL1[2] - TEAL3[2]) * t)
    draw.ellipse(
        [drop_cx + off_x - lr, drop_cy + off_y - int(lr*1.12),
         drop_cx + off_x + lr, drop_cy + off_y + int(lr*1.12)],
        fill=(rc, gc, bc_col, 210)
    )

# inner highlight
draw.ellipse(
    [drop_cx - 44, drop_cy - 68, drop_cx - 8, drop_cy - 20],
    fill=(*TEAL2, 95)
)
draw.ellipse(
    [drop_cx - 32, drop_cy - 56, drop_cx - 16, drop_cy - 36],
    fill=(*WHITE, 55)
)

# thin ring around drop
draw.ellipse(
    [drop_cx - drop_r - 2, drop_cy - int(drop_r * 1.12) - 2,
     drop_cx + drop_r + 2, drop_cy + int(drop_r * 1.12) + 2],
    outline=(*TEAL1, 55), width=1
)

# ── HORIZONTAL RULE ───────────────────────────────────────
rule_x1, rule_x2, rule_y = 470, 1140, 285
draw.line([(rule_x1, rule_y), (rule_x2, rule_y)], fill=(*TEAL3, 90), width=1)

# ── TYPOGRAPHY ────────────────────────────────────────────
def load(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONTS, name), size)
    except:
        return ImageFont.load_default()

font_serif_lg  = load("Gloock-Regular.ttf",         94)
font_serif_it  = load("CrimsonPro-Italic.ttf",       94)
font_label     = load("WorkSans-Regular.ttf",         13)
font_sub       = load("WorkSans-Regular.ttf",         18)
font_location  = load("WorkSans-Regular.ttf",         14)

# "INSTITUTO"  — small all-caps label
instituto_txt = "I N S T I T U T O"
draw.text((472, 248), instituto_txt, font=font_label,
          fill=(*TEAL1, 180))

# "Somos Água" — large serif, two-color: Somos (white) Água (teal)
# measure "Somos " width
somos_txt  = "Somos "
agua_txt   = "Água"

x_text = 468
y_text = 288

# shadow pass
draw.text((x_text + 2, y_text + 2), somos_txt + agua_txt,
          font=font_serif_lg, fill=(*NAVY, 120))

# white "Somos "
draw.text((x_text, y_text), somos_txt, font=font_serif_lg, fill=CREAM)

# measure somos width to position Água
somos_w = font_serif_lg.getlength(somos_txt)
draw.text((x_text + somos_w, y_text), agua_txt, font=font_serif_lg,
          fill=(*TEAL2, 240))

# ── DIVIDER LINE ──────────────────────────────────────────
draw.line([(472, 415), (1140, 415)], fill=(*TEAL3, 60), width=1)

# "tagline"
tagline = "Certificação participativa de cuidado das Águas"
draw.text((472, 430), tagline, font=font_sub, fill=(*CREAM, 160))

# location
location = "Ecovila Piracanga  ·  Sul da Bahia  ·  Brasil"
draw.text((472, 468), location, font=font_location, fill=(*TEAL1, 130))

# ── SMALL WATER-DROP ICON (top-right corner accent) ───────
ic_x, ic_y, ic_r = 1128, 72, 14
draw.ellipse([ic_x - ic_r, ic_y - ic_r, ic_x + ic_r, ic_y + ic_r],
             fill=(*TEAL1, 60))
draw.ellipse([ic_x - 5, ic_y - 10, ic_x + 5, ic_y],
             fill=(*TEAL2, 70))

# ── SUBTLE VIGNETTE ────────────────────────────────────────
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd  = ImageDraw.Draw(vig)
for s in range(180, 0, -3):
    a = int(48 * (1 - s / 180) ** 1.8)
    vd.rectangle([s, s, W - s, H - s], outline=(0, 0, 0, a))
img_rgba = img.convert("RGBA")
img_rgba.alpha_composite(vig)
img = img_rgba.convert("RGB")

# ── SAVE ──────────────────────────────────────────────────
out_path = os.path.join(OUT, "og-image.png")
img.save(out_path, "PNG", optimize=True)
print(f"Saved → {out_path}  ({W}×{H}px)")
