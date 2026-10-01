import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Directories
INPUT_DIR = r"C:\Users\HP\Desktop\atenapp"
DESKTOP_OUTPUT_DIR = r"C:\Users\HP\Desktop\atenapp"
PROJECT_OUTPUT_DIR = r"F:\AttendanceApp_revenueCat\store_assets"

os.makedirs(DESKTOP_OUTPUT_DIR, exist_ok=True)
os.makedirs(PROJECT_OUTPUT_DIR, exist_ok=True)

# System fonts
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\segoeui.ttf"
FONT_LIGHT_PATH = r"C:\Windows\Fonts\segoeuisl.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_gradient_canvas(width, height, top_color, bottom_color, horizontal=False):
    base = Image.new('RGB', (width, height), top_color)
    top_r, top_g, top_b = top_color
    bot_r, bot_g, bot_b = bottom_color
    
    draw = ImageDraw.Draw(base)
    steps = width if horizontal else height
    for i in range(steps):
        ratio = i / float(steps)
        r = int(top_r + (bot_r - top_r) * ratio)
        g = int(top_g + (bot_g - top_g) * ratio)
        b = int(top_b + (bot_b - top_b) * ratio)
        if horizontal:
            draw.line([(i, 0), (i, height)], fill=(r, g, b))
        else:
            draw.line([(0, i), (width, i)], fill=(r, g, b))
    return base

def draw_radial_glow(canvas, center_x, center_y, radius, color, max_alpha=120):
    glow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    r_val, g_val, b_val = color
    steps = 40
    for s in range(steps, 0, -1):
        cur_radius = int(radius * (s / steps))
        alpha = int(max_alpha * (1.0 - (s / steps) ** 1.6))
        glow_draw.ellipse(
            [center_x - cur_radius, center_y - cur_radius, center_x + cur_radius, center_y + cur_radius],
            fill=(r_val, g_val, b_val, alpha)
        )
    glow = glow.filter(ImageFilter.GaussianBlur(max(2, radius // 12)))
    canvas.paste(glow, (0, 0), glow)

def draw_tech_grid(canvas, grid_size=48, line_color=(30, 41, 59, 40)):
    w, h = canvas.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for x in range(0, w, grid_size):
        draw.line([(x, 0), (x, h)], fill=line_color, width=1)
    for y in range(0, h, grid_size):
        draw.line([(0, y), (w, y)], fill=line_color, width=1)
        
    canvas.paste(overlay, (0, 0), overlay)

def draw_circuit_lines(canvas, w, h, base_color=(6, 182, 212, 35)):
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    r, g, b, a = base_color
    nodes = [
        [(w - 650, 160), (w - 480, 160), (w - 400, 240), (w - 180, 240)],
        [(w - 750, 480), (w - 580, 480), (w - 500, 400), (w - 280, 400)],
        [(w - 820, 780), (w - 640, 780), (w - 550, 900), (w - 320, 900)],
        [(w - 520, 1020), (w - 380, 1020), (w - 280, 1120)]
    ]
    for path in nodes:
        for i in range(len(path) - 1):
            draw.line([path[i], path[i+1]], fill=(r, g, b, a), width=2)
        draw.ellipse([path[-1][0]-5, path[-1][1]-5, path[-1][0]+5, path[-1][1]+5], fill=(r, g, b, int(a*1.5)))
        draw.ellipse([path[0][0]-4, path[0][1]-4, path[0][0]+4, path[0][1]+4], fill=(r, g, b, int(a*1.5)))
        
    canvas.paste(overlay, (0, 0), overlay)

def draw_biometric_rings(canvas, center_x, center_y, base_color=(14, 165, 233, 40)):
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    r_val, g_val, b_val, a = base_color
    
    radii = [90, 180, 290, 420, 560]
    for rad in radii:
        draw.ellipse([center_x - rad, center_y - rad, center_x + rad, center_y + rad],
                     outline=(r_val, g_val, b_val, a), width=2)
    
    for angle_deg in range(0, 360, 30):
        ang = math.radians(angle_deg)
        x1 = center_x + int(280 * math.cos(ang))
        y1 = center_y + int(280 * math.sin(ang))
        x2 = center_x + int(300 * math.cos(ang))
        y2 = center_y + int(300 * math.sin(ang))
        draw.line([(x1, y1), (x2, y2)], fill=(r_val, g_val, b_val, int(a * 1.4)), width=2)
        
    canvas.paste(overlay, (0, 0), overlay)

def draw_vector_icon(draw, cx, cy, size, icon_type, color=(6, 182, 212), bg_color=(15, 23, 42)):
    r = size // 2
    draw.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=r//3, fill=bg_color, outline=color, width=1)
    ir = int(r * 0.55)
    
    if icon_type == 'check':
        draw.line([(cx - ir*0.6, cy), (cx - ir*0.1, cy + ir*0.5), (cx + ir*0.7, cy - ir*0.5)], fill=color, width=3)
    elif icon_type == 'eye':
        draw.ellipse([cx - ir, cy - int(ir*0.6), cx + ir, cy + int(ir*0.6)], outline=color, width=2)
        draw.ellipse([cx - int(ir*0.35), cy - int(ir*0.35), cx + int(ir*0.35), cy + int(ir*0.35)], fill=color)
    elif icon_type == 'clock':
        draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=color, width=2)
        draw.line([(cx, cy), (cx, cy - int(ir*0.6))], fill=color, width=2)
        draw.line([(cx, cy), (cx + int(ir*0.5), cy)], fill=color, width=2)
    elif icon_type == 'chart':
        w = int(ir * 0.4)
        draw.rectangle([cx - int(ir*0.9), cy + int(ir*0.1), cx - int(ir*0.9) + w, cy + ir], fill=color)
        draw.rectangle([cx - int(ir*0.2), cy - int(ir*0.4), cx - int(ir*0.2) + w, cy + ir], fill=color)
        draw.rectangle([cx + int(ir*0.5), cy - int(ir*0.9), cx + int(ir*0.5) + w, cy + ir], fill=color)
    elif icon_type == 'crown':
        pts = [
            (cx - ir, cy + ir*0.6),
            (cx - ir, cy - ir*0.4),
            (cx - int(ir*0.5), cy),
            (cx, cy - int(ir*0.8)),
            (cx + int(ir*0.5), cy),
            (cx + ir, cy - ir*0.4),
            (cx + ir, cy + ir*0.6)
        ]
        draw.polygon(pts, fill=color)
    elif icon_type == 'cloud':
        draw.ellipse([cx - int(ir*0.7), cy - int(ir*0.3), cx, cy + int(ir*0.5)], fill=color)
        draw.ellipse([cx - int(ir*0.3), cy - int(ir*0.7), cx + int(ir*0.5), cy + int(ir*0.4)], fill=color)
        draw.ellipse([cx + int(ir*0.1), cy - int(ir*0.2), cx + int(ir*0.8), cy + int(ir*0.5)], fill=color)
        draw.rectangle([cx - int(ir*0.5), cy, cx + int(ir*0.5), cy + int(ir*0.5)], fill=color)
    elif icon_type == 'shield':
        pts = [
            (cx, cy - ir),
            (cx + ir, cy - int(ir*0.5)),
            (cx + int(ir*0.8), cy + int(ir*0.3)),
            (cx, cy + ir),
            (cx - int(ir*0.8), cy + int(ir*0.3)),
            (cx - ir, cy - int(ir*0.5))
        ]
        draw.polygon(pts, outline=color, fill=bg_color, width=2)
        draw.line([(cx - ir*0.3, cy), (cx - ir*0.05, cy + ir*0.3), (cx + ir*0.4, cy - ir*0.3)], fill=color, width=2)
    elif icon_type == 'star':
        draw.ellipse([cx - int(ir*0.5), cy - int(ir*0.5), cx + int(ir*0.5), cy + int(ir*0.5)], fill=color)
    elif icon_type == 'location':
        draw.ellipse([cx - int(ir*0.6), cy - ir, cx + int(ir*0.6), cy + int(ir*0.2)], outline=color, width=2)
        draw.ellipse([cx - int(ir*0.25), cy - int(ir*0.6), cx + int(ir*0.25), cy - int(ir*0.1)], fill=color)
        pts = [(cx - int(ir*0.5), cy - int(ir*0.1)), (cx + int(ir*0.5), cy - int(ir*0.1)), (cx, cy + ir)]
        draw.polygon(pts, fill=color)

def trim_light_border(im):
    im = im.convert('RGBA')
    w, h = im.size
    
    def is_light(pixel):
        return pixel[0] > 180 and pixel[1] > 180 and pixel[2] > 180

    top = 0
    for y in range(min(50, h)):
        p = im.getpixel((w//2, y))
        if not is_light(p):
            top = y
            break

    bottom = h
    for y in range(h-1, max(h-50, 0), -1):
        p = im.getpixel((w//2, y))
        if not is_light(p):
            bottom = y + 1
            break

    left = 0
    for x in range(min(50, w)):
        p = im.getpixel((x, h//2))
        if not is_light(p):
            left = x
            break

    right = w
    for x in range(w-1, max(w-50, 0), -1):
        p = im.getpixel((x, h//2))
        if not is_light(p):
            right = x + 1
            break

    if right > left + 100 and bottom > top + 100:
        return im.crop((left, top, right, bottom))
    return im

def create_device_mockup(screen_img, target_h=960, corner_radius=36, border_width=12):
    screen_img = trim_light_border(screen_img)
    orig_w, orig_h = screen_img.size
    aspect = orig_w / float(orig_h)
    
    screen_h = target_h
    screen_w = int(target_h * aspect)
    
    resized_screen = screen_img.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
    
    outer_w = screen_w + border_width * 2
    outer_h = screen_h + border_width * 2
    
    screen_mask = Image.new('L', (screen_w, screen_h), 0)
    mask_draw = ImageDraw.Draw(screen_mask)
    mask_draw.rounded_rectangle([0, 0, screen_w, screen_h], radius=corner_radius - 8, fill=255)
    
    curved_screen = Image.new('RGBA', (screen_w, screen_h), (0, 0, 0, 0))
    curved_screen.paste(resized_screen.convert('RGBA'), (0, 0), screen_mask)
    
    frame = Image.new('RGBA', (outer_w, outer_h), (0, 0, 0, 0))
    frame_draw = ImageDraw.Draw(frame)
    
    frame_draw.rounded_rectangle(
        [0, 0, outer_w, outer_h],
        radius=corner_radius,
        fill=(15, 23, 42, 255),
        outline=(51, 65, 85, 255),
        width=2
    )
    
    frame.paste(curved_screen, (border_width, border_width), curved_screen)
    
    slit_w = int(screen_w * 0.22)
    slit_h = 4
    slit_x = (outer_w - slit_w) // 2
    slit_y = max(3, border_width // 2 - 2)
    frame_draw.rounded_rectangle(
        [slit_x, slit_y, slit_x + slit_w, slit_y + slit_h],
        radius=2,
        fill=(5, 8, 15, 240)
    )
    
    shadow_margin = 60
    total_w = outer_w + shadow_margin * 2
    total_h = outer_h + shadow_margin * 2
    
    canvas_with_shadow = Image.new('RGBA', (total_w, total_h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(canvas_with_shadow)
    
    shadow_draw.rounded_rectangle(
        [shadow_margin, shadow_margin + 16, shadow_margin + outer_w, shadow_margin + outer_h + 16],
        radius=corner_radius,
        fill=(0, 0, 0, 180)
    )
    canvas_with_shadow = canvas_with_shadow.filter(ImageFilter.GaussianBlur(30))
    
    sharp_shadow = Image.new('RGBA', (total_w, total_h), (0, 0, 0, 0))
    ss_draw = ImageDraw.Draw(sharp_shadow)
    ss_draw.rounded_rectangle(
        [shadow_margin + 4, shadow_margin + 6, shadow_margin + outer_w + 4, shadow_margin + outer_h + 6],
        radius=corner_radius,
        fill=(0, 0, 0, 110)
    )
    sharp_shadow = sharp_shadow.filter(ImageFilter.GaussianBlur(12))
    
    canvas_with_shadow.paste(sharp_shadow, (0, 0), sharp_shadow)
    canvas_with_shadow.paste(frame, (shadow_margin, shadow_margin), frame)
    
    return canvas_with_shadow

def save_image_multi(img, base_name, resize_dims=None):
    """Saves PNG and JPG in both output folders. Optionally resizes."""
    rgb_img = img.convert('RGB')
    
    targets = [(rgb_img, base_name)]
    if resize_dims:
        for rw, rh, rname in resize_dims:
            r_img = rgb_img.resize((rw, rh), Image.Resampling.LANCZOS)
            targets.append((r_img, rname))
            
    for cur_img, name in targets:
        for d in [DESKTOP_OUTPUT_DIR, PROJECT_OUTPUT_DIR]:
            png_path = os.path.join(d, f"{name}.png")
            jpg_path = os.path.join(d, f"{name}.jpg")
            cur_img.save(png_path, "PNG", optimize=True)
            cur_img.save(jpg_path, "JPEG", quality=95, optimize=True)
            print(f"Saved: {png_path} ({cur_img.size[0]}x{cur_img.size[1]})")

# Load source screenshots
img_pro = Image.open(os.path.join(INPUT_DIR, "1.png"))
img_login = Image.open(os.path.join(INPUT_DIR, "2.png"))
img_user = Image.open(os.path.join(INPUT_DIR, "3.png"))
img_admin_portal = Image.open(os.path.join(INPUT_DIR, "2_admin.png"))
img_admin_home = Image.open(os.path.join(INPUT_DIR, "1_admin.png"))

# =========================================================================
# 1. APP ICONS WITH TRANSPARENCY: 512 x 512 and 114 x 114
# =========================================================================
def generate_app_icons():
    print("\n--- Generating App Icons (512x512 and 114x114 with transparency) ---")
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
    mask = Image.new('L', (size, size), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle(
        [padding, padding, padding + badge_size, padding + badge_size],
        radius=radius,
        fill=255
    )
    
    grad = Image.new('RGBA', (size, size))
    g_draw = ImageDraw.Draw(grad)
    c1 = (11, 17, 32, 255)
    c2 = (30, 27, 75, 255)
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
    
    # 4. Biometric rings and graphics layer
    gfx_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(gfx_layer)
    
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
    
    r_out = 148
    d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], outline=(6, 182, 212, 180), width=4)
    
    r_mid = 110
    d.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], outline=(99, 102, 241, 200), width=3)
    
    for angle_deg in range(0, 360, 30):
        ang = math.radians(angle_deg)
        x1 = cx + int((r_out - 9) * math.cos(ang))
        y1 = cy + int((r_out - 9) * math.sin(ang))
        x2 = cx + int((r_out + 9) * math.cos(ang))
        y2 = cy + int((r_out + 9) * math.sin(ang))
        d.line([(x1, y1), (x2, y2)], fill=(56, 189, 248, 240), width=3)
        
    s_w, s_h = 116, 142
    top, bot = cy - s_h // 2, cy + s_h // 2
    l, r = cx - s_w // 2, cx + s_w // 2
    shield_pts = [
        (cx, top),
        (r, top + int(s_h * 0.22)),
        (r - 10, cy + int(s_h * 0.18)),
        (cx, bot),
        (l + 10, cy + int(s_h * 0.18)),
        (l, top + int(s_h * 0.22))
    ]
    d.polygon(shield_pts, fill=(16, 185, 129, 240), outline=(52, 211, 153, 255))
    
    chk_pts = [(cx - 32, cy - 2), (cx - 10, cy + 24), (cx + 34, cy - 24)]
    d.line([(chk_pts[0][0], chk_pts[0][1]), (chk_pts[1][0], chk_pts[1][1])], fill=(255, 255, 255, 255), width=9)
    d.line([(chk_pts[1][0], chk_pts[1][1]), (chk_pts[2][0], chk_pts[2][1])], fill=(255, 255, 255, 255), width=9)
    for pt in chk_pts:
        d.ellipse([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=(255, 255, 255, 255))
    
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
    
    # Save 512x512
    for d_path in [DESKTOP_OUTPUT_DIR, PROJECT_OUTPUT_DIR]:
        p512 = os.path.join(d_path, "icon_512x512.png")
        canvas.save(p512, "PNG")
        print(f"Saved: {p512} (512x512 PNG with transparency)")
        
    # Resize and save 114x114
    icon_114 = canvas.resize((114, 114), Image.Resampling.LANCZOS)
    for d_path in [DESKTOP_OUTPUT_DIR, PROJECT_OUTPUT_DIR]:
        p114 = os.path.join(d_path, "icon_114x114.png")
        icon_114.save(p114, "PNG")
        print(f"Saved: {p114} (114x114 PNG with transparency)")

# =========================================================================
# 2. TABLET SCREENSHOTS (LANDSCAPE: 1920 x 1200 and 1280 x 800)
# =========================================================================
def generate_tablet_landscape():
    print("\n--- Generating Tablet Landscape Screenshots (1920x1200 and 1280x800) ---")
    W, H = 1920, 1200
    
    # --- Screen 1: Biometric and Shifts ---
    c1 = draw_gradient_canvas(W, H, (11, 17, 32), (4, 7, 15))
    draw_radial_glow(c1, 1480, 600, 580, (6, 182, 212), max_alpha=110)
    draw_radial_glow(c1, 1250, 780, 480, (79, 70, 229), max_alpha=80)
    draw_radial_glow(c1, 350, 250, 450, (14, 165, 233), max_alpha=50)
    draw_tech_grid(c1, grid_size=48, line_color=(30, 41, 59, 45))
    draw_biometric_rings(c1, 1500, 600, base_color=(6, 182, 212, 40))
    draw_circuit_lines(c1, W, H, base_color=(14, 165, 233, 40))
    
    d1 = ImageDraw.Draw(c1)
    f_badge = get_font(FONT_BOLD_PATH, 16)
    f_title = get_font(FONT_BOLD_PATH, 52)
    f_sub = get_font(FONT_REG_PATH, 23)
    f_card_title = get_font(FONT_BOLD_PATH, 22)
    f_card_body = get_font(FONT_REG_PATH, 18)
    f_status = get_font(FONT_BOLD_PATH, 16)
    
    x, y = 100, 100
    pill_text = "BIOMETRIC SECURITY and AI LIVENESS"
    p_box = d1.textbbox((x, y), pill_text, font=f_badge)
    p_w = p_box[2] - p_box[0] + 55
    d1.rounded_rectangle([x, y, x + p_w, y + 42], radius=21, fill=(15, 23, 42, 240), outline=(2, 132, 199), width=2)
    draw_vector_icon(d1, x + 22, y + 21, 24, 'eye', color=(56, 189, 248), bg_color=(8, 47, 73))
    d1.text((x + 42, y + 9), pill_text, font=f_badge, fill=(56, 189, 248))
    
    y += 66
    d1.text((x, y), "Smart Biometric and Dual Shift Attendance", font=f_title, fill=(255, 255, 255))
    y += 75
    d1.text((x, y), "Next-generation employee verification with anti-spoof eye-blink liveness and automated shift window control.", font=f_sub, fill=(148, 163, 184))
    
    cards1 = [
        ("eye", "Real-Time Eye-Blink Liveness Verification",
         "Dynamic eye-blink detection confirms physical employee presence and eliminates static photo spoofing."),
        ("clock", "Dynamic Shift Slots (Morning and Evening)",
         "Enforces official Morning (8 AM - 12 PM) and Evening (4 PM - 6 PM) shifts with smart age-adapted flexibility."),
        ("shield", "Committee Election Voting Unlock",
         "Completing dual attendance automatically unlocks user access to cast votes in election panels.")
    ]
    card_w, card_h = 950, 126
    y += 65
    for itype, title, body in cards1:
        d1.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=(30, 41, 59, 220), outline=(51, 65, 85, 230), width=1)
        draw_vector_icon(d1, x + 40, y + 46, 44, itype, color=(6, 182, 212), bg_color=(15, 23, 42))
        d1.text((x + 82, y + 26), title, font=f_card_title, fill=(248, 250, 252))
        d1.text((x + 82, y + 64), body, font=f_card_body, fill=(148, 163, 184))
        y += card_h + 24
        
    y += 15
    stat_text = "100% Offline SQLite Architecture with Automated Cloud Synchronization"
    d1.rounded_rectangle([x, y, x + card_w, y + 50], radius=25, fill=(6, 78, 59, 210), outline=(16, 185, 129), width=2)
    draw_vector_icon(d1, x + 28, y + 25, 28, 'check', color=(16, 185, 129), bg_color=(4, 47, 46))
    d1.text((x + 58, y + 13), stat_text, font=f_status, fill=(52, 211, 153))
    
    phone1 = create_device_mockup(img_user, target_h=960, corner_radius=36, border_width=12)
    c1.paste(phone1, (1260, 110), phone1)
    
    save_image_multi(c1, "tablet_screenshot_1_1920x1200", [(1280, 800, "tablet_screenshot_1_1280x800")])
    
    # --- Screen 2: Admin Records Portal ---
    c2 = draw_gradient_canvas(W, H, (11, 15, 25), (4, 6, 12))
    draw_radial_glow(c2, 1480, 600, 580, (16, 185, 129), max_alpha=110)
    draw_radial_glow(c2, 1250, 780, 480, (14, 165, 233), max_alpha=80)
    draw_radial_glow(c2, 350, 250, 450, (99, 102, 241), max_alpha=50)
    draw_tech_grid(c2, grid_size=48, line_color=(30, 41, 59, 45))
    draw_biometric_rings(c2, 1500, 600, base_color=(16, 185, 129, 40))
    draw_circuit_lines(c2, W, H, base_color=(16, 185, 129, 35))
    
    d2 = ImageDraw.Draw(c2)
    x, y = 100, 100
    pill_text = "CENTRALIZED ADMINISTRATION and AUDIT"
    p_box = d2.textbbox((x, y), pill_text, font=f_badge)
    p_w = p_box[2] - p_box[0] + 55
    d2.rounded_rectangle([x, y, x + p_w, y + 42], radius=21, fill=(15, 23, 42, 240), outline=(5, 150, 105), width=2)
    draw_vector_icon(d2, x + 22, y + 21, 24, 'chart', color=(52, 211, 153), bg_color=(6, 78, 59))
    d2.text((x + 42, y + 9), pill_text, font=f_badge, fill=(52, 211, 153))
    
    y += 66
    d2.text((x, y), "Enterprise Admin Portal and Real-Time Sync", font=f_title, fill=(255, 255, 255))
    y += 75
    d2.text((x, y), "Comprehensive administrator console to view, filter, verify, and export employee attendance logs across all occasions.", font=f_sub, fill=(148, 163, 184))
    
    cards2 = [
        ("chart", "Live Shift Analytics and Status Counters",
         "Instant count of Total Logs, Morning Shifts, Evening Shifts, and Synced status updated in real time."),
        ("shield", "Multi-Criteria Smart Filtering",
         "Filter records by User ID, Aadhaar number, date picker, shift type, or special committee occasions."),
        ("cloud", "Instant CSV Export and Server Sync",
         "Export audit-compliant CSV reports and sync unsynced local SQLite entries with cloud REST endpoints.")
    ]
    y += 65
    for itype, title, body in cards2:
        d2.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=(30, 41, 59, 220), outline=(51, 65, 85, 230), width=1)
        draw_vector_icon(d2, x + 40, y + 46, 44, itype, color=(16, 185, 129), bg_color=(15, 23, 42))
        d2.text((x + 82, y + 26), title, font=f_card_title, fill=(248, 250, 252))
        d2.text((x + 82, y + 64), body, font=f_card_body, fill=(148, 163, 184))
        y += card_h + 24
        
    y += 15
    stat_text = "Robust Retrofit REST API Architecture with Centralized Cloud Database"
    d2.rounded_rectangle([x, y, x + card_w, y + 50], radius=25, fill=(8, 47, 73, 210), outline=(2, 132, 199), width=2)
    draw_vector_icon(d2, x + 28, y + 25, 28, 'cloud', color=(56, 189, 248), bg_color=(12, 74, 110))
    d2.text((x + 58, y + 13), stat_text, font=f_status, fill=(56, 189, 248))
    
    phone2 = create_device_mockup(img_admin_portal, target_h=960, corner_radius=36, border_width=12)
    c2.paste(phone2, (1260, 110), phone2)
    
    save_image_multi(c2, "tablet_screenshot_2_1920x1200", [(1280, 800, "tablet_screenshot_2_1280x800")])
    
    # --- Screen 3: Pro In-App Subscriptions ---
    c3 = draw_gradient_canvas(W, H, (15, 12, 27), (6, 5, 12))
    draw_radial_glow(c3, 1480, 600, 580, (245, 158, 11), max_alpha=100)
    draw_radial_glow(c3, 1250, 780, 480, (139, 92, 246), max_alpha=80)
    draw_radial_glow(c3, 350, 250, 450, (217, 119, 6), max_alpha=50)
    draw_tech_grid(c3, grid_size=48, line_color=(45, 30, 59, 45))
    draw_biometric_rings(c3, 1500, 600, base_color=(245, 158, 11, 40))
    draw_circuit_lines(c3, W, H, base_color=(139, 92, 246, 35))
    
    d3 = ImageDraw.Draw(c3)
    x, y = 100, 100
    pill_text = "ENTERPRISE PRO ACCESS and BILLING"
    p_box = d3.textbbox((x, y), pill_text, font=f_badge)
    p_w = p_box[2] - p_box[0] + 55
    d3.rounded_rectangle([x, y, x + p_w, y + 42], radius=21, fill=(30, 20, 45, 240), outline=(217, 119, 6), width=2)
    draw_vector_icon(d3, x + 22, y + 21, 24, 'crown', color=(251, 191, 36), bg_color=(69, 26, 3))
    d3.text((x + 42, y + 9), pill_text, font=f_badge, fill=(251, 191, 36))
    
    y += 66
    d3.text((x, y), "Seamless In-App Purchases and Subscriptions", font=f_title, fill=(255, 255, 255))
    y += 75
    d3.text((x, y), "Powered by RevenueCat Amazon Store SDK with flexible monthly and annual subscription tiers for teams.", font=f_sub, fill=(148, 163, 184))
    
    cards3 = [
        ("crown", "Unlimited Logs and Automatic Cloud Backup",
         "Unlock unlimited offline SQLite attendance records and automated real-time background cloud sync."),
        ("location", "Biometric Face and GPS Geofence Verification",
         "Combine high-precision location coordinate stamping with face and blink verification for tamper-proof audits."),
        ("shield", "Amazon Appstore Native In-App Purchases",
         "1-click Amazon IAP billing with instant entitlement unlocking and cross-device subscription restoration.")
    ]
    y += 65
    for itype, title, body in cards3:
        d3.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=(35, 25, 48, 220), outline=(68, 48, 85, 230), width=1)
        draw_vector_icon(d3, x + 40, y + 46, 44, itype, color=(245, 158, 11), bg_color=(25, 18, 38))
        d3.text((x + 82, y + 26), title, font=f_card_title, fill=(248, 250, 252))
        d3.text((x + 82, y + 64), body, font=f_card_body, fill=(148, 163, 184))
        y += card_h + 24
        
    y += 15
    stat_text = "Priority 24/7 Technical Support and Enterprise Cloud Security Included"
    d3.rounded_rectangle([x, y, x + card_w, y + 50], radius=25, fill=(69, 26, 3, 210), outline=(217, 119, 6), width=2)
    draw_vector_icon(d3, x + 28, y + 25, 28, 'star', color=(251, 191, 36), bg_color=(120, 53, 15))
    d3.text((x + 58, y + 13), stat_text, font=f_status, fill=(251, 191, 36))
    
    phone3 = create_device_mockup(img_pro, target_h=960, corner_radius=36, border_width=12)
    c3.paste(phone3, (1260, 110), phone3)
    
    save_image_multi(c3, "tablet_screenshot_3_1920x1200", [(1280, 800, "tablet_screenshot_3_1280x800")])

# =========================================================================
# 3. TABLET SCREENSHOTS (PORTRAIT: 1200 x 1920 and 800 x 1280)
# =========================================================================
def generate_tablet_portrait():
    print("\n--- Generating Tablet Portrait Screenshots (1200x1920 and 800x1280) ---")
    W, H = 1200, 1920
    
    f_badge = get_font(FONT_BOLD_PATH, 18)
    f_title = get_font(FONT_BOLD_PATH, 44)
    f_sub = get_font(FONT_REG_PATH, 22)
    f_status = get_font(FONT_BOLD_PATH, 18)
    
    # Portrait 1: Biometric and Shifts
    p1 = draw_gradient_canvas(W, H, (11, 17, 32), (4, 7, 15))
    draw_radial_glow(p1, 600, 1100, 600, (6, 182, 212), max_alpha=110)
    draw_tech_grid(p1, grid_size=48, line_color=(30, 41, 59, 45))
    draw_biometric_rings(p1, 600, 1100, base_color=(6, 182, 212, 40))
    d1 = ImageDraw.Draw(p1)
    
    # Header
    pill_text = "BIOMETRIC ATTENDANCE and SHIFTS"
    p_box = d1.textbbox((0, 0), pill_text, font=f_badge)
    pw = p_box[2] - p_box[0] + 55
    d1.rounded_rectangle([(W - pw)//2, 70, (W + pw)//2, 115], radius=22, fill=(15, 23, 42, 240), outline=(2, 132, 199), width=2)
    draw_vector_icon(d1, (W - pw)//2 + 24, 92, 26, 'eye', color=(56, 189, 248), bg_color=(8, 47, 73))
    d1.text(((W - pw)//2 + 46, 79), pill_text, font=f_badge, fill=(56, 189, 248))
    
    title = "Smart Biometric and Dual Shift Attendance"
    t_box = d1.textbbox((0, 0), title, font=f_title)
    d1.text(((W - (t_box[2] - t_box[0]))//2, 135), title, font=f_title, fill=(255, 255, 255))
    
    sub = "Real-time face and eye-blink verification with automated morning/evening shift control."
    s_box = d1.textbbox((0, 0), sub, font=f_sub)
    d1.text(((W - (s_box[2] - s_box[0]))//2, 200), sub, font=f_sub, fill=(148, 163, 184))
    
    # Device Mockup in center
    dev1 = create_device_mockup(img_user, target_h=1380, corner_radius=44, border_width=14)
    dw, dh = dev1.size
    p1.paste(dev1, ((W - dw)//2, 260), dev1)
    
    # Bottom Status Bar
    stat = "Offline SQLite Storage  •  Amazon Fire Tablet and Fire OS Compatible"
    st_box = d1.textbbox((0, 0), stat, font=f_status)
    stw = st_box[2] - st_box[0] + 60
    d1.rounded_rectangle([(W - stw)//2, 1780, (W + stw)//2, 1840], radius=30, fill=(6, 78, 59, 220), outline=(16, 185, 129), width=2)
    draw_vector_icon(d1, (W - stw)//2 + 30, 1810, 30, 'check', color=(16, 185, 129), bg_color=(4, 47, 46))
    d1.text(((W - stw)//2 + 60, 1797), stat, font=f_status, fill=(52, 211, 153))
    
    save_image_multi(p1, "tablet_portrait_1_1200x1920", [(800, 1280, "tablet_portrait_1_800x1280")])
    
    # Portrait 2: Admin Records Portal
    p2 = draw_gradient_canvas(W, H, (11, 15, 25), (4, 6, 12))
    draw_radial_glow(p2, 600, 1100, 600, (16, 185, 129), max_alpha=110)
    draw_tech_grid(p2, grid_size=48, line_color=(30, 41, 59, 45))
    draw_biometric_rings(p2, 600, 1100, base_color=(16, 185, 129, 40))
    d2 = ImageDraw.Draw(p2)
    
    pill_text = "ENTERPRISE ADMIN MANAGEMENT"
    p_box = d2.textbbox((0, 0), pill_text, font=f_badge)
    pw = p_box[2] - p_box[0] + 55
    d2.rounded_rectangle([(W - pw)//2, 70, (W + pw)//2, 115], radius=22, fill=(15, 23, 42, 240), outline=(5, 150, 105), width=2)
    draw_vector_icon(d2, (W - pw)//2 + 24, 92, 26, 'chart', color=(52, 211, 153), bg_color=(6, 78, 59))
    d2.text(((W - pw)//2 + 46, 79), pill_text, font=f_badge, fill=(52, 211, 153))
    
    title = "Enterprise Admin Portal and Real-Time Sync"
    t_box = d2.textbbox((0, 0), title, font=f_title)
    d2.text(((W - (t_box[2] - t_box[0]))//2, 135), title, font=f_title, fill=(255, 255, 255))
    
    sub = "Live shift counters, multi-criteria filtering, and audit-ready CSV exports."
    s_box = d2.textbbox((0, 0), sub, font=f_sub)
    d2.text(((W - (s_box[2] - s_box[0]))//2, 200), sub, font=f_sub, fill=(148, 163, 184))
    
    dev2 = create_device_mockup(img_admin_portal, target_h=1380, corner_radius=44, border_width=14)
    dw, dh = dev2.size
    p2.paste(dev2, ((W - dw)//2, 260), dev2)
    
    stat = "Centralized REST API Sync  •  Amazon Fire Tablet and Fire OS Compatible"
    st_box = d2.textbbox((0, 0), stat, font=f_status)
    stw = st_box[2] - st_box[0] + 60
    d2.rounded_rectangle([(W - stw)//2, 1780, (W + stw)//2, 1840], radius=30, fill=(8, 47, 73, 220), outline=(2, 132, 199), width=2)
    draw_vector_icon(d2, (W - stw)//2 + 30, 1810, 30, 'cloud', color=(56, 189, 248), bg_color=(12, 74, 110))
    d2.text(((W - stw)//2 + 60, 1797), stat, font=f_status, fill=(56, 189, 248))
    
    save_image_multi(p2, "tablet_portrait_2_1200x1920", [(800, 1280, "tablet_portrait_2_800x1280")])
    
    # Portrait 3: Pro Subscriptions
    p3 = draw_gradient_canvas(W, H, (15, 12, 27), (6, 5, 12))
    draw_radial_glow(p3, 600, 1100, 600, (245, 158, 11), max_alpha=100)
    draw_tech_grid(p3, grid_size=48, line_color=(45, 30, 59, 45))
    draw_biometric_rings(p3, 600, 1100, base_color=(245, 158, 11, 40))
    d3 = ImageDraw.Draw(p3)
    
    pill_text = "ENTERPRISE PRO SUBSCRIPTIONS"
    p_box = d3.textbbox((0, 0), pill_text, font=f_badge)
    pw = p_box[2] - p_box[0] + 55
    d3.rounded_rectangle([(W - pw)//2, 70, (W + pw)//2, 115], radius=22, fill=(30, 20, 45, 240), outline=(217, 119, 6), width=2)
    draw_vector_icon(d3, (W - pw)//2 + 24, 92, 26, 'crown', color=(251, 191, 36), bg_color=(69, 26, 3))
    d3.text(((W - pw)//2 + 46, 79), pill_text, font=f_badge, fill=(251, 191, 36))
    
    title = "Seamless In-App Purchases and Subscriptions"
    t_box = d3.textbbox((0, 0), title, font=f_title)
    d3.text(((W - (t_box[2] - t_box[0]))//2, 135), title, font=f_title, fill=(255, 255, 255))
    
    sub = "Powered by RevenueCat Amazon Store SDK with flexible monthly and annual plans."
    s_box = d3.textbbox((0, 0), sub, font=f_sub)
    d3.text(((W - (s_box[2] - s_box[0]))//2, 200), sub, font=f_sub, fill=(148, 163, 184))
    
    dev3 = create_device_mockup(img_pro, target_h=1380, corner_radius=44, border_width=14)
    dw, dh = dev3.size
    p3.paste(dev3, ((W - dw)//2, 260), dev3)
    
    stat = "Native Amazon In-App Purchases  •  Instant Entitlement Verification"
    st_box = d3.textbbox((0, 0), stat, font=f_status)
    stw = st_box[2] - st_box[0] + 60
    d3.rounded_rectangle([(W - stw)//2, 1780, (W + stw)//2, 1840], radius=30, fill=(69, 26, 3, 220), outline=(217, 119, 6), width=2)
    draw_vector_icon(d3, (W - stw)//2 + 30, 1810, 30, 'star', color=(251, 191, 36), bg_color=(120, 53, 15))
    d3.text(((W - stw)//2 + 60, 1797), stat, font=f_status, fill=(251, 191, 36))
    
    save_image_multi(p3, "tablet_portrait_3_1200x1920", [(800, 1280, "tablet_portrait_3_800x1280")])

if __name__ == "__main__":
    generate_app_icons()
    generate_tablet_landscape()
    generate_tablet_portrait()
    print("\nALL TABLET ASSETS AND ICONS CREATED SUCCESSFULLY!")
