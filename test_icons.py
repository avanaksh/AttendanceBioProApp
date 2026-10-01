import math
from PIL import Image, ImageDraw, ImageFilter

def create_app_icon_512():
    size = 512
    canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    padding = 32
    badge_size = size - padding * 2 # 448
    radius = 100
    cx, cy = size // 2, size // 2
    
    # 1. Drop shadow onto transparent canvas
    shadow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle(
        [padding, padding + 16, padding + badge_size, padding + badge_size + 16],
        radius=radius,
        fill=(0, 0, 0, 180)
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas, shadow_layer)
    
    # 2. Main badge layer
    badge_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Gradient base inside squircle
    mask = Image.new('L', (size, size), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle(
        [padding, padding, padding + badge_size, padding + badge_size],
        radius=radius,
        fill=255
    )
    
    # Gradient canvas
    grad = Image.new('RGBA', (size, size))
    g_draw = ImageDraw.Draw(grad)
    c1 = (11, 17, 32, 255) # deep slate/black
    c2 = (30, 27, 75, 255) # royal indigo
    for y in range(size):
        ratio = y / float(size)
        cr = int(c1[0] + (c2[0] - c1[0]) * ratio)
        cg = int(c1[1] + (c2[1] - c1[1]) * ratio)
        cb = int(c1[2] + (c2[2] - c1[2]) * ratio)
        g_draw.line([(0, y), (size, y)], fill=(cr, cg, cb, 255))
        
    badge_layer.paste(grad, (0, 0), mask)
    canvas = Image.alpha_composite(canvas, badge_layer)
    
    # 3. Ambient inner radial glow
    glow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gl_draw = ImageDraw.Draw(glow_layer)
    for s in range(35, 0, -1):
        rad = int(190 * (s / 35.0))
        alpha = int(110 * (1.0 - (s / 35.0) ** 1.5))
        gl_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(6, 182, 212, alpha))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(14))
    
    glow_masked = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_masked.paste(glow_layer, (0, 0), mask)
    canvas = Image.alpha_composite(canvas, glow_masked)
    
    # 4. Biometric rings & graphics layer
    gfx_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(gfx_layer)
    
    # Outer squircle border
    d.rounded_rectangle(
        [padding, padding, padding + badge_size, padding + badge_size],
        radius=radius,
        outline=(56, 189, 248, 220),
        width=3
    )
    d.rounded_rectangle(
        [padding + 3, padding + 3, padding + badge_size - 3, padding + badge_size - 3],
        radius=radius - 2,
        outline=(99, 102, 241, 140),
        width=2
    )
    
    # Biometric Concentric Rings
    r_out = 148
    d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], outline=(6, 182, 212, 180), width=4)
    
    r_mid = 110
    d.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=(99, 102, 241, 200), width=3)
    
    # Reticle ticks on outer ring
    for angle_deg in range(0, 360, 30):
        ang = math.radians(angle_deg)
        x1 = cx + int((r_out - 9) * math.cos(ang))
        y1 = cy + int((r_out - 9) * math.sin(ang))
        x2 = cx + int((r_out + 9) * math.cos(ang))
        y2 = cy + int((r_out + 9) * math.sin(ang))
        d.line([(x1, y1), (x2, y2)], fill=(56, 189, 248, 240), width=3)
        
    # Shield emblem in center
    s_w = 116
    s_h = 142
    top = cy - s_h // 2
    bot = cy + s_h // 2
    l = cx - s_w // 2
    r = cx + s_w // 2
    shield_pts = [
        (cx, top),
        (r, top + int(s_h * 0.22)),
        (r - 10, cy + int(s_h * 0.18)),
        (cx, bot),
        (l + 10, cy + int(s_h * 0.18)),
        (l, top + int(s_h * 0.22))
    ]
    # Shield fill
    d.polygon(shield_pts, fill=(16, 185, 129, 240), outline=(52, 211, 153, 255))
    
    # Crisp white checkmark
    chk_pts = [
        (cx - 32, cy - 2),
        (cx - 10, cy + 24),
        (cx + 34, cy - 24)
    ]
    d.line([(chk_pts[0][0], chk_pts[0][1]), (chk_pts[1][0], chk_pts[1][1])], fill=(255, 255, 255, 255), width=9)
    d.line([(chk_pts[1][0], chk_pts[1][1]), (chk_pts[2][0], chk_pts[2][1])], fill=(255, 255, 255, 255), width=9)
    d.ellipse([chk_pts[0][0]-4, chk_pts[0][1]-4, chk_pts[0][0]+4, chk_pts[0][1]+4], fill=(255, 255, 255, 255))
    d.ellipse([chk_pts[1][0]-4, chk_pts[1][1]-4, chk_pts[1][0]+4, chk_pts[1][1]+4], fill=(255, 255, 255, 255))
    d.ellipse([chk_pts[2][0]-4, chk_pts[2][1]-4, chk_pts[2][0]+4, chk_pts[2][1]+4], fill=(255, 255, 255, 255))
    
    # 5. Diagonal glass reflection
    refl_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    rf_draw = ImageDraw.Draw(refl_layer)
    refl_pts = [
        (padding, padding),
        (padding + badge_size, padding),
        (padding + badge_size, padding + int(badge_size * 0.35)),
        (padding, padding + int(badge_size * 0.55))
    ]
    rf_draw.polygon(refl_pts, fill=(255, 255, 255, 24))
    
    refl_masked = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    refl_masked.paste(refl_layer, (0, 0), mask)
    
    canvas = Image.alpha_composite(canvas, gfx_layer)
    canvas = Image.alpha_composite(canvas, refl_masked)
    
    return canvas

icon_512 = create_app_icon_512()
icon_512.save("test_icon_512.png", "PNG")

icon_114 = icon_512.resize((114, 114), Image.Resampling.LANCZOS)
icon_114.save("test_icon_114.png", "PNG")
print("Icons generated successfully!")
