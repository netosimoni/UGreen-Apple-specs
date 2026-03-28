"""
Generate PWA icons and splash screens for Audio Modes app.
Design: Minimal dark icon with green/blue accent arcs (representing the two audio modes).
"""
from PIL import Image, ImageDraw
import math

def draw_icon(size, padding_pct=0.15, bg_color=(0, 0, 0), is_maskable=False):
    """Create a premium icon with headphone-inspired audio wave arcs."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    if is_maskable:
        # Maskable needs full bleed background
        draw.rectangle([0, 0, size, size], fill=bg_color)
        safe_zone = size * 0.8  # 80% safe zone
        offset = (size - safe_zone) / 2
    else:
        # Rounded rect background (simulated with circle corners)
        corner = int(size * 0.22)
        draw.rounded_rectangle([0, 0, size-1, size-1], radius=corner, fill=bg_color)
        offset = 0
        safe_zone = size

    cx = size // 2
    cy = size // 2

    green = (48, 209, 88)
    blue = (10, 132, 255)
    white = (255, 255, 255)

    lw = max(int(size * 0.028), 2)

    # Draw headphone-inspired arcs
    # Outer arc (green — UGREEN)
    r1 = int(safe_zone * 0.36)
    draw.arc([cx-r1, cy-r1-int(size*0.02), cx+r1, cy+r1-int(size*0.02)],
             start=210, end=330, fill=green, width=lw*3)

    # Middle arc (blended teal)
    r2 = int(safe_zone * 0.26)
    draw.arc([cx-r2, cy-r2-int(size*0.02), cx+r2, cy+r2-int(size*0.02)],
             start=210, end=330, fill=(40, 170, 200), width=lw*2)

    # Inner arc (blue — AirPods)
    r3 = int(safe_zone * 0.16)
    draw.arc([cx-r3, cy-r3-int(size*0.02), cx+r3, cy+r3-int(size*0.02)],
             start=210, end=330, fill=blue, width=lw*2)

    # Ear cups (circles at arc endpoints)
    cup_r = int(safe_zone * 0.065)
    angle_l = math.radians(210)
    angle_r = math.radians(330)

    # Left ear
    lx = cx + int(r1 * math.cos(angle_l))
    ly = cy - int(size*0.02) + int(r1 * math.sin(angle_l))
    draw.ellipse([lx-cup_r, ly-cup_r, lx+cup_r, ly+cup_r], fill=green)

    # Right ear
    rx = cx + int(r1 * math.cos(angle_r))
    ry = cy - int(size*0.02) + int(r1 * math.sin(angle_r))
    draw.ellipse([rx-cup_r, ry-cup_r, rx+cup_r, ry+cup_r], fill=blue)

    # Center indicator dot
    dot_r = max(int(size * 0.025), 2)
    draw.ellipse([cx-dot_r, cy-dot_r-int(size*0.02), cx+dot_r, cy+dot_r-int(size*0.02)], fill=white)

    # Bottom label dots
    dot_size = max(int(size * 0.022), 2)
    gap = int(size * 0.06)
    by = int(cy + safe_zone * 0.3)

    draw.ellipse([cx-gap-dot_size, by-dot_size, cx-gap+dot_size, by+dot_size], fill=green)
    draw.ellipse([cx+gap-dot_size, by-dot_size, cx+gap+dot_size, by+dot_size], fill=blue)

    return img


def draw_splash(width, height):
    """Create splash screen — simple dark bg with centered icon."""
    img = Image.new('RGB', (width, height), (0, 0, 0))
    icon = draw_icon(min(width, height) // 4, is_maskable=False)
    # Center the icon
    x = (width - icon.width) // 2
    y = (height - icon.height) // 2 - height // 20  # Slightly above center
    img.paste(icon, (x, y), icon)
    return img


base = '/home/user/workspace/audio-modes-v2/assets'

# Regular icons
for s in [192, 512]:
    icon = draw_icon(s, is_maskable=False)
    icon.save(f'{base}/icon-{s}.png', 'PNG')
    print(f'Created icon-{s}.png')

# Maskable icons (full bleed, 80% safe zone)
for s in [192, 512]:
    icon = draw_icon(s, is_maskable=True)
    icon.save(f'{base}/icon-maskable-{s}.png', 'PNG')
    print(f'Created icon-maskable-{s}.png')

# Apple touch icon (180x180)
icon180 = draw_icon(180, is_maskable=False)
icon180.save(f'{base}/apple-touch-icon.png', 'PNG')
print('Created apple-touch-icon.png')

# Favicon
icon32 = draw_icon(32, is_maskable=False)
icon32.save(f'{base}/favicon-32.png', 'PNG')
print('Created favicon-32.png')

# Splash screens for common iPhone sizes
splashes = [
    (1170, 2532),  # iPhone 13/14
    (1284, 2778),  # iPhone 13/14 Pro Max
    (1179, 2556),  # iPhone 14 Pro
    (1290, 2796),  # iPhone 14 Pro Max / 15 Pro Max
]

for w, h in splashes:
    splash = draw_splash(w, h)
    splash.save(f'{base}/splash-{w}x{h}.png', 'PNG', optimize=True)
    print(f'Created splash-{w}x{h}.png')

print('\nAll assets generated.')
