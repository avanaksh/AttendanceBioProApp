# BioCheck Pro — Devpost Award Category Submission Notes

---

## 1. HAMM Award (Help Apps Make Money — Monetization Strategy)

### Monetization Model & Strategy
BioCheck Pro uses a high-converting B2B SaaS subscription model powered by RevenueCat, addressing the daily operational needs of small-to-medium businesses, field contractors, and retail teams.

* **Free Starter Tier:** Supports up to 5 members with basic attendance logging to drive organic adoption and remove onboarding friction.
* **Pro Monthly ($9.99/mo):** Unlocks unlimited staff check-ins, on-device AI facial recognition, interactive GPS geofencing, and automated timesheet exports (CSV/PDF).
* **Pro Annual ($89.99/yr — 25% discount):** Full Pro access with annual billing, including a 7-day free trial.

### Paywall Craft & RevenueCat Implementation
Integrated via RevenueCat SDK (`CustomerInfo`, Offerings, and the `pro_access` entitlement) within a dedicated native `PaywallActivity`. The paywall features transparent feature-matrix comparisons, localized store pricing, and instant entitlement unlocking. Because daily workforce compliance is mission-critical, B2B retention and lifetime value (LTV) are exceptionally high compared to consumer utility apps.

---

## 2. #BuildInPublic Award (Community & Social Journey)

### Building in Public Journey (#Shipaton)
Throughout the Shipaton hackathon, we openly documented the technical build, UI design iterations, and store launch process across social media under `#Shipaton` and `#BuildInPublic`.

### How Public Feedback Shaped the App
Sharing our progress publicly directly influenced two core engineering decisions:
1. Community feedback highlighted that field workers and construction teams frequently work in basements and remote areas with zero cell connectivity. In response, we engineered **100% offline-first AI facial recognition and local SQLite sync**.
2. Discussions on multi-channel distribution prompted us to implement a multi-flavor architecture supporting both Google Play and Amazon ecosystem devices.

### Highlighted Social Links
* **Demo Video & Showcase:** `[Paste your X/Twitter, LinkedIn, or YouTube post link]`
* **Architecture & Paywall Deep Dive:** `[Paste your tech devlog or tweet thread link]`
* **Ship Announcement:** `[Paste your launch announcement link]`

---

## 3. RevenueCat Design Award (Biometric UI & Standout Craft)

### Design Philosophy & Craft
BioCheck Pro blends cutting-edge on-device computer vision with clean, frictionless Material Design 3, engineered specifically so non-technical shift workers can complete an authenticated check-in in under 3 seconds.

### Standout Areas for Judges to Explore
* **Live Biometric Scan Experience:** Real-time camera viewfinder featuring a pulsing biometric target ring with immediate visual and haptic confirmation once a face is authenticated.
* **Interactive Geofence Radar:** A dynamic visual perimeter radar that transitions smoothly from amber (outside zone) to vibrant emerald green (within authorized job-site radius).
* **Polished Native Paywall:** High-clarity typography, clean visual hierarchy, transparent billing terms, and smooth micro-animations that make upgrading straightforward and trustworthy.

---

## 4. RevenueCat Peace Prize (Social Good & Workplace Fairness)

### Social Good & Community Impact
Wage theft and disputed work hours affect millions of vulnerable hourly, frontline, and gig workers globally. BioCheck Pro was created to bring transparency, accountability, and fairness to hourly workplace compensation.

### Impact & Community Benefit
* **Combats Wage Discrepancies:** Generates tamper-proof, timestamped, and GPS-verified attendance proof that guarantees workers are paid accurately for every minute on site.
* **Protects Worker Privacy:** Biometric facial recognition runs entirely on-device; biometric data is never transmitted or sold to third-party servers.
* **Free for Non-Profits & Community Groups:** The permanent free tier enables NGOs, volunteer clinics, disaster relief coordinators, and community projects to organize shifts and track volunteer hours without budget hurdles.
