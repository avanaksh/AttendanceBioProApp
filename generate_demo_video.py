import os
import sys
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

def generate_video():
    WIDTH = 1920
    HEIGHT = 1080
    FPS = 24
    DURATION_SEC = 120  # Exactly 2 minutes
    TOTAL_FRAMES = FPS * DURATION_SEC  # 2880 frames

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    out_mp4 = r"C:\AttendanceApp_RevenueCat\attendance_app_2min_demo.mp4"
    print(f"Using FFmpeg: {ffmpeg_exe}")
    print(f"Target Output: {out_mp4}")
    print(f"Total Frames: {TOTAL_FRAMES} (120 seconds @ 24 fps)")

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

    f_title = get_font(font_bold, 36)
    f_sub = get_font(font_semibold, 16)
    f_card_title = get_font(font_bold, 18)
    f_card_sub = get_font(font_semibold, 12)
    f_item_title = get_font(font_bold, 13)
    f_item_desc = get_font(font_reg, 11)
    f_badge = get_font(font_bold, 11)
    f_num = get_font(font_bold, 10)
    f_status = get_font(font_bold, 12)
    f_timer = get_font(font_bold, 13)

    # Preload Screenshots
    p1_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_1_biometric_1080x1920.png"
    p2_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_2_sequence_1080x1920.png"
    p3_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_3_voting_1080x1920.png"
    p4_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\phone_screenshot_4_organizations_1080x1920.png"
    tv_path = r"C:\AttendanceApp_RevenueCat\amazon_store_assets\firetv_screenshot_3_admin_audit_1920x1080.png"
    icon_path = r"C:\AttendanceApp_RevenueCat\google_play_assets\play_store_icon_512x512.png"

    def load_scaled_img(path, w, h):
        if os.path.exists(path):
            im = Image.open(path).convert("RGBA")
            return im.resize((w, h), Image.Resampling.LANCZOS)
        return None

    # Pre-render phone mockups
    def create_mockup(screen_img, pw=440, ph=780, accent=(99, 102, 241)):
        m = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        m_draw = ImageDraw.Draw(m)
        m_draw.rounded_rectangle([0, 0, pw, ph], radius=32, fill=(15, 23, 42, 255), outline=accent, width=2)
        m_draw.rounded_rectangle([8, 8, pw - 8, ph - 8], radius=26, fill=(30, 41, 59, 255))
        if screen_img:
            s_resized = screen_img.resize((pw - 24, ph - 52), Image.Resampling.LANCZOS)
            m.paste(s_resized, (12, 26))
        m_draw.rounded_rectangle([pw//2 - 36, 12, pw//2 + 36, 22], radius=5, fill=(10, 14, 23, 255))
        m_draw.rounded_rectangle([pw//2 - 45, ph - 16, pw//2 + 45, ph - 12], radius=2, fill=(148, 163, 184, 180))
        return m

    raw_p1 = Image.open(p1_path).convert("RGBA") if os.path.exists(p1_path) else None
    raw_p2 = Image.open(p2_path).convert("RGBA") if os.path.exists(p2_path) else None
    raw_p3 = Image.open(p3_path).convert("RGBA") if os.path.exists(p3_path) else None
    raw_p4 = Image.open(p4_path).convert("RGBA") if os.path.exists(p4_path) else None
    raw_tv = Image.open(tv_path).convert("RGBA") if os.path.exists(tv_path) else None
    raw_icon = Image.open(icon_path).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS) if os.path.exists(icon_path) else None

    mockup_p1 = create_mockup(raw_p1, 440, 780, (6, 182, 212))
    mockup_p2 = create_mockup(raw_p2, 440, 780, (168, 85, 247))
    mockup_p3 = create_mockup(raw_p3, 440, 780, (16, 185, 129))
    mockup_p4 = create_mockup(raw_p4, 440, 780, (99, 102, 241))

    # Pre-render Shadow
    shadow_img = Image.new("RGBA", (480, 820), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_img)
    s_draw.rounded_rectangle([15, 15, 465, 805], radius=36, fill=(0, 0, 0, 190))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(16))

    # Pre-render Grid Background
    base_bg = Image.new("RGBA", (WIDTH, HEIGHT), (10, 14, 23, 255))
    bg_draw = ImageDraw.Draw(base_bg)
    for y in range(0, HEIGHT, 40):
        bg_draw.line([(0, y), (WIDTH, y)], fill=(18, 24, 38, 120), width=1)
    for x in range(0, WIDTH, 40):
        bg_draw.line([(x, 0), (x, HEIGHT)], fill=(18, 24, 38, 120), width=1)

    # Ambient Top Glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    for r in range(450, 0, -25):
        alpha = int(22 * (1 - r / 450.0))
        g_draw.ellipse([WIDTH//2 - r*2, -180 - r, WIDTH//2 + r*2, 260 + r], fill=(79, 70, 229, alpha))
    base_bg = Image.alpha_composite(base_bg, glow)

    # Start FFmpeg subprocess streaming via stdin
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        out_mp4
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    # Storyboard Scenes Definition (Total 120 seconds):
    # Scene 1: 0 - 12s (12s = 288 frames) -> Intro and App Overview
    # Scene 2: 12 - 28s (16s = 384 frames) -> Multi-Tenant Setup and Shift Windows
    # Scene 3: 28 - 48s (20s = 480 frames) -> Step 1: Morning Check-in and Eye-Blink AI
    # Scene 4: 48 - 68s (20s = 480 frames) -> Step 2: Quorum and Voting Station
    # Scene 5: 68 - 88s (20s = 480 frames) -> Step 3: Evening Checkout and Record Seal
    # Scene 6: 88 - 104s (16s = 384 frames) -> Admin Portal and Direct CSV Export
    # Scene 7: 104 - 116s (12s = 288 frames) -> RevenueCat Subscriptions and Warning Sentinel
    # Scene 8: 116 - 120s (4s = 96 frames) -> Production Ready Summary

    def draw_common_ui(img, draw, frame_idx):
        cur_sec = frame_idx / float(FPS)
        mins = int(cur_sec // 60)
        secs = int(cur_sec % 60)
        time_str = f"{mins:02d}:{secs:02d} / 02:00"

        # Top persistent navigation header
        draw.rounded_rectangle([45, 18, WIDTH - 45, 58], radius=8, fill=(15, 23, 42, 230), outline=(30, 41, 59), width=1)

        # Brand badge
        draw.rounded_rectangle([55, 24, 210, 52], radius=6, fill=(30, 27, 75), outline=(99, 102, 241), width=1)
        draw.text((70, 31), "ATTENDANCE APP", fill=(165, 180, 252), font=f_badge)

        # Scene indicator
        if cur_sec < 12:
            scene_label = "[1/7] PRODUCT INTRODUCTION and ARCHITECTURE"
        elif cur_sec < 28:
            scene_label = "[2/7] MULTI-TENANT ORGANIZATIONS and DYNAMIC SHIFTS"
        elif cur_sec < 48:
            scene_label = "[3/7] STEP 1: MORNING CHECK-IN and EYE-BLINK LIVENESS AI"
        elif cur_sec < 68:
            scene_label = "[4/7] STEP 2: STATUTORY QUORUM and VOTING STATION"
        elif cur_sec < 88:
            scene_label = "[5/7] STEP 3: EVENING CHECK-OUT and TAMPER-PROOF SEAL"
        elif cur_sec < 104:
            scene_label = "[6/7] EXECUTIVE ADMIN PORTAL and DIRECT CSV EXPORT"
        elif cur_sec < 116:
            scene_label = "[7/7] REVENUECAT MULTI-STORE and TRIAL WARNING SENTINEL"
        else:
            scene_label = "[DEVPOST SHOWCASE] READY FOR ENTERPRISE DEPLOYMENT"

        draw.text((230, 31), scene_label, fill=(241, 245, 249), font=f_badge)

        # System Status Pill
        draw.rounded_rectangle([WIDTH - 380, 24, WIDTH - 170, 52], radius=6, fill=(6, 78, 59), outline=(16, 185, 129), width=1)
        draw.text((WIDTH - 365, 31), "100% OFFLINE SQLITE", fill=(110, 231, 183), font=f_badge)

        # Real-time counter
        draw.text((WIDTH - 150, 30), time_str, fill=(251, 191, 36), font=f_timer)

        # Bottom persistent progress bar
        progress = cur_sec / DURATION_SEC
        bar_w = WIDTH - 90
        fill_w = int(bar_w * progress)
        draw.rectangle([45, HEIGHT - 22, WIDTH - 45, HEIGHT - 14], fill=(17, 24, 39, 255))
        if fill_w > 0:
            draw.rectangle([45, HEIGHT - 22, 45 + fill_w, HEIGHT - 14], fill=(6, 182, 212, 255))
            draw.ellipse([45 + fill_w - 6, HEIGHT - 25, 45 + fill_w + 6, HEIGHT - 11], fill=(34, 211, 238, 255))

    # Helper: draw an informational glass card
    def draw_glass_card(draw, x1, y1, x2, y2, tag, title, sub, items, accent, border, status_txt=None, status_col=None):
        draw.rounded_rectangle([x1, y1, x2, y2], radius=14, fill=(17, 24, 39, 240), outline=border, width=1)
        draw.line([(x1 + 14, y1), (x2 - 14, y1)], fill=accent, width=3)

        draw.rounded_rectangle([x1 + 20, y1 + 18, x1 + 150, y1 + 42], radius=6, fill=accent, outline=(255, 255, 255), width=1)
        draw.text((x1 + 28, y1 + 23), tag, fill=(15, 23, 42), font=f_badge)

        draw.text((x1 + 20, y1 + 54), title, fill=(255, 255, 255), font=f_card_title)
        draw.text((x1 + 20, y1 + 78), sub, fill=accent, font=f_card_sub)
        draw.line([(x1 + 20, y1 + 98), (x2 - 20, y1 + 98)], fill=(30, 41, 59, 200), width=1)

        iy = y1 + 112
        for num, it_title, it_desc in items:
            draw.rounded_rectangle([x1 + 20, iy + 1, x1 + 42, iy + 21], radius=4, fill=(30, 41, 59), outline=accent, width=1)
            draw.text((x1 + 26, iy + 4), num, fill=accent, font=f_num)
            draw.text((x1 + 50, iy + 2), it_title, fill=(241, 245, 249), font=f_item_title)

            # Multiline desc
            words = it_desc.split(" ")
            lines = []
            curr = []
            for w in words:
                test = " ".join(curr + [w])
                if len(test) < 46:
                    curr.append(w)
                else:
                    lines.append(" ".join(curr))
                    curr = [w]
            if curr:
                lines.append(" ".join(curr))
            dy = iy + 22
            for l in lines[:2]:
                draw.text((x1 + 50, dy), l, fill=(148, 163, 184), font=f_item_desc)
                dy += 16

            iy += 68

        if status_txt:
            draw.rounded_rectangle([x1 + 20, y2 - 44, x2 - 20, y2 - 16], radius=6, fill=(15, 23, 42), outline=border, width=1)
            draw.text((x1 + 30, y2 - 37), status_txt, fill=status_col or accent, font=f_status)

    print("Rendering and encoding 2-minute video...")

    # Main Rendering Loop
    for f in range(TOTAL_FRAMES):
        sec = f / float(FPS)
        frame_img = base_bg.copy()
        draw = ImageDraw.Draw(frame_img)

        # -------------------- SCENE 1: TITLE and OVERVIEW (0s - 12s) --------------------
        if sec < 12.0:
            # Centered Hero Presentation Slide
            cx = WIDTH // 2
            # Icon
            if raw_icon:
                frame_img.paste(raw_icon, (cx - 32, 110), raw_icon)

            draw.rounded_rectangle([cx - 240, 190, cx + 240, 222], radius=8, fill=(30, 27, 75, 240), outline=(99, 102, 241), width=1)
            draw.text((cx - 215, 197), "★ OFFICIAL DEVPOST HACKATHON SHOWCASE ★", fill=(165, 180, 252), font=f_badge)

            draw.text((cx - 180, 235), "AttendanceApp", fill=(255, 255, 255), font=get_font(font_bold, 44))
            draw.text((cx - 380, 300), "Institutional Duty Attendance, Biometric Liveness and Quorum Voting System", fill=(129, 140, 248), font=get_font(font_semibold, 20))

            # 4 Architectural Pillars
            pillars = [
                ("01", "100% Offline Local SQLite", "Air-gapped architecture. Zero remote cloud leak. All duty logs, biometrics, and votes commit strictly to on-device Room DB.", (16, 185, 129)),
                ("02", "CameraX Eye-Blink AI Liveness", "MLKit calculates live Eye Aspect Ratio (EAR). Requires natural human blinks, defeating photo cutouts and digital screen replays.", (6, 182, 212)),
                ("03", "Strict 3-Step Sequence Verification", "Morning Check-In -> Quorum Voting Station -> Evening Seal. Mathematical state-machine locks each step until prerequisites pass.", (99, 102, 241)),
                ("04", "RevenueCat Multi-Store Monetization", "Unified Google Play and Amazon Appstore in-app purchases with 7-Day trial countdown and 2-Day expiration warning sentinels.", (236, 72, 153))
            ]

            pw = 860
            for idx, (pnum, ptitle, pdesc, paccent) in enumerate(pillars):
                px = 90 if idx % 2 == 0 else WIDTH - 90 - pw
                py = 370 if idx < 2 else 580
                draw.rounded_rectangle([px, py, px + pw, py + 180], radius=12, fill=(17, 24, 39, 235), outline=paccent, width=1)
                draw.rounded_rectangle([px + 20, py + 18, px + 52, py + 48], radius=6, fill=(30, 41, 59), outline=paccent, width=1)
                draw.text((px + 28, py + 24), pnum, fill=paccent, font=f_card_title)
                draw.text((px + 65, py + 22), ptitle, fill=(241, 245, 249), font=get_font(font_bold, 18))
                draw.text((px + 65, py + 60), pdesc, fill=(148, 163, 184), font=get_font(font_reg, 13))

            draw.text((cx - 340, 810), "Demonstrating the full operational workflow of the application across phone, tablet, and Fire TV", fill=(100, 116, 139), font=get_font(font_reg, 14))

        # -------------------- SCENE 2: MULTI-TENANT ORGS and SHIFTS (12s - 28s) --------------------
        elif sec < 28.0:
            # Left: Phone Mockup with Organizations Screen
            frame_img.paste(shadow_img, (110, 140), shadow_img)
            frame_img.paste(mockup_p4, (130, 160), mockup_p4)

            # Right: Interactive Process Explainer Cards
            draw_glass_card(
                draw, 640, 140, WIDTH - 90, 840,
                tag="STAGE 1 ARCHITECTURE",
                title="Multi-Tenant Institutional Hub and Dynamic Shift Timers",
                sub="Constitutional Entity Routing • Dual Shift Boundaries • Role-Based Access Control",
                accent=(99, 102, 241),
                border=(99, 102, 241, 160),
                status_txt="AUTHENTICATION STATUS: SESSION READY and SHIFT SYNCHRONIZED",
                status_col=(165, 180, 252),
                items=[
                    ("01", "Multi-Tenant Institutional Organization Hub", "Supports sovereign constitutional entities: Supreme Court and High Court, Election Commission, Bar Council, or Custom Municipal Bodies with isolated SQLite records."),
                    ("02", "Role-Based Privilege Dispatching", "Dispatches Presiding Officers and Members to duty execution flows, and authorized administrators to the Executive Audit and Discrepancy Portal."),
                    ("03", "Dynamic Morning and Evening Shift Timers", "Dynamically synchronizes institution shift windows (Morning: 09:00 - 13:00 | Evening: 16:00 - 19:00), strictly locking check-in/out buttons outside active shift hours."),
                    ("04", "RevenueCat Anonymous Device Identification", "Initializes subscription entitlements linked to local device tokens, ensuring uninterrupted offline access even when network is disconnected.")
                ]
            )

        # -------------------- SCENE 3: STEP 1 - MORNING CHECK-IN and LIVENESS AI (28s - 48s) --------------------
        elif sec < 48.0:
            # Left: Phone Mockup with Biometric Liveness Face Scan
            frame_img.paste(shadow_img, (110, 140), shadow_img)
            frame_img.paste(mockup_p1, (130, 160), mockup_p1)

            # Animate a pulsing / scanning laser bar across the phone screen viewfinder
            scan_cycle = math.sin((sec - 28.0) * 3.0)  # oscillates between -1 and 1
            laser_y = int(380 + (scan_cycle + 1.0) * 80)
            draw.line([(150, laser_y), (550, laser_y)], fill=(34, 211, 238, 220), width=3)

            # Dynamic blink metric simulation
            ear_val = 0.14 if abs(scan_cycle) > 0.75 else 0.32
            blink_detected = ear_val < 0.20

            draw_glass_card(
                draw, 640, 140, WIDTH - 90, 840,
                tag="STAGE 2 • STRICT SEQUENCE STEP 1",
                title="Morning Check-In with Real-Time Eye-Blink AI Liveness",
                sub="Google MLKit Computer Vision • Anti-Spoof Sentinel • Precise Geofencing GPS Lock",
                accent=(6, 182, 212),
                border=(6, 182, 212, 160),
                status_txt="LIVENESS AUDIT: BLINK DETECTED • 100% SPOOF-PROOF • STEP 1 RECORD COMMITTED ✓" if blink_detected else "SCANNING VIEWFINDER: AWAITING CONFIRMED EYE BLINK...",
                status_col=(103, 232, 249) if blink_detected else (251, 191, 36),
                items=[
                    ("01", f"Real-Time Eye Aspect Ratio (EAR: {ear_val:.2f})", "Continuously tracks left and right eye eyelid landmarks. A verified blink drops EAR below 0.20 threshold, completely thwarting 2D printed photos and video replay attacks."),
                    ("02", "Precise Geofence GPS Boundary Lock", "Validates device latitude and longitude coordinates against registered institution perimeter (<50m), guaranteeing the member is physically inside the designated premises."),
                    ("03", "Dynamic Shift Window Enforcement", "Confirms current time is within active morning shift window (09:00 - 13:00) before allowing biometric submission."),
                    ("04", "Cryptographic SQLite Duty Record Commit", "Commits encrypted check-in log with microsecond timestamp, photo biometric hash, and nature-of-work tag to on-device Room database.")
                ]
            )

        # -------------------- SCENE 4: STEP 2 - QUORUM and VOTING STATION (48s - 68s) --------------------
        elif sec < 68.0:
            # Left: Phone Mockup with Voting Screen
            frame_img.paste(shadow_img, (110, 140), shadow_img)
            frame_img.paste(mockup_p3, (130, 160), mockup_p3)

            # Animate quorum filling
            quorum_pct = min(88, int(60 + (sec - 48.0) * 1.5))

            draw_glass_card(
                draw, 640, 140, WIDTH - 90, 840,
                tag="STAGE 3 • STRICT SEQUENCE STEP 2",
                title="Statutory Quorum and Committee Voting Station",
                sub="Sequence-Enforced Unlock • Secret Ballot Resolutions • Duty Abandonment Sentinel",
                accent=(16, 185, 129),
                border=(16, 185, 129, 160),
                status_txt=f"QUORUM STATUS: {quorum_pct}% SATISFIED (100 / 128 ATTENDING) • BALLOT CONFIRMED ✓",
                status_col=(110, 231, 183),
                items=[
                    ("01", "Mathematical Sequence Guard", "Voting station remains strictly locked until Step 1 Morning Check-In is verified and sealed in the SQLite database, preventing fraudulent early votes."),
                    ("02", "Active Legislative / Council Ballots", "Presiding officers vote on critical council topics (e.g. Executive Disciplinary Council, Statutory Ethics Motion) with tamper-evident audit receipts."),
                    ("03", f"Real-Time Quorum Tracking ({quorum_pct}%)", "Automatically calculates active attending headcount to guarantee statutory quorum thresholds are reached before resolutions can be enacted."),
                    ("04", "Duty Abandonment Sentinel Protection", "Enforces voting before departure: any attempt to perform Evening Check-Out without casting ballot is blocked and flagged as duty abandonment.")
                ]
            )

        # -------------------- SCENE 5: STEP 3 - EVENING CHECK-OUT and SEAL (68s - 88s) --------------------
        elif sec < 88.0:
            # Left: Phone Mockup with Sequence State and Final Seal
            frame_img.paste(shadow_img, (110, 140), shadow_img)
            frame_img.paste(mockup_p2, (130, 160), mockup_p2)

            draw_glass_card(
                draw, 640, 140, WIDTH - 90, 840,
                tag="STAGE 4 • STRICT SEQUENCE STEP 3",
                title="Evening Check-Out and Cryptographic Record Sealing",
                sub="Secondary Biometric Re-Scan • Net Duty Hours Consolidation • Immutable Record Lock",
                accent=(168, 85, 247),
                border=(168, 85, 247, 160),
                status_txt="SESSION COMPLETED: DAY CLOSED • RECORD LOCKED IN IMMUTABLE STATE ✓",
                status_col=(216, 180, 254),
                items=[
                    ("01", "Secondary Facial Liveness Verification", "Mandatory second eye-blink liveness capture validates physical presence at departure, preventing proxy checkout or ghost attendance."),
                    ("02", "Shift Duration and Quorum Consolidation", "Consolidates morning arrival (09:14 AM), ballot record (11:42 AM), and departure (05:30 PM) into net 8 hours 16 minutes verified duty hours."),
                    ("03", "Cryptographic SQLite Tamper-Proof Seal", "Locks the daily record in SQLite Room DB into an immutable, read-only state. Prevents any post-submission alteration or manipulation."),
                    ("04", "Automatic Discrepancy Evaluator", "Flags early exits, late arrivals, or missed shifts automatically with reason codes for administrative review.")
                ]
            )

        # -------------------- SCENE 6: ADMIN PORTAL and CSV EXPORT (88s - 104s) --------------------
        elif sec < 104.0:
            # Left: Fire TV Widescreen Admin Portal Screenshot
            if raw_tv:
                tv_w = 760
                tv_h = 428
                tv_resized = raw_tv.resize((tv_w, tv_h), Image.Resampling.LANCZOS)
                frame_img.paste(tv_resized, (70, 220))
                draw.rounded_rectangle([70, 220, 70 + tv_w, 220 + tv_h], radius=8, outline=(245, 158, 11), width=2)
                draw.rounded_rectangle([70, 180, 420, 212], radius=6, fill=(245, 158, 11), outline=(255, 255, 255), width=1)
                draw.text((80, 187), "EXECUTIVE ADMIN CONSOLE (LEANBACK TV and TABLET)", fill=(15, 23, 42), font=f_badge)

            # Right: Admin Feature Explainer
            draw_glass_card(
                draw, 870, 140, WIDTH - 60, 840,
                tag="EXECUTIVE AUDIT SUITE",
                title="Admin and Audit Intelligence Center",
                sub="100% Local SQLite • Tamper-Evident Logs • 1-Click On-Device CSV Export",
                accent=(245, 158, 11),
                border=(245, 158, 11, 160),
                status_txt="AUDIT INTEGRITY: VERIFIED • ZERO EXTERNAL DATA LEAKAGE GUARANTEED ✓",
                status_col=(251, 191, 36),
                items=[
                    ("01", "Sub-Millisecond Multi-Filter Search Engine", "Live parametric queries by Aadhaar Number, Member ID, Full Name, Shift Type, or Calendar Date directly on indexed SQLite database."),
                    ("02", "Official Occasion and Assembly Sitting Tagging", "Designate records for National Holidays, Emergency Assemblies, Budget Sessions, or Tribunal Benches with permanent audit history."),
                    ("03", "Discrepancy Resolution and Audit Overrides", "Auditors review flagged discrepancies (abandonment, late entries) and log official administrative remarks."),
                    ("04", "1-Click Direct On-Device CSV Export", "Generates compliant audit spreadsheets stored strictly on local device storage—100% offline, zero cloud vulnerability.")
                ]
            )

        # -------------------- SCENE 7: REVENUECAT SUB and WARNING SENTINEL (104s - 116s) --------------------
        elif sec < 116.0:
            # RevenueCat Multi-Store and Subscription Safeguards
            draw_glass_card(
                draw, 90, 140, 940, 840,
                tag="COMMERCE ENGINE",
                title="RevenueCat Dual-Store Monetization",
                sub="Google Play Store + Amazon Appstore Flavors",
                accent=(236, 72, 153),
                border=(236, 72, 153, 160),
                status_txt="STORE STATUS: PLAY and AMAZON KEYS READY • DEMO SANDBOX ACTIVE",
                status_col=(249, 168, 212),
                items=[
                    ("01", "Cross-Platform Unified Purchases", "Single codebase serves Google Play (`standardAndroid` flavor) and Amazon Appstore (`amazon` flavor) with native SDK bindings."),
                    ("02", "Annual and Monthly In-App Subscriptions", "Annual Plan ($29.99/yr, 50% discount) and Monthly Plan ($4.99/mo) with full store receipt verification."),
                    ("03", "Judge and Evaluator Sandbox Mode", "Redeem promo codes (`JUDGE2026`, `REVENUECAT`) for instant unlocked evaluation without live credit card billing."),
                    ("04", "Offline Receipt and Entitlement Cache", "Caches Pro access state on device so members retain unlocked features even in zero-reception courtrooms.")
                ]
            )

            draw_glass_card(
                draw, 980, 140, WIDTH - 90, 840,
                tag="TRIAL SENTINEL",
                title="In-App Trial Countdown and Warning Sentinel",
                sub="Proactive Expiration Warnings • Graceful Auto-Downgrade",
                accent=(245, 158, 11),
                border=(245, 158, 11, 160),
                status_txt="WARNING ENGINE: IN-APP COUNTDOWN and EXPIRED PROMPTS OPERATIONAL ✓",
                status_col=(252, 211, 77),
                items=[
                    ("01", "7-Day Free Trial Autonomous Timer", "Records activation timestamp and provides real-time days-remaining countdown badges across all dashboards."),
                    ("02", "Proactive Expiration Warnings (<=2 Days)", "Displays prominent warning alerts (`⚠️ Trial ends in X days`) and toast reminders before trial lapsing."),
                    ("03", "Graceful Expiration and Paywall Prompt", "Upon 7 days completion, automatically downgrades to Free Tier and shows an actionable upgrade prompt."),
                    ("04", "Transparent Consumer Protection", "Zero hidden charges; respects store billing policies with full notice before any renewal.")
                ]
            )

        # -------------------- SCENE 8: RECAP and CONCLUSION (116s - 120s) --------------------
        else:
            cx = WIDTH // 2
            if raw_icon:
                frame_img.paste(raw_icon, (cx - 36, 200), raw_icon)

            draw.rounded_rectangle([cx - 260, 280, cx + 260, 314], radius=8, fill=(30, 27, 75), outline=(99, 102, 241), width=1)
            draw.text((cx - 235, 288), "★ PRODUCTION READY INSTITUTIONAL SUITE ★", fill=(165, 180, 252), font=f_badge)

            draw.text((cx - 180, 340), "AttendanceApp", fill=(255, 255, 255), font=get_font(font_bold, 44))
            draw.text((cx - 360, 410), "Ready for Google Play Store, Amazon Appstore and Enterprise Deployment", fill=(129, 140, 248), font=get_font(font_semibold, 20))

            tech_badges = [
                ("100% Kotlin 1.9", (99, 102, 241)),
                ("CameraX and MLKit AI", (6, 182, 212)),
                ("Room SQLite DB", (16, 185, 129)),
                ("RevenueCat SDK", (236, 72, 153)),
                ("Android and Fire TV", (139, 92, 246)),
                ("Zero Cloud Leak", (245, 158, 11))
            ]

            bx = cx - 440
            by = 480
            for t_name, t_col in tech_badges:
                draw.rounded_rectangle([bx, by, bx + 135, by + 40], radius=8, fill=(17, 24, 39), outline=t_col, width=1)
                draw.text((bx + 14, by + 12), t_name, fill=t_col, font=f_badge)
                bx += 150

            draw.text((cx - 210, 580), "Thank you for reviewing AttendanceApp for Devpost!", fill=(148, 163, 184), font=get_font(font_semibold, 16))

        # Persistent Chrome UI (Navigation bar and Progress Bar)
        draw_common_ui(frame_img, draw, f)

        # Write frame bytes to FFmpeg stdin
        proc.stdin.write(frame_img.tobytes())

        if f % (FPS * 10) == 0:
            pct = (f / float(TOTAL_FRAMES)) * 100.0
            print(f"Progress: {pct:.1f}% ({f}/{TOTAL_FRAMES} frames rendered)")

    # Close pipe and wait for FFmpeg to finish encoding
    proc.stdin.close()
    proc.wait()
    print("Video encoding complete!")

    # Copy output to F: drive and Desktop
    dest_paths = [
        r"F:\AttendanceApp_RevenueCat\attendance_app_2min_demo.mp4",
        r"C:\Users\HP\Desktop\attendance_store_assets\attendance_app_2min_demo.mp4",
        r"C:\Users\HP\.gemini\antigravity-cli\brain\4515bfce-4739-4f4f-95c0-f93f8477fd2f\attendance_app_2min_demo.mp4"
    ]
    for dp in dest_paths:
        try:
            os.makedirs(os.path.dirname(dp), exist_ok=True)
            with open(out_mp4, "rb") as rf:
                with open(dp, "wb") as wf:
                    wf.write(rf.read())
            print(f"Copied demo video to: {dp}")
        except Exception as e:
            print(f"Failed to copy to {dp}: {e}")

if __name__ == "__main__":
    generate_video()
