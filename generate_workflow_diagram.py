import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_workflow_diagram():
    WIDTH = 1920
    HEIGHT = 1080

    # 1. Canvas setup
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 14, 23, 255))
    draw = ImageDraw.Draw(img)

    # 2. Fonts
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

    f_super_title = get_font(font_bold, 36)
    f_sub = get_font(font_reg, 15)
    f_header_pill = get_font(font_bold, 11)
    f_badge = get_font(font_bold, 11)
    f_step_num = get_font(font_bold, 10)
    f_card_title = get_font(font_bold, 18)
    f_card_sub = get_font(font_semibold, 12)
    f_item_title = get_font(font_bold, 13)
    f_item_desc = get_font(font_reg, 11)
    f_status = get_font(font_bold, 11)
    f_bottom_title = get_font(font_bold, 17)
    f_footer = get_font(font_reg, 12)

    # 3. Background Tech Grid
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=(17, 24, 39, 140), width=1)
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=(17, 24, 39, 140), width=1)

    # Ambient Top Indigo Glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(450, 0, -25):
        alpha = int(22 * (1 - r / 450.0))
        glow_draw.ellipse(
            [WIDTH//2 - r*2, -180 - r, WIDTH//2 + r*2, 260 + r],
            fill=(79, 70, 229, alpha)
        )
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    def draw_card(x1, y1, x2, y2, radius, fill_color, border_color, accent_color=None):
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill_color)
        draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=border_color, width=1)
        # Top glowing accent line
        if accent_color:
            draw.line([(x1 + radius, y1), (x2 - radius, y1)], fill=accent_color, width=3)

    def draw_pill(text, cx, cy, bg_color, text_color, font=f_badge, pad_x=12, pad_y=5):
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x1 = cx - tw // 2 - pad_x
        y1 = cy - th // 2 - pad_y
        x2 = cx + tw // 2 + pad_x
        y2 = cy + th // 2 + pad_y
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=bg_color)
        draw.text((cx - tw // 2, cy - th // 2 - 1), text, fill=text_color, font=font)

    def draw_left_pill(text, x, y, bg_color, text_color, font=f_badge, pad_x=10, pad_y=4):
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x2 = x + tw + pad_x * 2
        y2 = y + th + pad_y * 2
        draw.rounded_rectangle([x, y, x2, y2], radius=6, fill=bg_color)
        draw.text((x + pad_x, y + pad_y - 1), text, fill=text_color, font=font)
        return x2

    # ==================== TOP HEADER SECTION ====================
    top_y = 26
    draw_pill("INSTITUTIONAL GRADE • ARCHITECTURAL WORKFLOW", WIDTH // 2, top_y + 12, (30, 27, 75, 240), (165, 180, 252), f_header_pill, 14, 5)

    title_text = "AttendanceApp and Quorum Voting System"
    tb = f_super_title.getbbox(title_text)
    draw.text(((WIDTH - (tb[2] - tb[0])) // 2, top_y + 36), title_text, fill=(255, 255, 255), font=f_super_title)

    sub_text = "End-to-End Operational Workflow • Biometric Eye-Blink Liveness • 100% Offline SQLite • RevenueCat Multi-Store Subscriptions"
    sb = f_sub.getbbox(sub_text)
    draw.text(((WIDTH - (sb[2] - sb[0])) // 2, top_y + 83), sub_text, fill=(148, 163, 184), font=f_sub)

    # Header feature badges (Clean tech text tags)
    top_badges = [
        ("[LOCAL-FIRST]", "100% Offline SQLite", (16, 185, 129, 35), (52, 211, 153)),
        ("[AI VISION]", "Eye-Blink Liveness", (6, 182, 212, 35), (103, 232, 249)),
        ("[SECURITY]", "Strict 3-Step Sequence", (99, 102, 241, 35), (165, 180, 252)),
        ("[PARLIAMENT]", "Quorum Presence Lock", (245, 158, 11, 35), (252, 211, 77)),
        ("[COMMERCE]", "RevenueCat Dual Store", (236, 72, 153, 35), (249, 168, 212)),
        ("[LEANBACK]", "Fire TV and Tablet Ready", (139, 92, 246, 35), (196, 181, 253))
    ]

    total_badge_w = 0
    badge_widths = []
    for tag, label, bg, tc in top_badges:
        txt = f"{tag} {label}"
        bw = f_badge.getbbox(txt)[2] - f_badge.getbbox(txt)[0] + 24
        badge_widths.append((txt, bw, bg, tc))
        total_badge_w += bw
    total_badge_w += 12 * (len(top_badges) - 1)

    cur_x = (WIDTH - total_badge_w) // 2
    for txt, bw, bg, tc in badge_widths:
        draw.rounded_rectangle([cur_x, top_y + 114, cur_x + bw, top_y + 140], radius=6, fill=bg, outline=tc, width=1)
        draw.text((cur_x + 12, top_y + 119), txt, fill=tc, font=f_badge)
        cur_x += bw + 12

    # ==================== MAIN 4-STAGE PIPELINE (TOP TIER) ====================
    card_w = 415
    gap = 42
    start_x = (WIDTH - (card_w * 4 + gap * 3)) // 2
    row1_y = 178
    row1_h = 492

    stages = [
        {
            "tag": "STAGE 1",
            "tag_bg": (99, 102, 241, 230),
            "tag_color": (255, 255, 255),
            "accent": (129, 140, 248),
            "border": (99, 102, 241, 150),
            "title": "Organization and Identity",
            "sub": "Multi-Tenant Selection and Session Setup",
            "status_text": "READY: Awaiting Morning Check-In",
            "status_bg": (30, 27, 75),
            "status_color": (165, 180, 252),
            "items": [
                ("01", "Institutional Org Routing", "Select jurisdiction: Supreme Court, High Court, Election Commission, Bar Council, or custom state entity."),
                ("02", "Role-Based Privilege Dispatch", "Dispatches to Member Portal (Duty execution, Voting) or Admin Portal (Audits, Shift alterations, CSV export)."),
                ("03", "Dynamic Shift Window Sync", "Calculates morning (09:00 - 13:00) and evening (16:00 - 19:00) strict duty thresholds dynamically."),
                ("04", "RevenueCat Subscription Check", "Queries on-device cached entitlement and 7-Day trial countdown timer before starting shift duty.")
            ]
        },
        {
            "tag": "STAGE 2 • STEP 1",
            "tag_bg": (6, 182, 212, 230),
            "tag_color": (15, 23, 42),
            "accent": (34, 211, 238),
            "border": (6, 182, 212, 150),
            "title": "Morning Check-In",
            "sub": "Facial Liveness and Geofencing Verification",
            "status_text": "PASSED: Step 1 Duty Record Sealed",
            "status_bg": (8, 51, 68),
            "status_color": (103, 232, 249),
            "items": [
                ("01", "CameraX Eye-Blink AI Analysis", "Google MLKit analyzes live Eye Aspect Ratio (EAR). Requires confirmed blinks to block static photos/screens."),
                ("02", "Precise Geofence GPS Lock", "Device GPS validated against registered institution perimeter (<50m). Rejects off-site attempts."),
                ("03", "Shift Window Time Validation", "Ensures member is checking in within active morning duty hours before allowing sequence progression."),
                ("04", "Immutable Local SQLite Commit", "Commits encrypted check-in log with timestamp and nature-of-work tag to on-device Room database.")
            ]
        },
        {
            "tag": "STAGE 3 • STEP 2",
            "tag_bg": (16, 185, 129, 230),
            "tag_color": (15, 23, 42),
            "accent": (52, 211, 153),
            "border": (16, 185, 129, 150),
            "title": "Quorum and Voting Station",
            "sub": "Legislative Ballots and Presence Locking",
            "status_text": "CONFIRMED: Quorum Vote Cast and Locked",
            "status_bg": (6, 78, 59),
            "status_color": (110, 231, 183),
            "items": [
                ("01", "Sequence-Enforced Unlock", "Voting station strictly locked until Step 1 Morning Check-in is fully validated and logged."),
                ("02", "Secret Ballot and Resolutions", "Members cast Yes / No / Abstain ballots on active parliamentary topics and assembly motions."),
                ("03", "Real-Time Quorum Tracking", "Tallies attending voting members to verify legal quorum compliance for valid proceedings."),
                ("04", "Abandonment Sentinel Protection", "Enforces voting before checkout; attempts to exit without voting trigger discrepancy flags.")
            ]
        },
        {
            "tag": "STAGE 4 • STEP 3",
            "tag_bg": (168, 85, 247, 230),
            "tag_color": (255, 255, 255),
            "accent": (192, 132, 252),
            "border": (168, 85, 247, 150),
            "title": "Evening Check-Out and Seal",
            "sub": "Duty Verification and Final Record Lock",
            "status_text": "SEALED: Session Finalized and Tamper-Proof",
            "status_bg": (59, 7, 100),
            "status_color": (216, 180, 254),
            "items": [
                ("01", "Secondary Biometric Verification", "Mandatory secondary eye-blink liveness capture validates physical presence at evening departure."),
                ("02", "Shift Duration Consolidation", "Correlates morning entry, evening departure, vote confirmation, and net verified duty hours."),
                ("03", "Cryptographic Record Lock", "Seals record in SQLite Room DB into immutable read-only state, preventing tampering."),
                ("04", "Automated Discrepancy Evaluator", "Flags late departures, skipped votes, or short shifts automatically for administrative audit.")
            ]
        }
    ]

    for idx, s in enumerate(stages):
        cx1 = start_x + idx * (card_w + gap)
        cy1 = row1_y
        cx2 = cx1 + card_w
        cy2 = cy1 + row1_h

        # Card container
        draw_card(cx1, cy1, cx2, cy2, 12, (17, 24, 39, 240), s["border"], s["accent"])

        # Tag
        draw_left_pill(s["tag"], cx1 + 18, cy1 + 18, s["tag_bg"], s["tag_color"], f_badge, 10, 4)

        # Title and Subtitle
        draw.text((cx1 + 18, cy1 + 50), s["title"], fill=(255, 255, 255), font=f_card_title)
        draw.text((cx1 + 18, cy1 + 75), s["sub"], fill=s["accent"], font=f_card_sub)
        draw.line([(cx1 + 18, cy1 + 96), (cx2 - 18, cy1 + 96)], fill=(30, 41, 59, 200), width=1)

        # 4 Items with numbered pills
        item_y = cy1 + 110
        for num, title, desc in s["items"]:
            # Draw numbered bullet pill
            draw.rounded_rectangle([cx1 + 18, item_y + 1, cx1 + 38, item_y + 19], radius=4, fill=(30, 41, 59, 255), outline=s["accent"], width=1)
            draw.text((cx1 + 22, item_y + 3), num, fill=s["accent"], font=f_step_num)

            # Title
            draw.text((cx1 + 46, item_y + 1), title, fill=(241, 245, 249), font=f_item_title)

            # Wrapped description
            words = desc.split(" ")
            lines = []
            curr = []
            for w in words:
                test = " ".join(curr + [w])
                if len(test) < 42:
                    curr.append(w)
                else:
                    lines.append(" ".join(curr))
                    curr = [w]
            if curr:
                lines.append(" ".join(curr))

            desc_y = item_y + 20
            for l in lines[:3]:
                draw.text((cx1 + 46, desc_y), l, fill=(148, 163, 184), font=f_item_desc)
                desc_y += 16

            item_y += 76

        # Bottom status pill
        draw.rounded_rectangle([cx1 + 18, cy2 - 42, cx2 - 18, cy2 - 16], radius=6, fill=s["status_bg"], outline=s["border"], width=1)
        draw.text((cx1 + 28, cy2 - 36), s["status_text"], fill=s["status_color"], font=f_status)

        # Connecting Vector Arrow between cards
        if idx < 3:
            arrow_cx = cx2 + gap // 2
            arrow_cy = cy1 + row1_h // 2
            # Circle
            draw.ellipse([arrow_cx - 16, arrow_cy - 16, arrow_cx + 16, arrow_cy + 16], fill=(17, 24, 39, 255), outline=(6, 182, 212, 180), width=1)
            # Clean filled chevron triangle pointing right
            draw.polygon([
                (arrow_cx - 4, arrow_cy - 7),
                (arrow_cx + 5, arrow_cy),
                (arrow_cx - 4, arrow_cy + 7)
            ], fill=(34, 211, 238))
            draw_pill("NEXT", arrow_cx, arrow_cy + 26, (15, 23, 42, 220), (148, 163, 184), f_step_num, 6, 2)

    # ==================== BOTTOM 2 ARCHITECTURE TIERS ====================
    bot_y = 692
    bot_h = 328
    bot_w = (WIDTH - (start_x * 2 + gap)) // 2

    # Bottom Left: Admin Portal and Audit Center
    bx1 = start_x
    bx2 = bx1 + bot_w
    draw_card(bx1, bot_y, bx2, bot_y + bot_h, 12, (17, 24, 39, 240), (245, 158, 11, 140), (245, 158, 11))

    draw_left_pill("EXECUTIVE MANAGEMENT", bx1 + 22, bot_y + 18, (245, 158, 11, 230), (15, 23, 42), f_badge, 10, 4)
    draw.text((bx1 + 22, bot_y + 50), "Admin and Audit Intelligence Center", fill=(255, 255, 255), font=f_bottom_title)
    draw.text((bx1 + 22, bot_y + 74), "100% Local SQLite • Tamper-Evident Audit Trails • DPAD / Leanback TV Support", fill=(251, 191, 36), font=f_card_sub)
    draw.line([(bx1 + 22, bot_y + 94), (bx2 - 22, bot_y + 94)], fill=(30, 41, 59, 200), width=1)

    admin_items = [
        ("01", "Real-Time Multi-Filter Search", "Search by Aadhaar number, member code, full name, shift status, or calendar date with instant sub-millisecond SQLite queries."),
        ("02", "Official Occasion and Assembly Tagging", "Designate special sittings: National Holidays, Emergency Assembly, Budget Sessions, or Tribunal Sittings across records."),
        ("03", "Discrepancy Resolution and Remark Override", "Detects abandonment, late morning check-ins, and early evening departures with official administrative override notes."),
        ("04", "Direct On-Device CSV Export", "Generates compliant audit spreadsheets stored strictly on local device storage—zero external cloud dependency or data leak.")
    ]
    ay = bot_y + 106
    for num, title, desc in admin_items:
        draw.rounded_rectangle([bx1 + 22, ay + 1, bx1 + 42, ay + 19], radius=4, fill=(30, 41, 59, 255), outline=(245, 158, 11), width=1)
        draw.text((bx1 + 26, ay + 3), num, fill=(245, 158, 11), font=f_step_num)
        draw.text((bx1 + 50, ay + 1), title, fill=(241, 245, 249), font=f_item_title)
        draw.text((bx1 + 50, ay + 19), desc, fill=(148, 163, 184), font=f_item_desc)
        ay += 52

    # Bottom Right: RevenueCat Monetization and Trial Safeguards
    rx1 = bx2 + gap
    rx2 = rx1 + bot_w
    draw_card(rx1, bot_y, rx2, bot_y + bot_h, 12, (17, 24, 39, 240), (236, 72, 153, 140), (236, 72, 153))

    draw_left_pill("MONETIZATION and TRIALS", rx1 + 22, bot_y + 18, (236, 72, 153, 230), (255, 255, 255), f_badge, 10, 4)
    draw.text((rx1 + 22, bot_y + 50), "RevenueCat Multi-Store and Trial Safeguards", fill=(255, 255, 255), font=f_bottom_title)
    draw.text((rx1 + 22, bot_y + 74), "Dual Flavors: Google Play Store + Amazon Appstore • Live Expiration Alerts", fill=(244, 114, 182), font=f_card_sub)
    draw.line([(rx1 + 22, bot_y + 94), (rx2 - 22, bot_y + 94)], fill=(30, 41, 59, 200), width=1)

    rev_items = [
        ("01", "7-Day Free Trial Autonomous Countdown", "Autonomous local timer tracks remaining days with continuous in-app countdown badges across dashboard cards."),
        ("02", "Proactive Expiration Warnings (<=2 Days)", "Triggers high-visibility warning banners and alert toasts when <=2 days remain, preventing unexpected service interruption."),
        ("03", "Graceful Expiration Sentinel", "Upon 7-day lapse, automatically revokes Pro privileges and displays an actionable upgrade dialog leading to Paywall."),
        ("04", "Judge and Evaluator Bypass Mode", "Accepts promo codes (JUDGE2026, REVENUECAT) and features offline demo sandbox mode for test evaluation without billing.")
    ]
    ry = bot_y + 106
    for num, title, desc in rev_items:
        draw.rounded_rectangle([rx1 + 22, ry + 1, rx1 + 42, ry + 19], radius=4, fill=(30, 41, 59, 255), outline=(236, 72, 153), width=1)
        draw.text((rx1 + 26, ry + 3), num, fill=(236, 72, 153), font=f_step_num)
        draw.text((rx1 + 50, ry + 1), title, fill=(241, 245, 249), font=f_item_title)
        draw.text((rx1 + 50, ry + 19), desc, fill=(148, 163, 184), font=f_item_desc)
        ry += 52

    # ==================== FOOTER ====================
    foot_text = "Built with Kotlin 1.9 • Android Jetpack • Google CameraX and MLKit • Room SQLite Database • RevenueCat Purchases SDK • Amazon Appstore and Google Play Ready"
    fb = f_footer.getbbox(foot_text)
    draw.text(((WIDTH - (fb[2] - fb[0])) // 2, 1045), foot_text, fill=(100, 116, 139), font=f_footer)

    # Save to all target locations
    out_paths = [
        r"C:\AttendanceApp_RevenueCat\workflow_diagram.png",
        r"F:\AttendanceApp_RevenueCat\workflow_diagram.png",
        r"C:\Users\HP\Desktop\attendance_store_assets\workflow_diagram.png",
        r"C:\AttendanceApp_RevenueCat\google_play_assets\workflow_diagram.png",
        r"C:\AttendanceApp_RevenueCat\amazon_store_assets\workflow_diagram.png",
        r"C:\Users\HP\.gemini\antigravity-cli\brain\4515bfce-4739-4f4f-95c0-f93f8477fd2f\workflow_diagram.png"
    ]

    for p in out_paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
            img.save(p, "PNG")
            print(f"Saved: {p}")
        except Exception as e:
            print(f"Notice: skipped locked path {p}: {e}")

if __name__ == "__main__":
    create_workflow_diagram()
