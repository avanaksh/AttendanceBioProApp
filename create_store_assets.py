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
    """Creates a smooth linear gradient canvas"""
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
    """Draws a soft radial glow onto canvas"""
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
    """Draws a subtle tech grid pattern"""
    w, h = canvas.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for x in range(0, w, grid_size):
        draw.line([(x, 0), (x, h)], fill=line_color, width=1)
    for y in range(0, h, grid_size):
        draw.line([(0, y), (w, y)], fill=line_color, width=1)
        
    canvas.paste(overlay, (0, 0), overlay)

def draw_circuit_lines(canvas, w, h, base_color=(6, 182, 212, 35)):
    """Draws subtle high-tech circuit / biometric lines"""
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    r, g, b, a = base_color
    nodes = [
        [(w - 650, 160), (w - 480, 160), (w - 400, 240), (w - 180, 240)],
        [(w - 750, 450), (w - 580, 450), (w - 500, 380), (w - 280, 380)],
        [(w - 820, 720), (w - 640, 720), (w - 550, 830), (w - 320, 830)],
        [(w - 520, 940), (w - 380, 940), (w - 280, 1020)]
    ]
    for path in nodes:
        for i in range(len(path) - 1):
            draw.line([path[i], path[i+1]], fill=(r, g, b, a), width=2)
        draw.ellipse([path[-1][0]-5, path[-1][1]-5, path[-1][0]+5, path[-1][1]+5], fill=(r, g, b, int(a*1.5)))
        draw.ellipse([path[0][0]-4, path[0][1]-4, path[0][0]+4, path[0][1]+4], fill=(r, g, b, int(a*1.5)))
        
    canvas.paste(overlay, (0, 0), overlay)

def draw_biometric_rings(canvas, center_x, center_y, base_color=(14, 165, 233, 40)):
    """Draws subtle concentric biometric target rings"""
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    r_val, g_val, b_val, a = base_color
    
    radii = [80, 160, 260, 380, 500]
    for rad in radii:
        draw.ellipse([center_x - rad, center_y - rad, center_x + rad, center_y + rad],
                     outline=(r_val, g_val, b_val, a), width=2)
    
    for angle_deg in range(0, 360, 30):
        ang = math.radians(angle_deg)
        x1 = center_x + int(250 * math.cos(ang))
        y1 = center_y + int(250 * math.sin(ang))
        x2 = center_x + int(270 * math.cos(ang))
        y2 = center_y + int(270 * math.sin(ang))
        draw.line([(x1, y1), (x2, y2)], fill=(r_val, g_val, b_val, int(a * 1.4)), width=2)
        
    canvas.paste(overlay, (0, 0), overlay)

def draw_vector_icon(draw, cx, cy, size, icon_type, color=(6, 182, 212), bg_color=(15, 23, 42)):
    """Draws a razor-sharp vector icon box"""
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
    """Trims away any light-gray window borders from Windows Snipping Tool"""
    im = im.convert('RGBA')
    w, h = im.size
    
    # Check if border is light gray
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

def create_phone_mockup(screen_img, target_h=860, corner_radius=34, border_width=10):
    """Wraps a screenshot into an ultra-modern bezel with shadows without covering status bar"""
    # Clean any snipping borders first
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
    
    # Outer dark titanium bezel
    frame_draw.rounded_rectangle(
        [0, 0, outer_w, outer_h],
        radius=corner_radius,
        fill=(15, 23, 42, 255),
        outline=(51, 65, 85, 255),
        width=2
    )
    
    # Paste curved screen cleanly inside bezel
    frame.paste(curved_screen, (border_width, border_width), curved_screen)
    
    # Speaker slit on TOP bezel (outside the screen so nothing is blocked!)
    slit_w = int(screen_w * 0.22)
    slit_h = 4
    slit_x = (outer_w - slit_w) // 2
    slit_y = max(3, border_width // 2 - 2)
    frame_draw.rounded_rectangle(
        [slit_x, slit_y, slit_x + slit_w, slit_y + slit_h],
        radius=2,
        fill=(5, 8, 15, 240)
    )
    
    # Realistic double drop shadow
    shadow_margin = 60
    total_w = outer_w + shadow_margin * 2
    total_h = outer_h + shadow_margin * 2
    
    canvas_with_shadow = Image.new('RGBA', (total_w, total_h), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(canvas_with_shadow)
    
    # Deep ambient drop shadow
    shadow_draw.rounded_rectangle(
        [shadow_margin, shadow_margin + 14, shadow_margin + outer_w, shadow_margin + outer_h + 14],
        radius=corner_radius,
        fill=(0, 0, 0, 180)
    )
    canvas_with_shadow = canvas_with_shadow.filter(ImageFilter.GaussianBlur(28))
    
    # Contact shadow
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

def save_image(img, base_name):
    """Saves both PNG (no transparency) and JPG to all output directories"""
    rgb_img = img.convert('RGB')
    for d in [DESKTOP_OUTPUT_DIR, PROJECT_OUTPUT_DIR]:
        png_path = os.path.join(d, f"{base_name}.png")
        jpg_path = os.path.join(d, f"{base_name}.jpg")
        rgb_img.save(png_path, "PNG", optimize=True)
        rgb_img.save(jpg_path, "JPEG", quality=95, optimize=True)
        print(f"Saved: {png_path} ({rgb_img.size[0]}x{rgb_img.size[1]})")

# Load source screenshots from atenapp
img_pro = Image.open(os.path.join(INPUT_DIR, "1.png"))
img_login = Image.open(os.path.join(INPUT_DIR, "2.png"))
img_user = Image.open(os.path.join(INPUT_DIR, "3.png"))
img_admin_portal = Image.open(os.path.join(INPUT_DIR, "2_admin.png"))
img_admin_home = Image.open(os.path.join(INPUT_DIR, "1_admin.png"))

print("Source screenshots loaded successfully.")

# =========================================================================
# 1. APP IMAGE (1280 x 720 px, landscape, no transparency)
# =========================================================================
def generate_app_image():
    print("Generating App Image (1280 x 720)...")
    W, H = 1280, 720
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (5, 8, 16))
    
    # Ambient glows
    draw_radial_glow(canvas, 1020, 360, 420, (6, 182, 212), max_alpha=110)
    draw_radial_glow(canvas, 750, 450, 360, (79, 70, 229), max_alpha=85)
    draw_radial_glow(canvas, 200, 150, 320, (14, 165, 233), max_alpha=50)
    
    draw_tech_grid(canvas, grid_size=40, line_color=(30, 41, 59, 40))
    draw_biometric_rings(canvas, 1040, 360, base_color=(6, 182, 212, 35))
    draw_circuit_lines(canvas, W, H, base_color=(14, 165, 233, 40))
    
    draw = ImageDraw.Draw(canvas)
    
    f_badge = get_font(FONT_BOLD_PATH, 14)
    f_title = get_font(FONT_BOLD_PATH, 58)
    f_sub = get_font(FONT_REG_PATH, 22)
    f_feat = get_font(FONT_BOLD_PATH, 16)
    f_compat = get_font(FONT_BOLD_PATH, 15)
    
    x = 75
    y = 65
    
    # Pill badge
    badge_text = "BIOMETRIC ATTENDANCE SUITE"
    b_box = draw.textbbox((x, y), badge_text, font=f_badge)
    b_w = b_box[2] - b_box[0] + 55
    b_h = 36
    draw.rounded_rectangle([x, y, x + b_w, y + b_h], radius=18, fill=(30, 41, 59, 230), outline=(99, 102, 241), width=2)
    draw_vector_icon(draw, x + 20, y + 18, 22, 'shield', color=(99, 102, 241), bg_color=(20, 27, 45))
    draw.text((x + 38, y + 8), badge_text, font=f_badge, fill=(165, 180, 252))
    
    # Title
    y += 58
    draw.text((x, y), "BioCheck Pro", font=f_title, fill=(255, 255, 255))
    
    # Tagline
    y += 75
    draw.text((x, y), "Smart Face and Eye-Blink Attendance Management", font=f_sub, fill=(148, 163, 184))
    
    # Feature Chips with vector icons
    features = [
        ("eye", "Anti-Spoof Eye-Blink Liveness Verification"),
        ("clock", "Dual Shift Slots: Morning and Evening"),
        ("chart", "Central Admin Portal and Instant CSV Export"),
        ("cloud", "Offline SQLite and Real-Time Cloud DB Sync")
    ]
    y += 50
    for itype, text in features:
        draw.rounded_rectangle([x, y, x + 460, y + 42], radius=10, fill=(30, 41, 59, 210), outline=(51, 65, 85, 230), width=1)
        draw_vector_icon(draw, x + 24, y + 21, 26, itype, color=(6, 182, 212), bg_color=(15, 23, 42))
        draw.text((x + 46, y + 10), text, font=f_feat, fill=(241, 245, 249))
        y += 52
        
    # Amazon Fire Compatibility Pill
    y += 15
    compat_text = "Optimized for Amazon Fire Tablets and Fire TV"
    draw.rounded_rectangle([x, y, x + 460, y + 42], radius=21, fill=(6, 78, 59, 200), outline=(16, 185, 129), width=2)
    draw_vector_icon(draw, x + 24, y + 21, 24, 'check', color=(16, 185, 129), bg_color=(4, 47, 46))
    draw.text((x + 46, y + 10), compat_text, font=f_compat, fill=(52, 211, 153))
    
    # Phone mockups on the right
    back_phone = create_phone_mockup(img_admin_portal, target_h=480, corner_radius=28, border_width=9)
    canvas.paste(back_phone, (860, 110), back_phone)
    
    front_phone = create_phone_mockup(img_user, target_h=530, corner_radius=30, border_width=10)
    canvas.paste(front_phone, (670, 80), front_phone)
    
    save_image(canvas, "app_image_1280x720")

# =========================================================================
# 2. SCREENSHOT 1 (1920 x 1080 px, landscape, no transparency)
# Theme: Biometric Attendance and Dual Shift Tracking (img_user: 3.png)
# =========================================================================
def generate_screenshot_1():
    print("Generating Screenshot 1 (1920 x 1080)...")
    W, H = 1920, 1080
    canvas = draw_gradient_canvas(W, H, (11, 17, 32), (4, 7, 15))
    
    # Ambient glows
    draw_radial_glow(canvas, 1480, 540, 540, (6, 182, 212), max_alpha=110)
    draw_radial_glow(canvas, 1250, 680, 450, (79, 70, 229), max_alpha=75)
    draw_radial_glow(canvas, 350, 200, 400, (14, 165, 233), max_alpha=45)
    
    draw_tech_grid(canvas, grid_size=48, line_color=(30, 41, 59, 45))
    draw_biometric_rings(canvas, 1500, 540, base_color=(6, 182, 212, 40))
    draw_circuit_lines(canvas, W, H, base_color=(14, 165, 233, 40))
    
    draw = ImageDraw.Draw(canvas)
    
    f_badge = get_font(FONT_BOLD_PATH, 16)
    f_title = get_font(FONT_BOLD_PATH, 50)
    f_sub = get_font(FONT_REG_PATH, 22)
    f_card_title = get_font(FONT_BOLD_PATH, 21)
    f_card_body = get_font(FONT_REG_PATH, 17)
    f_status = get_font(FONT_BOLD_PATH, 16)
    
    x = 100
    y = 80
    
    # Category Pill
    pill_text = "BIOMETRIC SECURITY and AI LIVENESS"
    p_box = draw.textbbox((x, y), pill_text, font=f_badge)
    p_w = p_box[2] - p_box[0] + 55
    draw.rounded_rectangle([x, y, x + p_w, y + 40], radius=20, fill=(15, 23, 42, 240), outline=(2, 132, 199), width=2)
    draw_vector_icon(draw, x + 22, y + 20, 24, 'eye', color=(56, 189, 248), bg_color=(8, 47, 73))
    draw.text((x + 42, y + 8), pill_text, font=f_badge, fill=(56, 189, 248))
    
    # Headline
    y += 62
    draw.text((x, y), "Smart Biometric and Dual Shift Attendance", font=f_title, fill=(255, 255, 255))
    
    # Subtitle
    y += 70
    draw.text((x, y), "Next-generation employee verification with anti-spoof eye-blink liveness and automated shift window control.", font=f_sub, fill=(148, 163, 184))
    
    # 3 Feature Cards
    cards = [
        ("eye", "Real-Time Eye-Blink Liveness Verification",
         "Dynamic eye-blink detection confirms physical employee presence and eliminates static photo spoofing."),
        ("clock", "Dynamic Shift Slots (Morning and Evening)",
         "Enforces official Morning (8 AM - 12 PM) and Evening (4 PM - 6 PM) shifts with smart age-adapted flexibility."),
        ("shield", "Committee Election Voting Unlock",
         "Completing dual attendance automatically unlocks user access to cast votes in election panels.")
    ]
    
    card_w = 950
    card_h = 118
    y += 55
    for itype, title, body in cards:
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=(30, 41, 59, 220), outline=(51, 65, 85, 230), width=1)
        draw_vector_icon(draw, x + 40, y + 42, 42, itype, color=(6, 182, 212), bg_color=(15, 23, 42))
        draw.text((x + 80, y + 24), title, font=f_card_title, fill=(248, 250, 252))
        draw.text((x + 80, y + 58), body, font=f_card_body, fill=(148, 163, 184))
        y += card_h + 20
        
    # Status Pill
    y += 10
    stat_text = "100% Offline SQLite Architecture with Automated Cloud Synchronization"
    draw.rounded_rectangle([x, y, x + card_w, y + 48], radius=24, fill=(6, 78, 59, 210), outline=(16, 185, 129), width=2)
    draw_vector_icon(draw, x + 28, y + 24, 28, 'check', color=(16, 185, 129), bg_color=(4, 47, 46))
    draw.text((x + 56, y + 12), stat_text, font=f_status, fill=(52, 211, 153))
    
    # Phone mockup on right
    phone = create_phone_mockup(img_user, target_h=860, corner_radius=36, border_width=12)
    canvas.paste(phone, (1260, 90), phone)
    
    save_image(canvas, "screenshot_1_1920x1080")

# =========================================================================
# 3. SCREENSHOT 2 (1920 x 1080 px, landscape, no transparency)
# Theme: Enterprise Admin Records Portal and Cloud Database (img_admin_portal: 2_admin.png)
# =========================================================================
def generate_screenshot_2():
    print("Generating Screenshot 2 (1920 x 1080)...")
    W, H = 1920, 1080
    canvas = draw_gradient_canvas(W, H, (11, 15, 25), (4, 6, 12))
    
    # Ambient glows
    draw_radial_glow(canvas, 1480, 540, 540, (16, 185, 129), max_alpha=110)
    draw_radial_glow(canvas, 1250, 680, 450, (14, 165, 233), max_alpha=75)
    draw_radial_glow(canvas, 350, 200, 400, (99, 102, 241), max_alpha=45)
    
    draw_tech_grid(canvas, grid_size=48, line_color=(30, 41, 59, 45))
    draw_biometric_rings(canvas, 1500, 540, base_color=(16, 185, 129, 40))
    draw_circuit_lines(canvas, W, H, base_color=(16, 185, 129, 35))
    
    draw = ImageDraw.Draw(canvas)
    
    f_badge = get_font(FONT_BOLD_PATH, 16)
    f_title = get_font(FONT_BOLD_PATH, 50)
    f_sub = get_font(FONT_REG_PATH, 22)
    f_card_title = get_font(FONT_BOLD_PATH, 21)
    f_card_body = get_font(FONT_REG_PATH, 17)
    f_status = get_font(FONT_BOLD_PATH, 16)
    
    x = 100
    y = 80
    
    # Category Pill
    pill_text = "CENTRALIZED ADMINISTRATION and AUDIT"
    p_box = draw.textbbox((x, y), pill_text, font=f_badge)
    p_w = p_box[2] - p_box[0] + 55
    draw.rounded_rectangle([x, y, x + p_w, y + 40], radius=20, fill=(15, 23, 42, 240), outline=(5, 150, 105), width=2)
    draw_vector_icon(draw, x + 22, y + 20, 24, 'chart', color=(52, 211, 153), bg_color=(6, 78, 59))
    draw.text((x + 42, y + 8), pill_text, font=f_badge, fill=(52, 211, 153))
    
    # Headline
    y += 62
    draw.text((x, y), "Enterprise Admin Portal and Real-Time Sync", font=f_title, fill=(255, 255, 255))
    
    # Subtitle
    y += 70
    draw.text((x, y), "Comprehensive administrator console to view, filter, verify, and export employee attendance logs across all occasions.", font=f_sub, fill=(148, 163, 184))
    
    # 3 Feature Cards
    cards = [
        ("chart", "Live Shift Analytics and Status Counters",
         "Instant count of Total Logs, Morning Shifts, Evening Shifts, and Synced status updated in real time."),
        ("shield", "Multi-Criteria Smart Filtering",
         "Filter records by User ID, Aadhaar number, date picker, shift type, or special committee occasions."),
        ("cloud", "Instant CSV Export and Server Sync",
         "Export audit-compliant CSV reports and sync unsynced local SQLite entries with cloud REST endpoints.")
    ]
    
    card_w = 950
    card_h = 118
    y += 55
    for itype, title, body in cards:
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=(30, 41, 59, 220), outline=(51, 65, 85, 230), width=1)
        draw_vector_icon(draw, x + 40, y + 42, 42, itype, color=(16, 185, 129), bg_color=(15, 23, 42))
        draw.text((x + 80, y + 24), title, font=f_card_title, fill=(248, 250, 252))
        draw.text((x + 80, y + 58), body, font=f_card_body, fill=(148, 163, 184))
        y += card_h + 20
        
    # Status Pill
    y += 10
    stat_text = "Robust Retrofit REST API Architecture with Centralized Cloud Database"
    draw.rounded_rectangle([x, y, x + card_w, y + 48], radius=24, fill=(8, 47, 73, 210), outline=(2, 132, 199), width=2)
    draw_vector_icon(draw, x + 28, y + 24, 28, 'cloud', color=(56, 189, 248), bg_color=(12, 74, 110))
    draw.text((x + 56, y + 12), stat_text, font=f_status, fill=(56, 189, 248))
    
    # Phone mockup on right
    phone = create_phone_mockup(img_admin_portal, target_h=860, corner_radius=36, border_width=12)
    canvas.paste(phone, (1260, 90), phone)
    
    save_image(canvas, "screenshot_2_1920x1080")

# =========================================================================
# 4. SCREENSHOT 3 (1920 x 1080 px, landscape, no transparency)
# Theme: BioCheck Pro In-App Subscriptions and Architecture (img_pro: 1.png)
# =========================================================================
def generate_screenshot_3():
    print("Generating Screenshot 3 (1920 x 1080)...")
    W, H = 1920, 1080
    canvas = draw_gradient_canvas(W, H, (15, 12, 27), (6, 5, 12))
    
    # Ambient glows
    draw_radial_glow(canvas, 1480, 540, 540, (245, 158, 11), max_alpha=100)
    draw_radial_glow(canvas, 1250, 680, 450, (139, 92, 246), max_alpha=75)
    draw_radial_glow(canvas, 350, 200, 400, (217, 119, 6), max_alpha=45)
    
    draw_tech_grid(canvas, grid_size=48, line_color=(45, 30, 59, 45))
    draw_biometric_rings(canvas, 1500, 540, base_color=(245, 158, 11, 40))
    draw_circuit_lines(canvas, W, H, base_color=(139, 92, 246, 35))
    
    draw = ImageDraw.Draw(canvas)
    
    f_badge = get_font(FONT_BOLD_PATH, 16)
    f_title = get_font(FONT_BOLD_PATH, 50)
    f_sub = get_font(FONT_REG_PATH, 22)
    f_card_title = get_font(FONT_BOLD_PATH, 21)
    f_card_body = get_font(FONT_REG_PATH, 17)
    f_status = get_font(FONT_BOLD_PATH, 16)
    
    x = 100
    y = 80
    
    # Category Pill
    pill_text = "ENTERPRISE PRO ACCESS and BILLING"
    p_box = draw.textbbox((x, y), pill_text, font=f_badge)
    p_w = p_box[2] - p_box[0] + 55
    draw.rounded_rectangle([x, y, x + p_w, y + 40], radius=20, fill=(30, 20, 45, 240), outline=(217, 119, 6), width=2)
    draw_vector_icon(draw, x + 22, y + 20, 24, 'crown', color=(251, 191, 36), bg_color=(69, 26, 3))
    draw.text((x + 42, y + 8), pill_text, font=f_badge, fill=(251, 191, 36))
    
    # Headline
    y += 62
    draw.text((x, y), "Seamless In-App Purchases and Subscriptions", font=f_title, fill=(255, 255, 255))
    
    # Subtitle
    y += 70
    draw.text((x, y), "Powered by RevenueCat Amazon Store SDK with flexible monthly and annual subscription tiers for teams.", font=f_sub, fill=(148, 163, 184))
    
    # 3 Feature Cards
    cards = [
        ("crown", "Unlimited Logs and Automatic Cloud Backup",
         "Unlock unlimited offline SQLite attendance records and automated real-time background cloud sync."),
        ("location", "Biometric Face and GPS Geofence Verification",
         "Combine high-precision location coordinate stamping with face and blink verification for tamper-proof audits."),
        ("shield", "Amazon Appstore Native In-App Purchases",
         "1-click Amazon IAP billing with instant entitlement unlocking and cross-device subscription restoration.")
    ]
    
    card_w = 950
    card_h = 118
    y += 55
    for itype, title, body in cards:
        draw.rounded_rectangle([x, y, x + card_w, y + card_h], radius=16, fill=(35, 25, 48, 220), outline=(68, 48, 85, 230), width=1)
        draw_vector_icon(draw, x + 40, y + 42, 42, itype, color=(245, 158, 11), bg_color=(25, 18, 38))
        draw.text((x + 80, y + 24), title, font=f_card_title, fill=(248, 250, 252))
        draw.text((x + 80, y + 58), body, font=f_card_body, fill=(148, 163, 184))
        y += card_h + 20
        
    # Status Pill
    y += 10
    stat_text = "Priority 24/7 Technical Support and Enterprise Cloud Security Included"
    draw.rounded_rectangle([x, y, x + card_w, y + 48], radius=24, fill=(69, 26, 3, 210), outline=(217, 119, 6), width=2)
    draw_vector_icon(draw, x + 28, y + 24, 28, 'star', color=(251, 191, 36), bg_color=(120, 53, 15))
    draw.text((x + 56, y + 12), stat_text, font=f_status, fill=(251, 191, 36))
    
    # Phone mockup on right
    phone = create_phone_mockup(img_pro, target_h=860, corner_radius=36, border_width=12)
    canvas.paste(phone, (1260, 90), phone)
    
    save_image(canvas, "screenshot_3_1920x1080")

# =========================================================================
# 5. BACKGROUND IMAGE (1920 x 1080 px, landscape, no transparency)
# Ambient backdrop for Fire TV and Fire Tablet product detail pages
# =========================================================================
def generate_background_image():
    print("Generating Background Image (1920 x 1080)...")
    W, H = 1920, 1080
    # Deep cinematic slate/navy background
    canvas = draw_gradient_canvas(W, H, (10, 15, 30), (3, 5, 12))
    
    # Multi-tier ambient light blooms
    draw_radial_glow(canvas, 1550, 320, 650, (6, 182, 212), max_alpha=95)
    draw_radial_glow(canvas, 1150, 780, 550, (99, 102, 241), max_alpha=80)
    draw_radial_glow(canvas, 1750, 850, 420, (16, 185, 129), max_alpha=65)
    draw_radial_glow(canvas, 300, 200, 450, (30, 58, 138), max_alpha=55)
    
    # High-tech grid
    draw_tech_grid(canvas, grid_size=48, line_color=(30, 41, 59, 45))
    
    # Concentric biometric target rings
    draw_biometric_rings(canvas, 1450, 480, base_color=(6, 182, 212, 45))
    draw_biometric_rings(canvas, 1100, 750, base_color=(99, 102, 241, 35))
    
    # Circuit tracks across canvas
    draw_circuit_lines(canvas, W, H, base_color=(14, 165, 233, 45))
    
    # Subtle glowing biometric shield emblem
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    # Large glowing shield watermark
    cx, cy, s = 1450, 480, 440
    pts = [
        (cx, cy - s//2),
        (cx + s//2, cy - s//4),
        (cx + int(s*0.42), cy + s//5),
        (cx, cy + s//2),
        (cx - int(s*0.42), cy + s//5),
        (cx - s//2, cy - s//4)
    ]
    d.polygon(pts, outline=(6, 182, 212, 45), width=3)
    
    # Inner biometric eye motif in shield
    eye_w, eye_h = int(s * 0.45), int(s * 0.25)
    d.ellipse([cx - eye_w, cy - eye_h, cx + eye_w, cy + eye_h], outline=(6, 182, 212, 45), width=2)
    d.ellipse([cx - eye_h//2, cy - eye_h//2, cx + eye_h//2, cy + eye_h//2], fill=(6, 182, 212, 35))
    
    # Subtle vignette on left/bottom to ensure Amazon Fire TV text is 100% legible
    vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for i in range(700):
        alpha = int(140 * (1.0 - i / 700.0))
        v_draw.line([(i, 0), (i, H)], fill=(3, 5, 12, alpha))
        
    canvas.paste(overlay, (0, 0), overlay)
    canvas.paste(vignette, (0, 0), vignette)
    
    save_image(canvas, "background_image_1920x1080")

if __name__ == "__main__":
    generate_app_image()
    generate_screenshot_1()
    generate_screenshot_2()
    generate_screenshot_3()
    generate_background_image()
    print("\nALL 5 STORE ASSETS GENERATED SUCCESSFULLY!")
