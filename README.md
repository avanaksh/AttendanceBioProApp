# BioCheck Pro (AttendanceBioProApp) 📱✨

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Fire%20OS-brightgreen.svg)](https://developer.android.com)
[![RevenueCat](https://img.shields.io/badge/Monetization-RevenueCat%20SDK-orange.svg)](https://www.revenuecat.com)
[![Status](https://img.shields.io/badge/Release-v1.0%20Production-success.svg)](https://github.com/avanaksh/AttendanceBioProApp)

**BioCheck Pro** is an enterprise-grade biometric workforce attendance and geofencing verification application built for Android and Amazon Fire OS devices. This app turns any standard Android device into a high-security attendance kiosk, eliminating buddy-punching and time theft with 100% on-device edge AI.

---

## 🚀 Key Highlights

* 🧠 **100% On-Device AI Facial Recognition:** Zero-latency biometric authentication running completely locally. Worker facial embeddings are never transmitted to third-party servers, guaranteeing privacy and ensuring operation in zero-connectivity environments (basements, remote job sites).
* 🛰️ **Interactive GPS Geofencing Radar:** Real-time perimeter radar visualization that dynamically alerts workers when they are inside (green) or outside (amber) their authorized work boundary.
* 💳 **RevenueCat Tiered In-App Subscriptions:** Powered natively by the RevenueCat SDK with the `pro_access` entitlement, offering monthly and annual subscriptions with automatic localized currency display and 7-day free trials.
* 🏢 **Multi-Flavor Build Architecture:** Clean Gradle product flavors supporting **Google Play Store** (`standardAndroid`) and **Amazon Appstore** (`amazon`), each utilizing isolated store-specific RevenueCat API keys and billing clients.
* 📊 **Automated Payroll Reporting:** One-tap export of verified check-in timestamps, GPS coordinates, and face-match scores into CSV and PDF reports.
* 🛡️ **Evaluator Ready:** Built-in evaluation mechanisms including one-tap trial simulation and promo code redemption (`XXXXX2026` or `REVENUECAT`) to test all premium features without payment.

---

## 🛠️ Architecture and Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Kotlin and Java | Modern Android development with Coroutines and ViewBinding |
| **Monetization** | RevenueCat SDK | Subscriptions, entitlements (`pro_access`), dynamic offerings, customer info cache |
| **Biometrics / AI** | On-Device ML | Real-time face detection, alignment, and facial embedding comparison |
| **Location Services** | Google Play Location / GPS | GPS provider geofencing with graceful fallbacks |
| **Database** | SQLite / Room | Offline-first local persistence for employee records and duty logs |
| **UI Design** | Material Design 3 | Dark-mode biometric scanner ring, radar view, and custom Paywall |

---

## 💰 Monetization Strategy

BioCheck Pro employs a high-converting **B2B SaaS tiered model** addressing the daily operational needs of small-to-medium businesses:

* **Free Starter Tier:** Supports up to 5 employees with basic attendance logging (removes onboarding friction and drives organic adoption).
* **Pro Monthly ($9.99/mo):** Unlimited staff enrollment, offline AI face recognition, interactive GPS geofencing, and automated timesheet exports.
* **Pro Annual ($89.99/yr — 25% Savings):** All Pro features with annual billing, including an optional 7-day free trial.

### Why This Model?
Traditional biometric punch clocks cost **$300–$800 upfront** plus maintenance. Moreover, "buddy punching" (time theft) drains 2%–5% of gross payroll. For a 10-person crew earning $15/hr, stopping just 15 minutes of unworked time per day saves **~$975/month**—yielding an immediate **>9,000% ROI** for business owners.

---

## 🧪 Evaluation and Testing Instructions

To test all premium features without payment:
1. Open the app and navigate to **Upgrade to Pro** (or attempt to export a payroll CSV/PDF report).
2. Tap **"Redeem Promo Code"** and enter:
   ```text
   XXXXX2026
   ```
   *(or `REVENUECAT` / `SHIPATON`)*. This will permanently activate `pro_access` for the device.
3. Alternatively, tap **"Start 7-Day Free Trial"** to simulate an active trial subscription.

---

## 📦 Project Structure

```text
AttendanceBioProApp/
├── app/
│   ├── src/
│   │   ├── main/                 # Core shared application logic, UI, and ML
│   │   │   ├── java/com/lrms/attendanceapp/
│   │   │   │   ├── iap/          # RevenueCat SubscriptionManager and PaywallActivity
│   │   │   │   ├── ui/           # Activities, ViewHolders, Biometric Radar View
│   │   │   │   └── util/         # Geofencing, DeviceEnvironment and SQLite helpers
│   │   │   └── res/              # Layouts, vector drawables, localized strings
│   │   ├── standardAndroid/      # Google Play flavor (Google Play Billing 8.3.0)
│   │   └── amazon/               # Amazon Appstore flavor (purchases-store-amazon)
│   └── build.gradle              # Multi-flavor dependencies and SDK configurations
├── LICENSE                       # MIT Open Source License
└── README.md
```

---

## ⚙️ How to Build

Clone the repository and build using Gradle:

```bash
# Clone the repository
git clone https://github.com/avanaksh/AttendanceBioProApp.git
cd AttendanceBioProApp

# Build Google Play release bundle (.aab)
./gradlew bundleStandardAndroidRelease

# Build Google Play release APK (.apk)
./gradlew assembleStandardAndroidRelease

# Build Amazon Appstore release APK (.apk)
./gradlew assembleAmazonRelease
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

```text
MIT License
Copyright (c) 2026 Avanaksh Singh Sambyal
```
See the full text in the [LICENSE](LICENSE) file.
