import os
import re

files_to_update = [
    r"C:\AttendanceApp_RevenueCat\generate_workflow_diagram.py",
    r"C:\AttendanceApp_RevenueCat\generate_workflow_svg.py",
    r"C:\AttendanceApp_RevenueCat\generate_devpost_cover.py",
    r"C:\AttendanceApp_RevenueCat\generate_demo_video.py",
    r"C:\AttendanceApp_RevenueCat\generate_all_store_assets.py",
    r"C:\AttendanceApp_RevenueCat\generate_google_play_assets.py",
    r"C:\AttendanceApp_RevenueCat\generate_tablet_assets.py",
    r"C:\AttendanceApp_RevenueCat\create_store_assets.py"
]

for file_path in files_to_update:
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace &amp; first
    content = content.replace("&amp;", "and")
    # Replace & in uppercase contexts e.g. MONETIZATION & TRIALS -> MONETIZATION AND TRIALS
    content = content.replace(" & ", " and ")
    content = content.replace(" &", " and")
    content = content.replace("& ", "and ")
    content = content.replace("&", "and")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {os.path.basename(file_path)}")

print("All files updated successfully!")
