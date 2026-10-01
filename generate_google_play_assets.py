import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR_C = r"C:\AttendanceApp_RevenueCat\google_play_assets"
OUTPUT_DIR_F = r"F:\AttendanceApp_RevenueCat\google_play_assets"
OUTPUT_DIR_DESKTOP = r"C:\Users\HP\Desktop\google_play_assets"

for d in [OUTPUT_DIR_C, OUTPUT_DIR_F, OUTPUT_DIR_DESKTOP]:
    os.makedirs(d, exist_ok=True)

# System fonts
FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMIBOLD_PATH = r"C:\Windows\Fonts\seguisb.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\segoeui.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf" if "b" in path else r"C:\Windows\Fonts\arial.ttf", size)
        except Exception:
            return ImageFont.load_default()

def save_image(img, base_name):
    # Save PNG and JPG to all target directories
    for d in [OUTPUT_DIR_C, OUTPUT_DIR_F, OUTPUT_DIR_DESKTOP]:
        png_path = os.path.join(d, f"{base_name}.png")
        img.save(png_path, "PNG", quality=95)
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (11, 15, 25))
            rgb_img.paste(img, mask=img.split()[3])
            jpg_path = os.path.join(d, f"{base_name}.jpg")
            rgb_img.save(jpg_path, "JPEG", quality=92)
        else:
            jpg_path = os.path.join(d, f"{base_name}.jpg")
            img.save(jpg_path, "JPEG", quality=92)
    print(f"Generated: {base_name} ({img.size[0]}x{img.size[1]})")

def draw_gradient_canvas(width, height, top_color, bottom_color):
    base = Image.new('RGB', (width, height), top_color)
    top_r, top_g, top_b = top_color
    bot_r, bot_g, bot_b = bottom_color
    draw = ImageDraw.Draw(base)
    for y in range(height):
        ratio = y / float(height)
        r = int(top_r + (bot_r - top_r) * ratio)
        g = int(top_g + (bot_g - top_g) * ratio)
        b = int(top_b + (bot_b - top_b) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return base

def draw_radial_glow(canvas, center_x, center_y, radius, color, max_alpha=100):
    glow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    r_val, g_val, b_val = color
    steps = 30
    for s in range(steps, 0, -1):
        cur_radius = int(radius * (s / steps))
        alpha = int(max_alpha * (1.0 - (s / steps) ** 1.5))
        glow_draw.ellipse(
            [center_x - cur_radius, center_y - cur_radius, center_x + cur_radius, center_y + cur_radius],
            fill=(r_val, g_val, b_val, alpha)
        )
    glow = glow.filter(ImageFilter.GaussianBlur(max(2, radius // 15)))
    canvas.paste(glow, (0, 0), glow)

def draw_tech_grid(canvas, grid_size=40, line_color=(30, 41, 59, 40)):
    w, h = canvas.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(0, w, grid_size):
        draw.line([(x, 0), (x, h)], fill=line_color, width=1)
    for y in range(0, h, grid_size):
        draw.line([(0, y), (w, y)], fill=line_color, width=1)
    canvas.paste(overlay, (0, 0), overlay)

def draw_phone_mockup(canvas, x, y, width, height, draw_screen_content):
    """Draws a clean modern smartphone frame with curved bezel and displays screen content inside"""
    bezel_radius = 44
    screen_padding = 14
    
    # Outer device shadow
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([x-6, y-4, x+width+6, y+height+16], radius=bezel_radius+6, fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(shadow, (0, 0), shadow)

    # Device Outer Rim (Slate Titanium)
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([x, y, x+width, y+height], radius=bezel_radius, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=3)
    
    # Screen boundary
    sx1 = x + screen_padding
    sy1 = y + screen_padding
    sx2 = x + width - screen_padding
    sy2 = y + height - screen_padding
    sw = sx2 - sx1
    sh = sy2 - sy1
    
    # Inner Screen image
    screen = Image.new('RGBA', (sw, sh), (15, 23, 42, 255))
    screen_draw = ImageDraw.Draw(screen)
    draw_screen_content(screen, screen_draw, sw, sh)

    # Rounded screen mask
    screen_mask = Image.new('L', (sw, sh), 0)
    mask_draw = ImageDraw.Draw(screen_mask)
    mask_draw.rounded_rectangle([0, 0, sw, sh], radius=bezel_radius - 8, fill=255)
    
    overlay.paste(screen, (sx1, sy1), screen_mask)
    
    # Top Speaker and Camera Punch-hole
    cam_x = x + width // 2
    cam_y = y + screen_padding + 16
    d.ellipse([cam_x - 7, cam_y - 7, cam_x + 7, cam_y + 7], fill=(2, 6, 23, 255), outline=(30, 41, 59, 255), width=2)
    d.rounded_rectangle([cam_x - 30, y + 8, cam_x + 30, y + 12], radius=2, fill=(51, 65, 85, 255))
    
    canvas.paste(overlay, (0, 0), overlay)

def draw_header_bar(draw, w, title_text, org_text):
    # App top bar
    draw.rectangle([0, 0, w, 80], fill=(2, 6, 23, 255))
    draw.line([(0, 80), (w, 80)], fill=(30, 41, 59, 255), width=1)
    
    f_title = get_font(FONT_BOLD_PATH, 24)
    f_sub = get_font(FONT_REG_PATH, 16)
    draw.text((24, 18), title_text, font=f_title, fill=(255, 255, 255))
    draw.text((24, 48), org_text, font=f_sub, fill=(148, 163, 184))
    
    # Admin / Status pill
    f_pill = get_font(FONT_BOLD_PATH, 13)
    draw.rounded_rectangle([w - 110, 24, w - 24, 54], radius=14, fill=(245, 158, 11, 230))
    draw.text((w - 95, 31), "ADMIN", font=f_pill, fill=(15, 23, 42))

# ==============================================================================
# 1. APP ICON (512 x 512 px)
# ==============================================================================
def generate_app_icon():
    W, H = 512, 512
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    
    draw_radial_glow(canvas, 256, 256, 230, (6, 182, 212), max_alpha=120)
    draw_radial_glow(canvas, 256, 180, 160, (59, 130, 246), max_alpha=100)
    draw_tech_grid(canvas, grid_size=32, line_color=(30, 41, 59, 50))
    
    draw = ImageDraw.Draw(canvas)
    
    # Outer Rounded Shield
    cx, cy = 256, 256
    s = 340
    shield_pts = [
        (cx, cy - s//2),
        (cx + s//2, cy - s//4),
        (cx + int(s*0.42), cy + s//5),
        (cx, cy + s//2),
        (cx - int(s*0.42), cy + s//5),
        (cx - s//2, cy - s//4)
    ]
    draw.polygon(shield_pts, fill=(15, 23, 42, 230), outline=(6, 182, 212, 255))
    
    # Biometric Scanning Reticle Rings
    for r in [130, 95, 60]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(59, 130, 246, 120), width=2)
        
    # Target corner brackets
    bl = 24
    b_rad = 115
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        bx = cx + dx * b_rad
        by = cy + dy * b_rad
        draw.line([(bx, by), (bx + dx * bl, by)], fill=(6, 182, 212, 255), width=4)
        draw.line([(bx, by), (bx, by + dy * bl)], fill=(6, 182, 212, 255), width=4)

    # Stylized Liveness Eye Motif in center
    eye_w, eye_h = 70, 42
    draw.arc([cx - eye_w, cy - eye_h - 10, cx + eye_w, cy + eye_h + 10], start=20, end=160, fill=(6, 182, 212, 255), width=5)
    draw.arc([cx - eye_w, cy - eye_h - 10, cx + eye_w, cy + eye_h + 10], start=200, end=340, fill=(6, 182, 212, 255), width=5)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(59, 130, 246, 255), outline=(255, 255, 255, 255), width=3)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255, 255))
    
    # Gold verified check badge in bottom-right corner of shield
    badge_x, badge_y, br = cx + 85, cy + 85, 34
    draw.ellipse([badge_x - br, badge_y - br, badge_x + br, badge_y + br], fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=3)
    f_check = get_font(FONT_BOLD_PATH, 36)
    draw.text((badge_x - 16, badge_y - 25), "✓", font=f_check, fill=(255, 255, 255))

    save_image(canvas, "play_store_icon_512x512")

# ==============================================================================
# 2. GOOGLE PLAY FEATURE GRAPHIC (1024 x 500 px)
# ==============================================================================
def generate_feature_graphic():
    W, H = 1024, 500
    canvas = draw_gradient_canvas(W, H, (11, 15, 25), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    
    draw_radial_glow(canvas, 800, 250, 380, (6, 182, 212), max_alpha=110)
    draw_radial_glow(canvas, 200, 150, 300, (59, 130, 246), max_alpha=80)
    draw_tech_grid(canvas, grid_size=36, line_color=(30, 41, 59, 45))
    
    draw = ImageDraw.Draw(canvas)
    
    # Left Side: Typography and Badges
    f_badge = get_font(FONT_BOLD_PATH, 14)
    draw.rounded_rectangle([60, 65, 330, 102], radius=18, fill=(15, 23, 42, 240), outline=(6, 182, 212, 180), width=1)
    draw.text((78, 75), "⚡ 100% SECURE ON-DEVICE DUTY", font=f_badge, fill=(6, 182, 212))

    f_title = get_font(FONT_BOLD_PATH, 44)
    draw.text((60, 125), "Biometric Attendance\nand Duty Portal", font=f_title, fill=(255, 255, 255))
    
    f_sub = get_font(FONT_REG_PATH, 19)
    draw.text((60, 240), "• Face and Eye-Blink Liveness Verification\n• 3-Step Duty Sequence (Morning / Evening)\n• Official Committee Ballot Voting Station\n• Supreme Court, High Court and ICAR Portals", font=f_sub, fill=(148, 163, 184))
    
    # Feature pill highlights
    pills = ["👁️ Blink Verified", "🏛️ Multi-Institute", "🔒 Secure Database", "📊 CSV Audit"]
    px = 60
    py = 390
    for p in pills:
        draw.rounded_rectangle([px, py, px + 170, py + 42], radius=21, fill=(30, 41, 59, 220), outline=(51, 65, 85, 200), width=1)
        f_p = get_font(FONT_SEMIBOLD_PATH, 14)
        draw.text((px + 14, py + 12), p, font=f_p, fill=(241, 245, 249))
        px += 185
        
    # Right Side: Illustrated High-Tech Phone and Shield
    cx, cy = 820, 250
    s = 280
    shield_pts = [
        (cx, cy - s//2),
        (cx + s//2, cy - s//4),
        (cx + int(s*0.42), cy + s//5),
        (cx, cy + s//2),
        (cx - int(s*0.42), cy + s//5),
        (cx - s//2, cy - s//4)
    ]
    draw.polygon(shield_pts, fill=(15, 23, 42, 240), outline=(6, 182, 212, 255), width=2)
    
    for r in [100, 70, 45]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(59, 130, 246, 100), width=2)
        
    # Eye and Verified Icon
    draw.arc([cx - 50, cy - 35, cx + 50, cy + 35], start=20, end=160, fill=(6, 182, 212, 255), width=4)
    draw.arc([cx - 50, cy - 35, cx + 50, cy + 35], start=200, end=340, fill=(6, 182, 212, 255), width=4)
    draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(59, 130, 246, 255))
    
    # Verified card float
    draw.rounded_rectangle([cx - 120, cy + 90, cx + 120, cy + 155], radius=16, fill=(16, 185, 129, 230))
    f_vc = get_font(FONT_BOLD_PATH, 18)
    f_vcs = get_font(FONT_REG_PATH, 13)
    draw.text((cx - 100, cy + 102), "✓ Liveness Verified", font=f_vc, fill=(255, 255, 255))
    draw.text((cx - 100, cy + 128), "Confidence: 99.2% (Present)", font=f_vcs, fill=(241, 245, 249))

    save_image(canvas, "feature_graphic_1024x500")

# ==============================================================================
# 3. SCREENSHOT 1: BIOMETRIC SCANNER and EYE BLINK (1080 x 1920 px)
# ==============================================================================
def generate_screenshot_1():
    W, H = 1080, 1920
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 540, 300, 500, (6, 182, 212), max_alpha=110)
    draw_tech_grid(canvas, grid_size=48)
    
    draw = ImageDraw.Draw(canvas)
    
    # Marketing Banner Text at Top
    f_sub = get_font(FONT_BOLD_PATH, 24)
    f_main = get_font(FONT_BOLD_PATH, 54)
    f_desc = get_font(FONT_REG_PATH, 26)
    
    draw.text((70, 90), "BIOMETRIC VERIFICATION", font=f_sub, fill=(6, 182, 212))
    draw.text((70, 135), "Face and Eye-Blink Liveness", font=f_main, fill=(255, 255, 255))
    draw.text((70, 210), "Anti-spoofing liveness verification with on-device GPS logging", font=f_desc, fill=(148, 163, 184))
    
    # Phone Mockup
    pw, ph = 760, 1500
    px = (W - pw) // 2
    py = 310
    
    def render_screen(screen, s_draw, sw, sh):
        draw_header_bar(s_draw, sw, "Presiding Officer Alex", "Supreme Court and High Court")
        
        # User details card
        s_draw.rounded_rectangle([20, 100, sw - 20, 220], radius=16, fill=(30, 41, 59, 255))
        f_card_t = get_font(FONT_BOLD_PATH, 20)
        f_card_d = get_font(FONT_REG_PATH, 15)
        s_draw.text((36, 115), "👤 Alex Rivera (MEM-01)", font=f_card_t, fill=(255, 255, 255))
        s_draw.text((36, 145), "🆔 Aadhaar: 1234-5678-9021", font=f_card_d, fill=(148, 163, 184))
        s_draw.text((36, 170), "📍 Central District Headquarters • 19.0760 N, 72.8777 E", font=f_card_d, fill=(148, 163, 184))
        s_draw.text((36, 193), "🕒 Morning Shift: 09:00 - 13:00 | Evening: 16:00 - 19:00", font=f_card_d, fill=(6, 182, 212))

        # Camera Viewfinder Box
        cf_y1 = 240
        cf_y2 = 620
        s_draw.rounded_rectangle([20, cf_y1, sw - 20, cf_y2], radius=20, fill=(2, 6, 23, 255), outline=(59, 130, 246, 255), width=2)
        
        # Reticle in viewfinder
        vcx, vcy = sw // 2, (cf_y1 + cf_y2) // 2
        for r in [120, 85, 50]:
            s_draw.ellipse([vcx - r, vcy - r, vcx + r, vcy + r], outline=(6, 182, 212, 100), width=2)
        # Corner brackets
        bl = 30
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            cx = vcx + dx * 135
            cy = vcy + dy * 135
            s_draw.line([(cx, cy), (cx + dx * bl, cy)], fill=(6, 182, 212, 255), width=4)
            s_draw.line([(cx, cy), (cx, cy + dy * bl)], fill=(6, 182, 212, 255), width=4)
            
        # Liveness Prompt Banner
        s_draw.rounded_rectangle([40, cf_y2 - 65, sw - 40, cf_y2 - 15], radius=14, fill=(16, 185, 129, 240))
        f_live = get_font(FONT_BOLD_PATH, 18)
        s_draw.text((sw // 2 - 140, cf_y2 - 55), "👁️ Eye Blink Liveness Verified! (99.2%)", font=f_live, fill=(255, 255, 255))
        
        # Shift Action Buttons
        f_btn = get_font(FONT_BOLD_PATH, 20)
        s_draw.rounded_rectangle([20, 645, sw - 20, 725], radius=16, fill=(16, 185, 129, 255))
        s_draw.text((sw // 2 - 130, 670), "✓ STEP 1: MORNING VERIFIED", font=f_btn, fill=(255, 255, 255))
        
        s_draw.rounded_rectangle([20, 745, sw - 20, 825], radius=16, fill=(59, 130, 246, 255))
        s_draw.text((sw // 2 - 135, 770), "🗳️ STEP 2: OPEN BALLOT STATION", font=f_btn, fill=(255, 255, 255))

        s_draw.rounded_rectangle([20, 845, sw - 20, 925], radius=16, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=1)
        s_draw.text((sw // 2 - 135, 870), "🔒 STEP 3: EVENING SHIFT (16:00)", font=f_btn, fill=(148, 163, 184))

        # Recent Duty Log Item
        s_draw.rounded_rectangle([20, 950, sw - 20, 1080], radius=16, fill=(30, 41, 59, 255))
        f_log_h = get_font(FONT_BOLD_PATH, 17)
        f_log_t = get_font(FONT_REG_PATH, 14)
        s_draw.text((36, 965), "📋 Latest Secure Audit Record", font=f_log_h, fill=(245, 158, 11))
        s_draw.text((36, 995), "Type: Morning Shift • Verified Biometric + Eye Blink", font=f_log_t, fill=(255, 255, 255))
        s_draw.text((36, 1020), "Status: Morning Shift Verified • On-Device Storage", font=f_log_t, fill=(16, 185, 129))
        s_draw.text((36, 1045), "Timestamp: 01/10/2026, 09:14:22 AM", font=f_log_t, fill=(148, 163, 184))

    draw_phone_mockup(canvas, px, py, pw, ph, render_screen)
    save_image(canvas, "phone_screenshot_1_biometric_1080x1920")

# ==============================================================================
# 4. SCREENSHOT 2: 3-STEP DUTY SEQUENCE TRACKER (1080 x 1920 px)
# ==============================================================================
def generate_screenshot_2():
    W, H = 1080, 1920
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 540, 300, 500, (59, 130, 246), max_alpha=110)
    draw_tech_grid(canvas, grid_size=48)
    
    draw = ImageDraw.Draw(canvas)
    
    f_sub = get_font(FONT_BOLD_PATH, 24)
    f_main = get_font(FONT_BOLD_PATH, 54)
    f_desc = get_font(FONT_REG_PATH, 26)
    
    draw.text((70, 90), "STRUCTURED WORKFLOW", font=f_sub, fill=(59, 130, 246))
    draw.text((70, 135), "3-Step Duty Sequence", font=f_main, fill=(255, 255, 255))
    draw.text((70, 210), "Enforces strict sequential completion for attendance and ballots", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px = (W - pw) // 2
    py = 310
    
    def render_screen(screen, s_draw, sw, sh):
        draw_header_bar(s_draw, sw, "Session Sequence", "Supreme Court and High Court")
        
        # Step Cards
        steps = [
            ("STEP 1: MORNING SHIFT", "Biometric Face Scan + Eye Blink", "COMPLETED", (16, 185, 129), "09:14 AM • Liveness Verified"),
            ("STEP 2: COMMITTEE BALLOT", "IETE and Court Election Voting", "VOTE CAST (PROVISIONAL)", (245, 158, 11), "Ballot Cast • Awaiting Evening"),
            ("STEP 3: EVENING SHIFT", "End-of-Duty Departure Attendance", "ACTION REQUIRED", (59, 130, 246), "Window Open: 16:00 - 19:00")
        ]
        
        y_pos = 110
        f_s_title = get_font(FONT_BOLD_PATH, 19)
        f_s_sub = get_font(FONT_REG_PATH, 15)
        f_s_badge = get_font(FONT_BOLD_PATH, 13)
        
        for num, (title, sub, badge, color, details) in enumerate(steps, 1):
            s_draw.rounded_rectangle([20, y_pos, sw - 20, y_pos + 155], radius=18, fill=(30, 41, 59, 255), outline=color, width=2)
            
            # Number Circle
            s_draw.ellipse([38, y_pos + 20, 84, y_pos + 66], fill=color)
            f_num = get_font(FONT_BOLD_PATH, 24)
            s_draw.text((52, y_pos + 26), str(num), font=f_num, fill=(255, 255, 255))
            
            s_draw.text((98, y_pos + 22), title, font=f_s_title, fill=(255, 255, 255))
            s_draw.text((98, y_pos + 48), sub, font=f_s_sub, fill=(148, 163, 184))
            
            # Badge
            s_draw.rounded_rectangle([sw - 230, y_pos + 18, sw - 36, y_pos + 52], radius=12, fill=color)
            s_draw.text((sw - 220, y_pos + 26), badge, font=f_s_badge, fill=(255, 255, 255))
            
            # Detail divider
            s_draw.line([(38, y_pos + 90), (sw - 38, y_pos + 90)], fill=(51, 65, 85, 255), width=1)
            s_draw.text((38, y_pos + 105), f"⏱️ {details}", font=f_s_sub, fill=(203, 213, 225))
            
            y_pos += 185

        # Anti-Discrepancy Safeguard Card
        s_draw.rounded_rectangle([20, y_pos + 10, sw - 20, y_pos + 210], radius=18, fill=(2, 6, 23, 255), outline=(239, 68, 68, 255), width=2)
        f_disc_h = get_font(FONT_BOLD_PATH, 18)
        f_disc_t = get_font(FONT_REG_PATH, 14)
        s_draw.text((38, y_pos + 28), "🛡️ Discrepancy and Abandonment Monitor", font=f_disc_h, fill=(239, 68, 68))
        s_draw.text((38, y_pos + 62), "• If Evening Shift is absent, ballot is marked ABANDONED.\n• Member account is automatically locked to preserve audit.\n• Complete Step 3 to finalize both duty hours and vote count.", font=f_disc_t, fill=(203, 213, 225))

    draw_phone_mockup(canvas, px, py, pw, ph, render_screen)
    save_image(canvas, "phone_screenshot_2_sequence_1080x1920")

# ==============================================================================
# 5. SCREENSHOT 3: COMMITTEE BALLOT and VOTING STATION (1080 x 1920 px)
# ==============================================================================
def generate_screenshot_3():
    W, H = 1080, 1920
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 540, 300, 500, (16, 185, 129), max_alpha=110)
    draw_tech_grid(canvas, grid_size=48)
    
    draw = ImageDraw.Draw(canvas)
    
    f_sub = get_font(FONT_BOLD_PATH, 24)
    f_main = get_font(FONT_BOLD_PATH, 54)
    f_desc = get_font(FONT_REG_PATH, 26)
    
    draw.text((70, 90), "DEMOCRATIC GOVERNANCE", font=f_sub, fill=(16, 185, 129))
    draw.text((70, 135), "Committee Voting Station", font=f_main, fill=(255, 255, 255))
    draw.text((70, 210), "Provisional ballot casting with dual biometric authorization", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px = (W - pw) // 2
    py = 310
    
    def render_screen(screen, s_draw, sw, sh):
        draw_header_bar(s_draw, sw, "🗳️ Committee Ballots", "Supreme Court and High Court")
        
        # Topic Header
        s_draw.rounded_rectangle([20, 100, sw - 20, 210], radius=16, fill=(30, 41, 59, 255))
        f_th = get_font(FONT_BOLD_PATH, 20)
        f_ts = get_font(FONT_REG_PATH, 14)
        s_draw.text((36, 115), "Executive Disciplinary Council Election 2026", font=f_th, fill=(255, 255, 255))
        s_draw.text((36, 145), "Eligible: Presiding Officers and Registered Advocates", font=f_ts, fill=(148, 163, 184))
        s_draw.text((36, 170), "Status: 🟢 Active Ballot Window (Vote finalized after Step 3)", font=f_ts, fill=(16, 185, 129))

        # Candidates / Options
        options = [
            ("Adv. Priya Sharma", "Senior Council Nominee (Bar Association)", "VOTE CAST", (16, 185, 129)),
            ("Hon. Justice K. Raman", "Judicial Officer Representative", "SELECT", (59, 130, 246)),
            ("Dr. M. S. Venkatesh", "Independent Ethics Auditor", "SELECT", (59, 130, 246))
        ]
        
        y_pos = 230
        f_c_title = get_font(FONT_BOLD_PATH, 18)
        f_c_sub = get_font(FONT_REG_PATH, 14)
        f_c_b = get_font(FONT_BOLD_PATH, 14)
        
        for name, sub, b_text, color in options:
            s_draw.rounded_rectangle([20, y_pos, sw - 20, y_pos + 125], radius=16, fill=(15, 23, 42, 255), outline=color, width=2)
            
            s_draw.text((38, y_pos + 20), name, font=f_c_title, fill=(255, 255, 255))
            s_draw.text((38, y_pos + 50), sub, font=f_c_sub, fill=(148, 163, 184))
            
            s_draw.rounded_rectangle([sw - 160, y_pos + 38, sw - 36, y_pos + 84], radius=12, fill=color)
            s_draw.text((sw - 145, y_pos + 50), b_text, font=f_c_b, fill=(255, 255, 255))
            y_pos += 145

        # Biometric Verification Prompt Box
        s_draw.rounded_rectangle([20, y_pos + 20, sw - 20, y_pos + 200], radius=18, fill=(30, 41, 59, 255), outline=(16, 185, 129, 255), width=2)
        f_vp_h = get_font(FONT_BOLD_PATH, 18)
        f_vp_t = get_font(FONT_REG_PATH, 14)
        s_draw.text((38, y_pos + 40), "🔒 Biometric Ballot Confirmation", font=f_vp_h, fill=(16, 185, 129))
        s_draw.text((38, y_pos + 75), "• Dual Biometric Match: Eye Blink + Sensor Verified\n• Provisional Vote recorded in secure on-device database\n• Becomes OFFICIAL when Evening Shift is completed", font=f_vp_t, fill=(203, 213, 225))

    draw_phone_mockup(canvas, px, py, pw, ph, render_screen)
    save_image(canvas, "phone_screenshot_3_voting_1080x1920")

# ==============================================================================
# 6. SCREENSHOT 4: MULTI-INSTITUTION PORTAL (1080 x 1920 px)
# ==============================================================================
def generate_screenshot_4():
    W, H = 1080, 1920
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 540, 300, 500, (245, 158, 11), max_alpha=110)
    draw_tech_grid(canvas, grid_size=48)
    
    draw = ImageDraw.Draw(canvas)
    
    f_sub = get_font(FONT_BOLD_PATH, 24)
    f_main = get_font(FONT_BOLD_PATH, 54)
    f_desc = get_font(FONT_REG_PATH, 26)
    
    draw.text((70, 90), "INSTITUTIONAL ROLES", font=f_sub, fill=(245, 158, 11))
    draw.text((70, 135), "Multi-Organization Portal", font=f_main, fill=(255, 255, 255))
    draw.text((70, 210), "Switch seamlessly between Courts, ICAR Institutes and Universities", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px = (W - pw) // 2
    py = 310
    
    def render_screen(screen, s_draw, sw, sh):
        draw_header_bar(s_draw, sw, "Select Organization", "Universal Duty Gateway")
        
        orgs = [
            ("Supreme Court and High Court", "Presiding Officer / Registrar", "09:00 - 19:00", "ACTIVE SESSION", (16, 185, 129)),
            ("ICAR-CIFE Central Institute", "Senior Scientist / Faculty", "09:30 - 17:30", "REGISTERED", (59, 130, 246)),
            ("ICAR-IASRI New Delhi", "Research Fellow / Analyst", "10:00 - 18:00", "REGISTERED", (59, 130, 246)),
            ("IETE Technical Council", "Executive Council Member", "Flexible Duty", "BALLOT READY", (245, 158, 11))
        ]
        
        y_pos = 110
        f_o_title = get_font(FONT_BOLD_PATH, 18)
        f_o_sub = get_font(FONT_REG_PATH, 14)
        f_o_badge = get_font(FONT_BOLD_PATH, 12)
        
        for name, role, timing, b_text, color in orgs:
            s_draw.rounded_rectangle([20, y_pos, sw - 20, y_pos + 130], radius=16, fill=(30, 41, 59, 255), outline=color, width=2)
            
            s_draw.text((38, y_pos + 18), name, font=f_o_title, fill=(255, 255, 255))
            s_draw.text((38, y_pos + 46), f"💼 {role}", font=f_o_sub, fill=(203, 213, 225))
            s_draw.text((38, y_pos + 72), f"⏰ Duty Hours: {timing}", font=f_o_sub, fill=(148, 163, 184))
            
            s_draw.rounded_rectangle([sw - 165, y_pos + 20, sw - 36, y_pos + 56], radius=12, fill=color)
            s_draw.text((sw - 152, y_pos + 28), b_text, font=f_o_badge, fill=(255, 255, 255))
            
            y_pos += 150

        # Hardware Auto-Detection Banner
        s_draw.rounded_rectangle([20, y_pos + 20, sw - 20, y_pos + 190], radius=16, fill=(2, 6, 23, 255), outline=(6, 182, 212, 255), width=1)
        f_h_title = get_font(FONT_BOLD_PATH, 17)
        f_h_text = get_font(FONT_REG_PATH, 14)
        s_draw.text((38, y_pos + 38), "⚡ Hardware and OS Auto-Detection", font=f_h_title, fill=(6, 182, 212))
        s_draw.text((38, y_pos + 70), "• Android 14+ and Google Play Billing Ready\n• Auto-detects GPS, Camera and Telephony silently\n• Zero user disturbance or permission prompts at boot", font=f_h_text, fill=(203, 213, 225))

    draw_phone_mockup(canvas, px, py, pw, ph, render_screen)
    save_image(canvas, "phone_screenshot_4_organizations_1080x1920")

# ==============================================================================
# 7. SCREENSHOT 5: ADMIN AUDIT RECORDS and CSV EXPORT (1080 x 1920 px)
# ==============================================================================
def generate_screenshot_5():
    W, H = 1080, 1920
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 540, 300, 500, (6, 182, 212), max_alpha=110)
    draw_tech_grid(canvas, grid_size=48)
    
    draw = ImageDraw.Draw(canvas)
    
    f_sub = get_font(FONT_BOLD_PATH, 24)
    f_main = get_font(FONT_BOLD_PATH, 54)
    f_desc = get_font(FONT_REG_PATH, 26)
    
    draw.text((70, 90), "ADMIN AUDIT PORTAL", font=f_sub, fill=(6, 182, 212))
    draw.text((70, 135), "Records and Instant CSV Export", font=f_main, fill=(255, 255, 255))
    draw.text((70, 210), "Filter by Date, Occasion, Employee ID with 1-tap CSV export", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px = (W - pw) // 2
    py = 310
    
    def render_screen(screen, s_draw, sw, sh):
        draw_header_bar(s_draw, sw, "🛡️ Admin Records Portal", "Real-Time Device Audit Records")
        
        # Metric Cards Row
        metrics = [
            ("TOTAL", "128", (59, 130, 246)),
            ("MORNING", "64", (16, 185, 129)),
            ("EVENING", "64", (245, 158, 11)),
            ("VERIFIED", "128", (6, 182, 212))
        ]
        card_w = (sw - 40 - 24) // 4
        f_m_num = get_font(FONT_BOLD_PATH, 22)
        f_m_lbl = get_font(FONT_REG_PATH, 12)
        
        for i, (lbl, val, col) in enumerate(metrics):
            cx = 20 + i * (card_w + 8)
            s_draw.rounded_rectangle([cx, 100, cx + card_w, 175], radius=14, fill=(30, 41, 59, 255))
            s_draw.text((cx + 12, 112), val, font=f_m_num, fill=col)
            s_draw.text((cx + 12, 145), lbl, font=f_m_lbl, fill=(148, 163, 184))

        # Search Bar
        s_draw.rounded_rectangle([20, 190, sw - 20, 245], radius=14, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=1)
        f_search = get_font(FONT_REG_PATH, 15)
        s_draw.text((36, 205), "🔍 Search Aadhaar, Name or Employee ID...", font=f_search, fill=(100, 116, 139))
        
        # Action Buttons: Export CSV and Filter
        s_draw.rounded_rectangle([20, 260, sw // 2 - 8, 310], radius=12, fill=(99, 102, 241, 255))
        f_btn_a = get_font(FONT_BOLD_PATH, 15)
        s_draw.text((38, 275), "📥 EXPORT CSV REPORT", font=f_btn_a, fill=(255, 255, 255))
        
        s_draw.rounded_rectangle([sw // 2 + 8, 260, sw - 20, 310], radius=12, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=1)
        s_draw.text((sw // 2 + 24, 275), "📅 DATE: TODAY (ALL)", font=f_btn_a, fill=(203, 213, 225))

        # Records List
        records = [
            ("Alex Rivera", "ID: MEM-01 | Supreme Court", "Morning Shift", "01/10/2026, 09:14 AM", "Eye Blink Verified"),
            ("Priya Sharma", "ID: MEM-02 | Supreme Court", "Committee Ballot", "01/10/2026, 11:32 AM", "Provisional Cast"),
            ("Dr. R. K. Sen", "ID: MEM-03 | ICAR-CIFE", "Morning Shift", "01/10/2026, 09:28 AM", "Eye Blink Verified"),
            ("K. Venkatesh", "ID: MEM-04 | High Court", "Evening Shift", "01/10/2026, 17:05 PM", "Completed and Finalized")
        ]
        
        y_pos = 330
        f_r_n = get_font(FONT_BOLD_PATH, 16)
        f_r_s = get_font(FONT_REG_PATH, 13)
        f_r_b = get_font(FONT_BOLD_PATH, 12)
        
        for name, uid, shift, time, status in records:
            s_draw.rounded_rectangle([20, y_pos, sw - 20, y_pos + 95], radius=14, fill=(30, 41, 59, 255))
            
            s_draw.text((36, y_pos + 12), name, font=f_r_n, fill=(255, 255, 255))
            s_draw.text((36, y_pos + 38), uid, font=f_r_s, fill=(148, 163, 184))
            s_draw.text((36, y_pos + 62), f"📅 {time} • {status}", font=f_r_s, fill=(16, 185, 129))
            
            # Type Pill
            pill_col = (16, 185, 129) if "Morning" in shift else (245, 158, 11) if "Ballot" in shift else (59, 130, 246)
            s_draw.rounded_rectangle([sw - 145, y_pos + 16, sw - 36, y_pos + 46], radius=10, fill=pill_col)
            s_draw.text((sw - 135, y_pos + 23), shift, font=f_r_b, fill=(255, 255, 255))
            
            y_pos += 110

    draw_phone_mockup(canvas, px, py, pw, ph, render_screen)
    save_image(canvas, "phone_screenshot_5_admin_audit_1080x1920")

# ==============================================================================
# MAIN GENERATOR
# ==============================================================================
if __name__ == "__main__":
    print("Generating Google Play Store Graphics Suite...")
    generate_app_icon()
    generate_feature_graphic()
    generate_screenshot_1()
    generate_screenshot_2()
    generate_screenshot_3()
    generate_screenshot_4()
    generate_screenshot_5()
    print("\nALL GOOGLE PLAY ASSETS GENERATED SUCCESSFULLY!")
