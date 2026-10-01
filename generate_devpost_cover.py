import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_devpost_cover():
    WIDTH = 1920
    HEIGHT = 1080

    # 1. Base Dark Canvas
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 14, 23, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
    font_reg = "C:\\Windows\\Fonts\\segoeui.ttf"
    font_semibold = "C:\\Windows\\Fonts\\seguisb.ttf"
    if not os.path.exists(font_semibold):
        font_semibold = font_bold

    def get_font(path, size):
        try:
            return ImageFont.truetype(path, size)
        except:
            return ImageFont.load_default()

    f_hero_badge = get_font(font_bold, 12)
    f_hero_title = get_font(font_bold, 44)
    f_hero_sub = get_font(font_semibold, 18)
    f_desc = get_font(font_reg, 13)
    f_pill = get_font(font_bold, 11)
    f_feature_title = get_font(font_bold, 14)
    f_feature_desc = get_font(font_reg, 11)
    f_tech_badge = get_font(font_bold, 11)
    f_phone_title = get_font(font_bold, 12)

    # Background Tech Grid
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=(18, 24, 38, 110), width=1)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=(18, 24, 38, 110), width=1)

    # Ambient Glows (Indigo Top-Left, Cyan Right)
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(500, 0, -25):
        alpha = int(24 * (1 - r / 500.0))
        glow_draw.ellipse([-150 - r, -100 - r, 600 + r, 500 + r], fill=(79, 70, 229, alpha))
        glow_draw.ellipse([1200 - r, 300 - r, 2100 + r, 1200 + r], fill=(6, 182, 212, int(alpha * 0.7)))
        glow_draw.ellipse([900 - r, -100 - r, 1800 + r, 700 + r], fill=(139, 92, 246, int(alpha * 0.5)))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # ==================== LEFT SIDE: PRESENTATION and VALUE PROP ====================
    left_x = 75
    cur_y = 75

    # Devpost Category Banner Pill
    badge_txt = "[ DEVPOST HACKATHON SHOWCASE • ENTERPRISE TRACK ]"
    bbox = f_hero_badge.getbbox(badge_txt)
    bw = bbox[2] - bbox[0] + 32
    draw.rounded_rectangle([left_x, cur_y, left_x + bw, cur_y + 30], radius=8, fill=(30, 27, 75, 240), outline=(99, 102, 241), width=1)
    draw.text((left_x + 16, cur_y + 6), badge_txt, fill=(165, 180, 252), font=f_hero_badge)

    cur_y += 50
    # Hero Title
    title_text = "AttendanceApp"
    draw.text((left_x, cur_y), title_text, fill=(255, 255, 255), font=f_hero_title)

    # Sub-Pill next to title
    icon_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\play_store_icon_512x512.png"
    if os.path.exists(icon_path):
        app_icon = Image.open(icon_path).convert("RGBA").resize((56, 56), Image.Resampling.LANCZOS)
        # Rounded icon mask
        mask = Image.new("L", (56, 56), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, 56, 56], radius=12, fill=255)
        img.paste(app_icon, (left_x + 360, cur_y + 6), mask)

    cur_y += 66
    # Tagline
    tagline = "Institutional Attendance, Biometric Liveness and Quorum Voting System"
    draw.text((left_x, cur_y), tagline, fill=(129, 140, 248), font=f_hero_sub)

    cur_y += 48
    # Description paragraph
    desc = "A proctor-grade mobile platform designed for high-security legislative bodies, judicial benches,\nand statutory commissions. Enforces physical presence with anti-spoof AI, locks quorum ballots,\nand guarantees zero data leakage through an air-gapped, 100% on-device SQLite architecture."
    draw.text((left_x, cur_y), desc, fill=(148, 163, 184), font=f_desc)

    cur_y += 88
    # 5 High-Impact Feature Cards (Left Column)
    features = [
        ("01", "CameraX Eye-Blink AI Liveness", "MLKit computer vision calculates real-time Eye Aspect Ratio (EAR) to detect natural blinks, blocking static photos, video replay, and deepfake masks.", (6, 182, 212)),
        ("02", "Strict 3-Step Sequence Protocol", "Step 1 Morning Entry -> Step 2 Voting Station -> Step 3 Evening Seal. Each step strictly locked until prior verification passes.", (99, 102, 241)),
        ("03", "Statutory Quorum and Resolution Ballots", "Real-time presence tracking calculates voting quorum. Members cast verified votes; abandonment prevention blocks premature exit.", (16, 185, 129)),
        ("04", "100% Offline SQLite Architecture", "Zero external server or cloud dependency. Direct cryptographic database records with 1-click on-device CSV export for audit.", (245, 158, 11)),
        ("05", "RevenueCat Subscriptions and Expiration Warnings", "Dual Google Play and Amazon Appstore monetization with 7-Day trial countdown timers, warning alerts (<=2 days), and judge demo sandbox.", (236, 72, 153))
    ]

    card_w = 820
    for num, f_title, f_sub, accent in features:
        draw.rounded_rectangle([left_x, cur_y, left_x + card_w, cur_y + 68], radius=10, fill=(17, 24, 39, 230), outline=(30, 41, 59), width=1)
        # Accent left indicator
        draw.line([(left_x + 3, cur_y + 12), (left_x + 3, cur_y + 56)], fill=accent, width=3)
        # Number badge
        draw.rounded_rectangle([left_x + 16, cur_y + 14, left_x + 40, cur_y + 36], radius=6, fill=(30, 41, 59), outline=accent, width=1)
        draw.text((left_x + 22, cur_y + 17), num, fill=accent, font=f_hero_badge)
        # Title
        draw.text((left_x + 50, cur_y + 13), f_title, fill=(241, 245, 249), font=f_feature_title)
        # Desc
        draw.text((left_x + 50, cur_y + 35), f_sub, fill=(148, 163, 184), font=f_feature_desc)
        cur_y += 78

    # Tech Stack Badges at Bottom Left
    cur_y += 10
    techs = [
        ("Kotlin 1.9", (99, 102, 241)),
        ("Jetpack CameraX", (6, 182, 212)),
        ("Google MLKit AI", (16, 185, 129)),
        ("Room SQLite DB", (245, 158, 11)),
        ("RevenueCat SDK", (236, 72, 153)),
        ("Fire TV and Tablet", (139, 92, 246)),
        ("Play Store Ready", (34, 197, 94))
    ]
    tx = left_x
    for name, col in techs:
        tb = f_tech_badge.getbbox(name)
        tw = tb[2] - tb[0] + 20
        draw.rounded_rectangle([tx, cur_y, tx + tw, cur_y + 26], radius=6, fill=(17, 24, 39, 220), outline=col, width=1)
        draw.text((tx + 10, cur_y + 5), name, fill=col, font=f_tech_badge)
        tx += tw + 10

    # ==================== RIGHT SIDE: DEVICE MOCKUP SHOWCASE ====================
    # We compose 3 realistic device mockups from the real app screenshots!
    # Background mockup: Tablet / Admin Portal Console (centered-behind)
    # Foreground Left mockup: Phone with Biometric Face Liveness Scanning
    # Foreground Right mockup: Phone with Quorum Voting Station

    p1_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_1_biometric_1080x1920.png"
    p2_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_2_sequence_1080x1920.png"
    p3_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_3_voting_1080x1920.png"
    tv_path = r"C:\AttendanceApp_RevenueCat\amazon_store_assets\firetv_screenshot_3_admin_audit_1920x1080.png"

    # Function to create a phone frame around a screenshot
    def create_phone_mockup(screen_path, target_w, target_h, title_label, accent_color):
        screen = Image.open(screen_path).convert("RGBA")
        screen_resized = screen.resize((target_w - 24, target_h - 48), Image.Resampling.LANCZOS)

        phone = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(phone)

        # Phone outer chassis
        p_draw.rounded_rectangle([0, 0, target_w, target_h], radius=28, fill=(15, 23, 42, 255), outline=accent_color, width=2)
        # Inner bezel
        p_draw.rounded_rectangle([8, 8, target_w - 8, target_h - 8], radius=22, fill=(30, 41, 59, 255))
        # Paste screen
        phone.paste(screen_resized, (12, 24))
        # Dynamic Island / Camera notch
        p_draw.rounded_rectangle([target_w//2 - 32, 12, target_w//2 + 32, 20], radius=4, fill=(10, 14, 23, 255))
        # Home indicator line
        p_draw.rounded_rectangle([target_w//2 - 40, target_h - 14, target_w//2 + 40, target_h - 10], radius=2, fill=(148, 163, 184, 180))

        return phone

    # Back tablet / Fire TV mockup
    if os.path.exists(tv_path):
        tv_img = Image.open(tv_path).convert("RGBA")
        tv_w = 880
        tv_h = 495
        tv_resized = tv_img.resize((tv_w - 20, tv_h - 20), Image.Resampling.LANCZOS)
        tv_frame = Image.new("RGBA", (tv_w, tv_h), (0, 0, 0, 0))
        tv_draw = ImageDraw.Draw(tv_frame)
        tv_draw.rounded_rectangle([0, 0, tv_w, tv_h], radius=16, fill=(15, 23, 42, 240), outline=(245, 158, 11, 160), width=2)
        tv_frame.paste(tv_resized, (10, 10))

        # Position tablet on upper-right
        tv_x = 970
        tv_y = 110
        # Shadow
        shadow = Image.new("RGBA", (tv_w + 40, tv_h + 40), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.rounded_rectangle([15, 15, tv_w + 25, tv_h + 25], radius=20, fill=(0, 0, 0, 160))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        img.paste(shadow, (tv_x - 15, tv_y - 15), shadow)
        img.paste(tv_frame, (tv_x, tv_y), tv_frame)

        # Label pill above tablet
        draw.rounded_rectangle([tv_x + 20, tv_y - 14, tv_x + 290, tv_y + 12], radius=6, fill=(245, 158, 11), outline=(255, 255, 255), width=1)
        draw.text((tv_x + 30, tv_y - 10), "EXECUTIVE ADMIN and AUDIT PORTAL", fill=(15, 23, 42), font=f_phone_title)

    # Foreground Phone 1: Biometric Face Liveness (Left)
    phone_w = 390
    phone_h = 690
    if os.path.exists(p1_path):
        phone1 = create_phone_mockup(p1_path, phone_w, phone_h, "Eye-Blink AI Liveness", (6, 182, 212))
        p1_x = 1000
        p1_y = 330
        # Shadow
        p1_shadow = Image.new("RGBA", (phone_w + 40, phone_h + 40), (0, 0, 0, 0))
        ps_draw = ImageDraw.Draw(p1_shadow)
        ps_draw.rounded_rectangle([10, 10, phone_w + 30, phone_h + 30], radius=34, fill=(0, 0, 0, 200))
        p1_shadow = p1_shadow.filter(ImageFilter.GaussianBlur(16))
        img.paste(p1_shadow, (p1_x - 10, p1_y - 10), p1_shadow)
        img.paste(phone1, (p1_x, p1_y), phone1)

        # Floating status badge on Phone 1
        draw.rounded_rectangle([p1_x + 30, p1_y + phone_h - 40, p1_x + 360, p1_y + phone_h - 8], radius=8, fill=(8, 51, 68, 240), outline=(6, 182, 212), width=1)
        draw.text((p1_x + 45, p1_y + phone_h - 34), "EYE-BLINK LIVENESS: [VERIFIED]", fill=(103, 232, 249), font=f_phone_title)

    # Foreground Phone 2: Quorum Voting Station (Right)
    if os.path.exists(p3_path):
        phone2 = create_phone_mockup(p3_path, phone_w, phone_h, "Quorum Voting", (16, 185, 129))
        p2_x = 1440
        p2_y = 330
        # Shadow
        p2_shadow = Image.new("RGBA", (phone_w + 40, phone_h + 40), (0, 0, 0, 0))
        ps_draw = ImageDraw.Draw(p2_shadow)
        ps_draw.rounded_rectangle([10, 10, phone_w + 30, phone_h + 30], radius=34, fill=(0, 0, 0, 200))
        p2_shadow = p2_shadow.filter(ImageFilter.GaussianBlur(16))
        img.paste(p2_shadow, (p2_x - 10, p2_y - 10), p2_shadow)
        img.paste(phone2, (p2_x, p2_y), phone2)

        # Floating status badge on Phone 2
        draw.rounded_rectangle([p2_x + 30, p2_y + phone_h - 40, p2_x + 360, p2_y + phone_h - 8], radius=8, fill=(6, 78, 59, 240), outline=(16, 185, 129), width=1)
        draw.text((p2_x + 50, p2_y + phone_h - 34), "QUORUM VOTE: [CONFIRMED]", fill=(110, 231, 183), font=f_phone_title)

    # Save to all relevant project locations
    out_paths = [
        r"C:\AttendanceApp_RevenueCat\devpost_cover_image.png",
        r"F:\AttendanceApp_RevenueCat\devpost_cover_image.png",
        r"C:\Users\HP\Desktop\attendance_store_assets\devpost_cover_image.png",
        r"C:\AttendanceApp_RevenueCat\google_play_assets\devpost_cover_image.png",
        r"C:\AttendanceApp_RevenueCat\amazon_store_assets\devpost_cover_image.png",
        r"C:\Users\HP\.gemini\antigravity-cli\brain\4515bfce-4739-4f4f-95c0-f93f8477fd2f\devpost_cover_image.png"
    ]

    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, "PNG")
        print(f"Saved Devpost Cover: {p}")

if __name__ == "__main__":
    create_devpost_cover()
