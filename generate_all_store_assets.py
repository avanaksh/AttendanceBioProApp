import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Directories
PLAY_DIRS = [
    r"C:\AttendanceApp_RevenueCat\google_play_assets",
    r"F:\AttendanceApp_RevenueCat\google_play_assets",
    r"C:\Users\HP\Desktop\attendance_store_assets\google_play"
]

AMAZON_DIRS = [
    r"C:\AttendanceApp_RevenueCat\amazon_store_assets",
    r"C:\AttendanceApp_RevenueCat\store_assets",
    r"F:\AttendanceApp_RevenueCat\amazon_store_assets",
    r"C:\Users\HP\Desktop\attendance_store_assets\amazon"
]

for d in PLAY_DIRS + AMAZON_DIRS:
    os.makedirs(d, exist_ok=True)

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

def save_image_to_dirs(img, base_name, target_dirs):
    for d in target_dirs:
        png_path = os.path.join(d, f"{base_name}.png")
        img.save(png_path, "PNG", quality=95)
        # Also create crisp JPEG for store consoles requiring JPG
        rgb_img = Image.new('RGB', img.size, (11, 15, 25))
        if img.mode == 'RGBA':
            rgb_img.paste(img, mask=img.split()[3])
        else:
            rgb_img = img
        jpg_path = os.path.join(d, f"{base_name}.jpg")
        rgb_img.save(jpg_path, "JPEG", quality=92)
    print(f"Generated: {base_name} ({img.size[0]}x{img.size[1]})")

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
    glow = glow.filter(ImageFilter.GaussianBlur(max(2, radius // 14)))
    canvas.paste(glow, (0, 0), glow)

def draw_tech_grid(canvas, grid_size=40, line_color=(30, 41, 59, 45)):
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
        [(w - 750, 450), (w - 580, 450), (w - 500, 380), (w - 280, 380)],
        [(w - 820, 720), (w - 640, 720), (w - 550, 830), (w - 320, 830)]
    ]
    for path in nodes:
        for i in range(len(path) - 1):
            draw.line([path[i], path[i+1]], fill=(r, g, b, a), width=2)
        draw.ellipse([path[-1][0]-5, path[-1][1]-5, path[-1][0]+5, path[-1][1]+5], fill=(r, g, b, int(a*1.5)))
        draw.ellipse([path[0][0]-4, path[0][1]-4, path[0][0]+4, path[0][1]+4], fill=(r, g, b, int(a*1.5)))
    canvas.paste(overlay, (0, 0), overlay)

def draw_phone_frame(canvas, x, y, width, height, render_content):
    bezel_radius = 42
    screen_padding = 14
    
    # Shadow
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([x-6, y-4, x+width+6, y+height+16], radius=bezel_radius+6, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(shadow, (0, 0), shadow)

    # Frame
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([x, y, x+width, y+height], radius=bezel_radius, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=3)
    
    sx1 = x + screen_padding
    sy1 = y + screen_padding
    sx2 = x + width - screen_padding
    sy2 = y + height - screen_padding
    sw = sx2 - sx1
    sh = sy2 - sy1
    
    screen = Image.new('RGBA', (sw, sh), (15, 23, 42, 255))
    screen_draw = ImageDraw.Draw(screen)
    render_content(screen, screen_draw, sw, sh)

    screen_mask = Image.new('L', (sw, sh), 0)
    mask_draw = ImageDraw.Draw(screen_mask)
    mask_draw.rounded_rectangle([0, 0, sw, sh], radius=bezel_radius - 8, fill=255)
    overlay.paste(screen, (sx1, sy1), screen_mask)
    
    # Speaker bar and front camera
    cam_x = x + width // 2
    cam_y = y + screen_padding + 16
    d.ellipse([cam_x - 6, cam_y - 6, cam_x + 6, cam_y + 6], fill=(2, 6, 23, 255), outline=(30, 41, 59, 255), width=2)
    d.rounded_rectangle([cam_x - 28, y + 8, cam_x + 28, y + 12], radius=2, fill=(51, 65, 85, 255))
    
    canvas.paste(overlay, (0, 0), overlay)

def draw_header_nav(draw, w, title, subtitle, badge="ADMIN"):
    draw.rectangle([0, 0, w, 78], fill=(2, 6, 23, 255))
    draw.line([(0, 78), (w, 78)], fill=(30, 41, 59, 255), width=1)
    f_t = get_font(FONT_BOLD_PATH, 22)
    f_s = get_font(FONT_REG_PATH, 15)
    f_b = get_font(FONT_BOLD_PATH, 12)
    draw.text((22, 16), title, font=f_t, fill=(255, 255, 255))
    draw.text((22, 46), subtitle, font=f_s, fill=(148, 163, 184))
    if badge:
        draw.rounded_rectangle([w - 105, 22, w - 22, 52], radius=12, fill=(245, 158, 11, 230))
        draw.text((w - 92, 29), badge, font=f_b, fill=(15, 23, 42))

# ==============================================================================
# SECTION 1: COMMON ICONS (512x512 and 114x114)
# ==============================================================================
def generate_master_icons():
    # 512x512 Icon
    W, H = 512, 512
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 256, 256, 230, (6, 182, 212), max_alpha=120)
    draw_radial_glow(canvas, 256, 180, 160, (59, 130, 246), max_alpha=100)
    draw_tech_grid(canvas, grid_size=32, line_color=(30, 41, 59, 50))
    
    draw = ImageDraw.Draw(canvas)
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
    draw.polygon(shield_pts, fill=(15, 23, 42, 235), outline=(6, 182, 212, 255))
    for r in [130, 95, 60]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(59, 130, 246, 120), width=2)
    bl, b_rad = 24, 115
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        bx = cx + dx * b_rad
        by = cy + dy * b_rad
        draw.line([(bx, by), (bx + dx * bl, by)], fill=(6, 182, 212, 255), width=4)
        draw.line([(bx, by), (bx, by + dy * bl)], fill=(6, 182, 212, 255), width=4)

    eye_w, eye_h = 70, 42
    draw.arc([cx - eye_w, cy - eye_h - 10, cx + eye_w, cy + eye_h + 10], start=20, end=160, fill=(6, 182, 212, 255), width=5)
    draw.arc([cx - eye_w, cy - eye_h - 10, cx + eye_w, cy + eye_h + 10], start=200, end=340, fill=(6, 182, 212, 255), width=5)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(59, 130, 246, 255), outline=(255, 255, 255, 255), width=3)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255, 255))
    
    badge_x, badge_y, br = cx + 85, cy + 85, 34
    draw.ellipse([badge_x - br, badge_y - br, badge_x + br, badge_y + br], fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=3)
    f_check = get_font(FONT_BOLD_PATH, 36)
    draw.text((badge_x - 16, badge_y - 25), "✓", font=f_check, fill=(255, 255, 255))

    save_image_to_dirs(canvas, "play_store_icon_512x512", PLAY_DIRS)
    save_image_to_dirs(canvas, "icon_512x512", AMAZON_DIRS)

    # 114x114 Small Amazon Icon
    icon_114 = canvas.resize((114, 114), Image.Resampling.LANCZOS)
    save_image_to_dirs(icon_114, "icon_114x114", AMAZON_DIRS)

# ==============================================================================
# SECTION 2: GOOGLE PLAY STORE ASSETS
# ==============================================================================
def generate_google_play_feature_graphic():
    W, H = 1024, 500
    canvas = draw_gradient_canvas(W, H, (11, 15, 25), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 800, 250, 380, (6, 182, 212), max_alpha=110)
    draw_radial_glow(canvas, 200, 150, 300, (59, 130, 246), max_alpha=80)
    draw_tech_grid(canvas, grid_size=36, line_color=(30, 41, 59, 45))
    
    draw = ImageDraw.Draw(canvas)
    f_badge = get_font(FONT_BOLD_PATH, 14)
    draw.rounded_rectangle([60, 65, 360, 102], radius=18, fill=(15, 23, 42, 240), outline=(6, 182, 212, 180), width=1)
    draw.text((78, 75), "🔒 100% SECURE ON-DEVICE DUTY LOGS", font=f_badge, fill=(6, 182, 212))

    f_title = get_font(FONT_BOLD_PATH, 44)
    draw.text((60, 125), "Biometric Attendance\nand Duty Portal", font=f_title, fill=(255, 255, 255))
    
    f_sub = get_font(FONT_REG_PATH, 19)
    draw.text((60, 240), "• Face and Eye-Blink Liveness Verification\n• 3-Step Duty Sequence (Morning / Evening)\n• Official Committee Ballot Voting Station\n• 100% Local SQLite Database (Zero Server Required)", font=f_sub, fill=(148, 163, 184))
    
    pills = ["👁️ Blink Verified", "🏛️ Multi-Institute", "💾 Device SQLite", "📊 Instant CSV"]
    px, py = 60, 390
    for p in pills:
        draw.rounded_rectangle([px, py, px + 175, py + 42], radius=21, fill=(30, 41, 59, 220), outline=(51, 65, 85, 200), width=1)
        f_p = get_font(FONT_SEMIBOLD_PATH, 14)
        draw.text((px + 14, py + 12), p, font=f_p, fill=(241, 245, 249))
        px += 190
        
    cx, cy, s = 820, 250, 280
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
        
    draw.arc([cx - 50, cy - 35, cx + 50, cy + 35], start=20, end=160, fill=(6, 182, 212, 255), width=4)
    draw.arc([cx - 50, cy - 35, cx + 50, cy + 35], start=200, end=340, fill=(6, 182, 212, 255), width=4)
    draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(59, 130, 246, 255))
    
    draw.rounded_rectangle([cx - 120, cy + 90, cx + 120, cy + 155], radius=16, fill=(16, 185, 129, 230))
    f_vc = get_font(FONT_BOLD_PATH, 18)
    f_vcs = get_font(FONT_REG_PATH, 13)
    draw.text((cx - 100, cy + 102), "✓ Liveness Verified", font=f_vc, fill=(255, 255, 255))
    draw.text((cx - 100, cy + 128), "Secure Local SQLite Storage", font=f_vcs, fill=(241, 245, 249))

    save_image_to_dirs(canvas, "feature_graphic_1024x500", PLAY_DIRS)

def generate_play_screenshot_1():
    W, H = 1080, 1920
    canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 540, 300, 500, (6, 182, 212), max_alpha=110)
    draw_tech_grid(canvas, grid_size=48)
    
    draw = ImageDraw.Draw(canvas)
    f_sub = get_font(FONT_BOLD_PATH, 24)
    f_main = get_font(FONT_BOLD_PATH, 54)
    f_desc = get_font(FONT_REG_PATH, 26)
    
    draw.text((70, 90), "BIOMETRIC VERIFICATION", font=f_sub, fill=(6, 182, 212))
    draw.text((70, 135), "Face and Eye-Blink Liveness", font=f_main, fill=(255, 255, 255))
    draw.text((70, 210), "Anti-spoofing liveness verified directly on device", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px, py = (W - pw) // 2, 310
    
    def render(screen, s_draw, sw, sh):
        draw_header_nav(s_draw, sw, "Presiding Officer Alex", "Supreme Court and High Court")
        s_draw.rounded_rectangle([20, 95, sw - 20, 215], radius=16, fill=(30, 41, 59, 255))
        f_card_t = get_font(FONT_BOLD_PATH, 19)
        f_card_d = get_font(FONT_REG_PATH, 14)
        s_draw.text((36, 110), "👤 Alex Rivera (MEM-01)", font=f_card_t, fill=(255, 255, 255))
        s_draw.text((36, 138), "🆔 Aadhaar: 1234-5678-9021 • Central Headquarters", font=f_card_d, fill=(148, 163, 184))
        s_draw.text((36, 162), "📍 Location: 19.0760 N, 72.8777 E (Device GPS)", font=f_card_d, fill=(148, 163, 184))
        s_draw.text((36, 186), "🕒 Morning: 09:00 - 13:00 | Evening: 16:00 - 19:00", font=f_card_d, fill=(6, 182, 212))

        cf_y1, cf_y2 = 230, 610
        s_draw.rounded_rectangle([20, cf_y1, sw - 20, cf_y2], radius=20, fill=(2, 6, 23, 255), outline=(59, 130, 246, 255), width=2)
        vcx, vcy = sw // 2, (cf_y1 + cf_y2) // 2
        for r in [120, 85, 50]:
            s_draw.ellipse([vcx - r, vcy - r, vcx + r, vcy + r], outline=(6, 182, 212, 100), width=2)
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            cx, cy = vcx + dx * 135, vcy + dy * 135
            s_draw.line([(cx, cy), (cx + dx * 30, cy)], fill=(6, 182, 212, 255), width=4)
            s_draw.line([(cx, cy), (cx, cy + dy * 30)], fill=(6, 182, 212, 255), width=4)
            
        s_draw.rounded_rectangle([40, cf_y2 - 65, sw - 40, cf_y2 - 15], radius=14, fill=(16, 185, 129, 240))
        f_live = get_font(FONT_BOLD_PATH, 18)
        s_draw.text((sw // 2 - 145, cf_y2 - 55), "👁️ Eye Blink Liveness Verified! (99.2%)", font=f_live, fill=(255, 255, 255))
        
        f_btn = get_font(FONT_BOLD_PATH, 19)
        s_draw.rounded_rectangle([20, 635, sw - 20, 715], radius=16, fill=(16, 185, 129, 255))
        s_draw.text((sw // 2 - 130, 660), "✓ STEP 1: MORNING VERIFIED", font=f_btn, fill=(255, 255, 255))
        
        s_draw.rounded_rectangle([20, 735, sw - 20, 815], radius=16, fill=(59, 130, 246, 255))
        s_draw.text((sw // 2 - 135, 760), "🗳️ STEP 2: OPEN BALLOT STATION", font=f_btn, fill=(255, 255, 255))

        s_draw.rounded_rectangle([20, 835, sw - 20, 915], radius=16, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=1)
        s_draw.text((sw // 2 - 135, 860), "🔒 STEP 3: EVENING SHIFT (16:00)", font=f_btn, fill=(148, 163, 184))

        s_draw.rounded_rectangle([20, 940, sw - 20, 1070], radius=16, fill=(30, 41, 59, 255))
        f_log_h = get_font(FONT_BOLD_PATH, 17)
        f_log_t = get_font(FONT_REG_PATH, 14)
        s_draw.text((36, 955), "📋 Latest Secure Duty Log (Device SQLite)", font=f_log_h, fill=(245, 158, 11))
        s_draw.text((36, 985), "Shift: Morning Shift • Biometric Face + Eye Blink", font=f_log_t, fill=(255, 255, 255))
        s_draw.text((36, 1010), "Storage: 💾 SECURE LOCAL DATABASE (On-Device)", font=f_log_t, fill=(16, 185, 129))
        s_draw.text((36, 1035), "Timestamp: 01/10/2026, 09:14:22 AM", font=f_log_t, fill=(148, 163, 184))

    draw_phone_frame(canvas, px, py, pw, ph, render)
    save_image_to_dirs(canvas, "phone_screenshot_1_biometric_1080x1920", PLAY_DIRS)

def generate_play_screenshot_2():
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
    draw.text((70, 210), "Enforces strict sequential duty: Morning ➔ Ballot ➔ Evening", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px, py = (W - pw) // 2, 310
    
    def render(screen, s_draw, sw, sh):
        draw_header_nav(s_draw, sw, "Session Sequence", "Supreme Court and High Court")
        steps = [
            ("STEP 1: MORNING SHIFT", "Biometric Face Scan + Eye Blink", "COMPLETED", (16, 185, 129), "09:14 AM • Liveness Verified"),
            ("STEP 2: COMMITTEE BALLOT", "IETE and Court Election Voting", "VOTE CAST (PROVISIONAL)", (245, 158, 11), "Ballot Cast • Awaiting Evening"),
            ("STEP 3: EVENING SHIFT", "End-of-Duty Departure Attendance", "ACTION REQUIRED", (59, 130, 246), "Window Open: 16:00 - 19:00")
        ]
        
        y_pos = 110
        f_s_title = get_font(FONT_BOLD_PATH, 19)
        f_s_sub = get_font(FONT_REG_PATH, 14)
        f_s_badge = get_font(FONT_BOLD_PATH, 12)
        
        for num, (title, sub, badge, color, details) in enumerate(steps, 1):
            s_draw.rounded_rectangle([20, y_pos, sw - 20, y_pos + 155], radius=18, fill=(30, 41, 59, 255), outline=color, width=2)
            s_draw.ellipse([38, y_pos + 20, 84, y_pos + 66], fill=color)
            f_num = get_font(FONT_BOLD_PATH, 24)
            s_draw.text((52, y_pos + 26), str(num), font=f_num, fill=(255, 255, 255))
            
            s_draw.text((98, y_pos + 22), title, font=f_s_title, fill=(255, 255, 255))
            s_draw.text((98, y_pos + 48), sub, font=f_s_sub, fill=(148, 163, 184))
            
            s_draw.rounded_rectangle([sw - 230, y_pos + 18, sw - 36, y_pos + 52], radius=12, fill=color)
            s_draw.text((sw - 220, y_pos + 26), badge, font=f_s_badge, fill=(255, 255, 255))
            
            s_draw.line([(38, y_pos + 90), (sw - 38, y_pos + 90)], fill=(51, 65, 85, 255), width=1)
            s_draw.text((38, y_pos + 105), f"⏱️ {details}", font=f_s_sub, fill=(203, 213, 225))
            y_pos += 185

        s_draw.rounded_rectangle([20, y_pos + 10, sw - 20, y_pos + 210], radius=18, fill=(2, 6, 23, 255), outline=(239, 68, 68, 255), width=2)
        f_disc_h = get_font(FONT_BOLD_PATH, 18)
        f_disc_t = get_font(FONT_REG_PATH, 14)
        s_draw.text((38, y_pos + 28), "🛡️ Discrepancy and Abandonment Monitor", font=f_disc_h, fill=(239, 68, 68))
        s_draw.text((38, y_pos + 62), "• If Evening Shift is absent, ballot is marked ABANDONED.\n• Member account is automatically frozen to preserve audit.\n• Complete Step 3 to finalize both duty hours and vote count.", font=f_disc_t, fill=(203, 213, 225))

    draw_phone_frame(canvas, px, py, pw, ph, render)
    save_image_to_dirs(canvas, "phone_screenshot_2_sequence_1080x1920", PLAY_DIRS)

def generate_play_screenshot_3():
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
    draw.text((70, 210), "Provisional ballot casting with dual biometric verification", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px, py = (W - pw) // 2, 310
    
    def render(screen, s_draw, sw, sh):
        draw_header_nav(s_draw, sw, "🗳️ Committee Ballots", "Supreme Court and High Court")
        s_draw.rounded_rectangle([20, 95, sw - 20, 205], radius=16, fill=(30, 41, 59, 255))
        f_th = get_font(FONT_BOLD_PATH, 19)
        f_ts = get_font(FONT_REG_PATH, 14)
        s_draw.text((36, 110), "Executive Disciplinary Council Election 2026", font=f_th, fill=(255, 255, 255))
        s_draw.text((36, 140), "Eligible: Presiding Officers and Registered Advocates", font=f_ts, fill=(148, 163, 184))
        s_draw.text((36, 165), "Status: 🟢 Active Ballot Window (Vote finalized after Step 3)", font=f_ts, fill=(16, 185, 129))

        options = [
            ("Adv. Priya Sharma", "Senior Council Nominee (Bar Association)", "VOTE CAST", (16, 185, 129)),
            ("Hon. Justice K. Raman", "Judicial Officer Representative", "SELECT", (59, 130, 246)),
            ("Dr. M. S. Venkatesh", "Independent Ethics Auditor", "SELECT", (59, 130, 246))
        ]
        
        y_pos = 225
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

        s_draw.rounded_rectangle([20, y_pos + 20, sw - 20, y_pos + 200], radius=18, fill=(30, 41, 59, 255), outline=(16, 185, 129, 255), width=2)
        f_vp_h = get_font(FONT_BOLD_PATH, 18)
        f_vp_t = get_font(FONT_REG_PATH, 14)
        s_draw.text((38, y_pos + 40), "🔒 Biometric Ballot Confirmation", font=f_vp_h, fill=(16, 185, 129))
        s_draw.text((38, y_pos + 75), "• Dual Biometric Match: Eye Blink + Sensor Verified\n• Provisional Vote recorded in secure on-device database\n• Becomes OFFICIAL when Evening Shift is completed", font=f_vp_t, fill=(203, 213, 225))

    draw_phone_frame(canvas, px, py, pw, ph, render)
    save_image_to_dirs(canvas, "phone_screenshot_3_voting_1080x1920", PLAY_DIRS)

def generate_play_screenshot_4():
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
    draw.text((70, 210), "Supreme Court, High Court and ICAR Research Institutes", font=f_desc, fill=(148, 163, 184))
    
    pw, ph = 760, 1500
    px, py = (W - pw) // 2, 310
    
    def render(screen, s_draw, sw, sh):
        draw_header_nav(s_draw, sw, "Select Organization", "Universal Duty Gateway")
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

        s_draw.rounded_rectangle([20, y_pos + 20, sw - 20, y_pos + 190], radius=16, fill=(2, 6, 23, 255), outline=(6, 182, 212, 255), width=1)
        f_h_title = get_font(FONT_BOLD_PATH, 17)
        f_h_text = get_font(FONT_REG_PATH, 14)
        s_draw.text((38, y_pos + 38), "⚡ Hardware and OS Auto-Detection", font=f_h_title, fill=(6, 182, 212))
        s_draw.text((38, y_pos + 70), "• Android 14+ and Google Play Billing Ready\n• Auto-detects GPS, Camera and Telephony silently\n• Zero user disturbance or permission prompts at boot", font=f_h_text, fill=(203, 213, 225))

    draw_phone_frame(canvas, px, py, pw, ph, render)
    save_image_to_dirs(canvas, "phone_screenshot_4_organizations_1080x1920", PLAY_DIRS)

def generate_play_screenshot_5():
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
    px, py = (W - pw) // 2, 310
    
    def render(screen, s_draw, sw, sh):
        draw_header_nav(s_draw, sw, "🛡️ Admin Records Portal", "Real-Time Device Audit Records")
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
            s_draw.rounded_rectangle([cx, 95, cx + card_w, 170], radius=14, fill=(30, 41, 59, 255))
            s_draw.text((cx + 12, 107), val, font=f_m_num, fill=col)
            s_draw.text((cx + 12, 140), lbl, font=f_m_lbl, fill=(148, 163, 184))

        s_draw.rounded_rectangle([20, 185, sw - 20, 240], radius=14, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=1)
        f_search = get_font(FONT_REG_PATH, 15)
        s_draw.text((36, 200), "🔍 Search Aadhaar, Name or Employee ID...", font=f_search, fill=(100, 116, 139))
        
        s_draw.rounded_rectangle([20, 255, sw // 2 - 8, 305], radius=12, fill=(99, 102, 241, 255))
        f_btn_a = get_font(FONT_BOLD_PATH, 15)
        s_draw.text((38, 270), "📥 EXPORT CSV REPORT", font=f_btn_a, fill=(255, 255, 255))
        
        s_draw.rounded_rectangle([sw // 2 + 8, 255, sw - 20, 305], radius=12, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=1)
        s_draw.text((sw // 2 + 24, 270), "📅 DATE: TODAY (ALL)", font=f_btn_a, fill=(203, 213, 225))

        records = [
            ("Alex Rivera", "ID: MEM-01 | Supreme Court", "Morning Shift", "01/10/2026, 09:14 AM", "Eye Blink Verified"),
            ("Priya Sharma", "ID: MEM-02 | Supreme Court", "Committee Ballot", "01/10/2026, 11:32 AM", "Provisional Cast"),
            ("Dr. R. K. Sen", "ID: MEM-03 | ICAR-CIFE", "Morning Shift", "01/10/2026, 09:28 AM", "Eye Blink Verified"),
            ("K. Venkatesh", "ID: MEM-04 | High Court", "Evening Shift", "01/10/2026, 17:05 PM", "Completed and Finalized")
        ]
        
        y_pos = 325
        f_r_n = get_font(FONT_BOLD_PATH, 16)
        f_r_s = get_font(FONT_REG_PATH, 13)
        f_r_b = get_font(FONT_BOLD_PATH, 12)
        
        for name, uid, shift, time, status in records:
            s_draw.rounded_rectangle([20, y_pos, sw - 20, y_pos + 95], radius=14, fill=(30, 41, 59, 255))
            s_draw.text((36, y_pos + 12), name, font=f_r_n, fill=(255, 255, 255))
            s_draw.text((36, y_pos + 38), uid, font=f_r_s, fill=(148, 163, 184))
            s_draw.text((36, y_pos + 62), f"📅 {time} • {status}", font=f_r_s, fill=(16, 185, 129))
            pill_col = (16, 185, 129) if "Morning" in shift else (245, 158, 11) if "Ballot" in shift else (59, 130, 246)
            s_draw.rounded_rectangle([sw - 145, y_pos + 16, sw - 36, y_pos + 46], radius=10, fill=pill_col)
            s_draw.text((sw - 135, y_pos + 23), shift, font=f_r_b, fill=(255, 255, 255))
            y_pos += 110

    draw_phone_frame(canvas, px, py, pw, ph, render)
    save_image_to_dirs(canvas, "phone_screenshot_5_admin_audit_1080x1920", PLAY_DIRS)

# ==============================================================================
# SECTION 3: AMAZON APPSTORE and FIRE TV ASSETS
# ==============================================================================
def generate_amazon_background():
    # 1920x1080 Fire TV Backdrop
    W, H = 1920, 1080
    canvas = draw_gradient_canvas(W, H, (11, 15, 25), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 1550, 320, 650, (6, 182, 212), max_alpha=95)
    draw_radial_glow(canvas, 1150, 780, 550, (99, 102, 241), max_alpha=80)
    draw_tech_grid(canvas, grid_size=48, line_color=(30, 41, 59, 45))
    draw_circuit_lines(canvas, W, H, base_color=(14, 165, 233, 45))
    
    draw = ImageDraw.Draw(canvas)
    f_badge = get_font(FONT_BOLD_PATH, 18)
    draw.rounded_rectangle([100, 120, 480, 168], radius=24, fill=(15, 23, 42, 240), outline=(6, 182, 212, 200), width=2)
    draw.text((125, 132), "🔥 AMAZON FIRE TV and TABLET EDITION", font=f_badge, fill=(6, 182, 212))

    f_title = get_font(FONT_BOLD_PATH, 58)
    draw.text((100, 200), "Biometric Duty Attendance\nand Committee Ballot Station", font=f_title, fill=(255, 255, 255))

    f_sub = get_font(FONT_REG_PATH, 24)
    desc = (
        "• 100% Secure Local SQLite Database Storage (Zero Cloud Dependency)\n"
        "• Hardware-Aware Biometric Liveness Verification (Fire OS and Fire TV)\n"
        "• 3-Step Sequence: Morning Verification ➔ Committee Ballot ➔ Evening Shift\n"
        "• Official Multi-Organization Portal: Supreme Court, High Court and ICAR\n"
        "• Admin Records Audit Portal with Instant CSV Report Export"
    )
    draw.text((100, 360), desc, font=f_sub, fill=(203, 213, 225))

    pills = [
        ("👁️ Eye Blink Liveness", (6, 182, 212)),
        ("💾 Secure Local SQLite", (16, 185, 129)),
        ("📺 Fire TV Leanback D-Pad", (245, 158, 11)),
        ("📊 Instant CSV Export", (99, 102, 241))
    ]
    px, py = 100, 680
    for p, col in pills:
        draw.rounded_rectangle([px, py, px + 280, py + 56], radius=28, fill=(30, 41, 59, 230), outline=col, width=2)
        f_p = get_font(FONT_BOLD_PATH, 16)
        draw.text((px + 22, py + 16), p, font=f_p, fill=(255, 255, 255))
        px += 300

    cx, cy, s = 1520, 540, 480
    shield_pts = [
        (cx, cy - s//2),
        (cx + s//2, cy - s//4),
        (cx + int(s*0.42), cy + s//5),
        (cx, cy + s//2),
        (cx - int(s*0.42), cy + s//5),
        (cx - s//2, cy - s//4)
    ]
    draw.polygon(shield_pts, fill=(15, 23, 42, 235), outline=(6, 182, 212, 255), width=3)
    for r in [180, 130, 80]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(59, 130, 246, 90), width=2)
    draw.arc([cx - 80, cy - 50, cx + 80, cy + 50], start=20, end=160, fill=(6, 182, 212, 255), width=6)
    draw.arc([cx - 80, cy - 50, cx + 80, cy + 50], start=200, end=340, fill=(6, 182, 212, 255), width=6)
    draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=(59, 130, 246, 255))

    save_image_to_dirs(canvas, "background_image_1920x1080", AMAZON_DIRS)

def generate_amazon_promo_1280x720():
    # 1280x720 Amazon Header Image
    W, H = 1280, 720
    canvas = draw_gradient_canvas(W, H, (11, 15, 25), (2, 6, 23))
    canvas = canvas.convert('RGBA')
    draw_radial_glow(canvas, 1000, 360, 450, (6, 182, 212), max_alpha=100)
    draw_tech_grid(canvas, grid_size=36, line_color=(30, 41, 59, 45))
    
    draw = ImageDraw.Draw(canvas)
    f_badge = get_font(FONT_BOLD_PATH, 14)
    draw.rounded_rectangle([70, 70, 420, 110], radius=20, fill=(15, 23, 42, 240), outline=(6, 182, 212, 200), width=1)
    draw.text((90, 80), "🔥 FIRE TABLET and FIRE TV OPTIMIZED", font=f_badge, fill=(6, 182, 212))

    f_title = get_font(FONT_BOLD_PATH, 42)
    draw.text((70, 135), "Biometric Duty Attendance\nand Committee Ballots", font=f_title, fill=(255, 255, 255))

    f_sub = get_font(FONT_REG_PATH, 18)
    draw.text((70, 255), "• 100% Secure Local SQLite Database Storage\n• Face and Eye-Blink Liveness Verification\n• 3-Step Duty Sequence (Morning / Evening)\n• Official Court and ICAR Institutional Portals", font=f_sub, fill=(203, 213, 225))

    pills = [("👁️ Blink Verified", (6, 182, 212)), ("💾 Local Storage", (16, 185, 129)), ("📊 CSV Audit", (99, 102, 241))]
    px, py = 70, 480
    for p, col in pills:
        draw.rounded_rectangle([px, py, px + 195, py + 46], radius=23, fill=(30, 41, 59, 230), outline=col, width=1)
        f_p = get_font(FONT_BOLD_PATH, 14)
        draw.text((px + 18, py + 14), p, font=f_p, fill=(255, 255, 255))
        px += 215

    # Right side badge
    cx, cy, s = 1040, 360, 320
    shield_pts = [
        (cx, cy - s//2),
        (cx + s//2, cy - s//4),
        (cx + int(s*0.42), cy + s//5),
        (cx, cy + s//2),
        (cx - int(s*0.42), cy + s//5),
        (cx - s//2, cy - s//4)
    ]
    draw.polygon(shield_pts, fill=(15, 23, 42, 235), outline=(6, 182, 212, 255), width=2)
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(59, 130, 246, 255))

    save_image_to_dirs(canvas, "app_image_1280x720", AMAZON_DIRS)

def generate_firetv_screenshots():
    # 3 High-Res Landscape Screenshots for Fire TV (1920x1080)
    W, H = 1920, 1080
    screens = [
        ("firetv_screenshot_1_console_1920x1080", "Biometric Duty Attendance Console", "Hardware-Aware Eye Blink Liveness and Duty Shift Tracking", (6, 182, 212)),
        ("firetv_screenshot_2_ballots_1920x1080", "Official Committee Ballot Station", "3-Step Workflow: Provisional Voting Finalized by Evening Attendance", (16, 185, 129)),
        ("firetv_screenshot_3_admin_audit_1920x1080", "Enterprise Admin Records and CSV Audit", "100% On-Device SQLite Records with Instant CSV Report Export", (99, 102, 241))
    ]
    
    for filename, title, subtitle, accent_col in screens:
        canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
        canvas = canvas.convert('RGBA')
        draw_radial_glow(canvas, 960, 200, 600, accent_col, max_alpha=90)
        draw_tech_grid(canvas, grid_size=48)
        
        draw = ImageDraw.Draw(canvas)
        # Leanback TV Header
        draw.rectangle([0, 0, W, 110], fill=(2, 6, 23, 255))
        draw.line([(0, 110), (W, 110)], fill=(30, 41, 59, 255), width=2)
        
        f_tv_title = get_font(FONT_BOLD_PATH, 36)
        f_tv_sub = get_font(FONT_REG_PATH, 20)
        draw.text((80, 22), f"🛡️ {title}", font=f_tv_title, fill=(255, 255, 255))
        draw.text((80, 68), subtitle, font=f_tv_sub, fill=(148, 163, 184))
        
        f_badge = get_font(FONT_BOLD_PATH, 16)
        draw.rounded_rectangle([W - 320, 32, W - 80, 80], radius=16, fill=accent_col)
        draw.text((W - 300, 44), "📺 FIRE TV EDITION", font=f_badge, fill=(255, 255, 255))

        # Main TV Dashboard Window (TV Frame)
        dw, dh = 1760, 860
        dx, dy = (W - dw) // 2, 160
        draw.rounded_rectangle([dx, dy, dx + dw, dy + dh], radius=24, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=2)
        
        # Left Panel (User / Shift Details)
        draw.rounded_rectangle([dx + 40, dy + 40, dx + 650, dy + dh - 40], radius=18, fill=(30, 41, 59, 255))
        f_pan_h = get_font(FONT_BOLD_PATH, 24)
        f_pan_t = get_font(FONT_REG_PATH, 17)
        draw.text((dx + 65, dy + 65), "🏛️ Organization and Duty Session", font=f_pan_h, fill=(255, 255, 255))
        draw.text((dx + 65, dy + 110), "Institute: Supreme Court and High Court", font=f_pan_t, fill=(203, 213, 225))
        draw.text((dx + 65, dy + 140), "Presiding Officer: Alex Rivera (MEM-01)", font=f_pan_t, fill=(203, 213, 225))
        draw.text((dx + 65, dy + 170), "Aadhaar Card: 1234-5678-9021", font=f_pan_t, fill=(148, 163, 184))
        draw.text((dx + 65, dy + 200), "Location: Central District HQ (Device GPS)", font=f_pan_t, fill=(148, 163, 184))
        
        draw.line([(dx + 65, dy + 245), (dx + 625, dy + 245)], fill=(51, 65, 85, 255), width=1)
        draw.text((dx + 65, dy + 265), "⚡ 3-Step Duty Sequence Status", font=f_pan_h, fill=(245, 158, 11))
        draw.text((dx + 65, dy + 310), "• Step 1: Morning Shift verified present", font=f_pan_t, fill=(16, 185, 129))
        draw.text((dx + 65, dy + 345), "• Step 2: Provisional Committee Vote cast", font=f_pan_t, fill=(245, 158, 11))
        draw.text((dx + 65, dy + 380), "• Step 3: Evening Shift finalizes all logs", font=f_pan_t, fill=(59, 130, 246))
        
        draw.rounded_rectangle([dx + 65, dy + 440, dx + 625, dy + 550], radius=14, fill=(2, 6, 23, 255), outline=(16, 185, 129, 255), width=2)
        draw.text((dx + 85, dy + 460), "💾 100% On-Device Storage", font=f_pan_h, fill=(16, 185, 129))
        draw.text((dx + 85, dy + 495), "All records saved to local SQLite database.\nZero server required. Total data privacy.", font=f_pan_t, fill=(203, 213, 225))

        # Right Panel: Interactive Feed or Viewfinder
        draw.rounded_rectangle([dx + 690, dy + 40, dx + dw - 40, dy + dh - 40], radius=18, fill=(2, 6, 23, 255), outline=(51, 65, 85, 255), width=1)
        
        if "console" in filename:
            # Biometric scanner card
            vcx, vcy = dx + 1200, dy + 340
            for r in [170, 120, 70]:
                draw.ellipse([vcx - r, vcy - r, vcx + r, vcy + r], outline=(6, 182, 212, 100), width=2)
            draw.arc([vcx - 70, vcy - 45, vcx + 70, vcy + 45], start=20, end=160, fill=(6, 182, 212, 255), width=5)
            draw.arc([vcx - 70, vcy - 45, vcx + 70, vcy + 45], start=200, end=340, fill=(6, 182, 212, 255), width=5)
            draw.ellipse([vcx - 20, vcy - 20, vcx + 20, vcy + 20], fill=(59, 130, 246, 255))
            
            draw.rounded_rectangle([dx + 800, dy + 580, dx + dw - 150, dy + 660], radius=18, fill=(16, 185, 129, 240))
            f_bl = get_font(FONT_BOLD_PATH, 26)
            draw.text((dx + 860, dy + 605), "👁️ Eye Blink Liveness Verified (99.2%)", font=f_bl, fill=(255, 255, 255))
        elif "ballots" in filename:
            # Ballot options
            opts = [
                ("Adv. Priya Sharma", "Senior Council Nominee (Bar Association)", "VOTE CAST (PROVISIONAL)", (16, 185, 129)),
                ("Hon. Justice K. Raman", "Judicial Officer Representative", "SELECT BALLOT", (59, 130, 246)),
                ("Dr. M. S. Venkatesh", "Independent Ethics Auditor", "SELECT BALLOT", (59, 130, 246))
            ]
            oy = dy + 80
            for name, des, btxt, col in opts:
                draw.rounded_rectangle([dx + 720, oy, dx + dw - 70, oy + 180], radius=16, fill=(30, 41, 59, 255), outline=col, width=2)
                draw.text((dx + 750, oy + 25), name, font=f_pan_h, fill=(255, 255, 255))
                draw.text((dx + 750, oy + 65), des, font=f_pan_t, fill=(148, 163, 184))
                draw.rounded_rectangle([dx + 750, oy + 105, dx + 1080, oy + 155], radius=12, fill=col)
                draw.text((dx + 770, oy + 118), btxt, font=get_font(FONT_BOLD_PATH, 16), fill=(255, 255, 255))
                oy += 210
        else:
            # Admin Audit Records
            draw.rounded_rectangle([dx + 720, dy + 65, dx + dw - 70, dy + 180], radius=16, fill=(30, 41, 59, 255))
            draw.text((dx + 750, dy + 85), "📊 Real-Time Duty Audit Metrics", font=f_pan_h, fill=(255, 255, 255))
            draw.text((dx + 750, dy + 125), "Total Records: 128  |  Morning: 64  |  Evening: 64  |  Verified: 128", font=f_pan_t, fill=(16, 185, 129))
            
            # Export CSV button
            draw.rounded_rectangle([dx + 720, dy + 210, dx + 1120, dy + 270], radius=14, fill=(99, 102, 241, 255))
            draw.text((dx + 750, dy + 228), "📥 EXPORT CSV REPORT TO FILE", font=get_font(FONT_BOLD_PATH, 18), fill=(255, 255, 255))
            
            # Record rows
            rec_y = dy + 300
            recs = [
                ("Alex Rivera (MEM-01)", "Morning Shift • Biometric Blink Verified", "09:14 AM"),
                ("Priya Sharma (MEM-02)", "Committee Ballot • Provisional Cast", "11:32 AM"),
                ("Dr. R. K. Sen (MEM-03)", "Morning Shift • Biometric Blink Verified", "09:28 AM"),
                ("K. Venkatesh (MEM-04)", "Evening Shift • Completed and Finalized", "17:05 PM")
            ]
            for rname, rdesc, rtime in recs:
                draw.rounded_rectangle([dx + 720, rec_y, dx + dw - 70, rec_y + 90], radius=12, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=1)
                draw.text((dx + 745, rec_y + 16), rname, font=get_font(FONT_BOLD_PATH, 18), fill=(255, 255, 255))
                draw.text((dx + 745, rec_y + 48), f"{rdesc}  ({rtime})", font=f_pan_t, fill=(148, 163, 184))
                rec_y += 110

        save_image_to_dirs(canvas, filename, AMAZON_DIRS)

def generate_fire_tablet_screenshots():
    # Tablet 1280x800 Landscape Screenshots
    W, H = 1280, 800
    screens = [
        ("fire_tablet_screenshot_1_1280x800", "Biometric Duty Attendance", "Face and Eye-Blink Liveness Verification", (6, 182, 212)),
        ("fire_tablet_screenshot_2_1280x800", "Committee Ballot Voting", "3-Step Workflow with Dual Biometrics", (16, 185, 129)),
        ("fire_tablet_screenshot_3_1280x800", "Admin Records and CSV Audit", "100% On-Device SQLite Records", (99, 102, 241))
    ]
    for filename, title, subtitle, accent in screens:
        canvas = draw_gradient_canvas(W, H, (15, 23, 42), (2, 6, 23))
        canvas = canvas.convert('RGBA')
        draw_radial_glow(canvas, 640, 150, 450, accent, max_alpha=90)
        draw_tech_grid(canvas, grid_size=36)
        draw = ImageDraw.Draw(canvas)
        
        # Header
        draw.rectangle([0, 0, W, 80], fill=(2, 6, 23, 255))
        draw.line([(0, 80), (W, 80)], fill=(30, 41, 59, 255), width=1)
        draw.text((50, 16), f"🛡️ {title}", font=get_font(FONT_BOLD_PATH, 26), fill=(255, 255, 255))
        draw.text((50, 48), subtitle, font=get_font(FONT_REG_PATH, 15), fill=(148, 163, 184))
        
        draw.rounded_rectangle([W - 220, 22, W - 50, 58], radius=14, fill=accent)
        draw.text((W - 205, 30), "FIRE TABLET", font=get_font(FONT_BOLD_PATH, 14), fill=(255, 255, 255))
        
        # Tablet content layout
        draw.rounded_rectangle([50, 110, 500, H - 40], radius=18, fill=(30, 41, 59, 255))
        f_th = get_font(FONT_BOLD_PATH, 18)
        f_tt = get_font(FONT_REG_PATH, 14)
        draw.text((75, 130), "Session and Sequence Overview", font=f_th, fill=(255, 255, 255))
        draw.text((75, 165), "• Alex Rivera (MEM-01)", font=f_tt, fill=(203, 213, 225))
        draw.text((75, 190), "• Supreme Court and High Court", font=f_tt, fill=(203, 213, 225))
        draw.text((75, 215), "• Aadhaar: 1234-5678-9021", font=f_tt, fill=(148, 163, 184))
        
        draw.line([(75, 250), (475, 250)], fill=(51, 65, 85, 255), width=1)
        draw.text((75, 270), "💾 100% On-Device SQLite", font=f_th, fill=(16, 185, 129))
        draw.text((75, 300), "No web server or cloud required.\nEncrypted local audit logging.\nInstant CSV export.", font=f_tt, fill=(203, 213, 225))
        
        # Right panel
        draw.rounded_rectangle([530, 110, W - 50, H - 40], radius=18, fill=(2, 6, 23, 255), outline=(51, 65, 85, 255), width=1)
        if "screenshot_1" in filename:
            vcx, vcy = 870, 360
            for r in [140, 100, 60]:
                draw.ellipse([vcx - r, vcy - r, vcx + r, vcy + r], outline=(6, 182, 212, 100), width=2)
            draw.ellipse([vcx - 20, vcy - 20, vcx + 20, vcy + 20], fill=(59, 130, 246, 255))
            draw.rounded_rectangle([620, 560, 1120, 630], radius=16, fill=(16, 185, 129, 240))
            draw.text((660, 582), "👁️ Eye Blink Liveness Verified! (99.2%)", font=get_font(FONT_BOLD_PATH, 20), fill=(255, 255, 255))
        elif "screenshot_2" in filename:
            b_y = 150
            for cname in ["Adv. Priya Sharma (Bar Council)", "Hon. Justice K. Raman (Judiciary)", "Dr. M. S. Venkatesh (Ethics)"]:
                draw.rounded_rectangle([560, b_y, W - 80, b_y + 110], radius=14, fill=(30, 41, 59, 255), outline=(16, 185, 129), width=2)
                draw.text((585, b_y + 20), cname, font=f_th, fill=(255, 255, 255))
                draw.text((585, b_y + 55), "Provisional Ballot Cast • Finalized on Evening Duty", font=f_tt, fill=(148, 163, 184))
                b_y += 140
        else:
            draw.text((560, 140), "📊 Real-Time Local Duty Logs", font=get_font(FONT_BOLD_PATH, 22), fill=(255, 255, 255))
            draw.rounded_rectangle([560, 180, 860, 230], radius=12, fill=(99, 102, 241, 255))
            draw.text((580, 195), "📥 EXPORT CSV TO STORAGE", font=get_font(FONT_BOLD_PATH, 15), fill=(255, 255, 255))
            ry = 260
            for name, act, t in [("Alex Rivera", "Morning Shift Verified", "09:14 AM"), ("Priya Sharma", "Provisional Ballot Cast", "11:32 AM"), ("K. Venkatesh", "Evening Shift Finalized", "17:05 PM")]:
                draw.rounded_rectangle([560, ry, W - 80, ry + 75], radius=12, fill=(30, 41, 59, 255))
                draw.text((580, ry + 15), name, font=f_th, fill=(255, 255, 255))
                draw.text((580, ry + 42), f"{act} • {t}", font=f_tt, fill=(16, 185, 129))
                ry += 95

        save_image_to_dirs(canvas, filename, AMAZON_DIRS)

if __name__ == "__main__":
    print("==================================================")
    print("GENERATING ACCURATE STORE GRAPHICS FOR BOTH STORES")
    print("Zero Cloud/Sync Mentions - 100% On-Device Verified")
    print("==================================================")
    generate_master_icons()
    print("\n--- Generating Google Play Store Assets ---")
    generate_google_play_feature_graphic()
    generate_play_screenshot_1()
    generate_play_screenshot_2()
    generate_play_screenshot_3()
    generate_play_screenshot_4()
    generate_play_screenshot_5()
    print("\n--- Generating Amazon Appstore and Fire TV Assets ---")
    generate_amazon_background()
    generate_amazon_promo_1280x720()
    generate_firetv_screenshots()
    generate_fire_tablet_screenshots()
    print("\n==================================================")
    print("ALL STORE ASSETS GENERATED FOR BOTH STORES SUCCESSFULLY!")
    print("==================================================")
