# AttendanceApp - RevenueCat In-App Purchase & Subscription Module

This project is a standalone copy of the Attendance App with a fully integrated **RevenueCat In-App Purchase (IAP)** and subscription paywall module.

- **Project Location:** `F:\AttendanceApp_RevenueCat`
- **Compiled Output:** `F:\AttendanceApp_RevenueCat\app\build\outputs\apk\debug\app-debug.apk`

---

## 🏗 Architecture & Key Files

### 1. Application Initialization
* **File:** [`AttendanceApplication.kt`](file:///F:/AttendanceApp_RevenueCat/app/src/main/java/com/lrms/attendanceapp/AttendanceApplication.kt)
* Configures the RevenueCat Purchases SDK (`Purchases.configure(...)`) with debug logging enabled.
* Contains the configuration constants:
  * `REVENUECAT_GOOGLE_API_KEY` (placeholder: `"goog_sample_api_key_replace_with_yours"`)
  * `ENTITLEMENT_ID` (`"pro_access"`)

### 2. In-App Purchase Management
* **File:** [`SubscriptionManager.kt`](file:///F:/AttendanceApp_RevenueCat/app/src/main/java/com/lrms/attendanceapp/iap/SubscriptionManager.kt)
* Singleton wrapper around RevenueCat Purchases API:
  * `checkProAccess(onResult)`: Checks if the user currently holds the active Pro entitlement.
  * `fetchOfferings(onSuccess, onError)`: Fetches active paywall packages and localized prices from Google Play via RevenueCat.
  * `purchase(activity, package, onSuccess, onError)`: Launches the Google Play billing purchase flow.
  * `restorePurchases(onSuccess, onError)`: Restores previously purchased subscriptions (required by Google Play).
  * `identifyUser(userId)`: Binds the user's Attendance ID to RevenueCat for cross-device sync.
  * `logOut()`: Resets RevenueCat session back to anonymous on logout.

### 3. Subscription Paywall UI
* **File:** [`PaywallActivity.kt`](file:///F:/AttendanceApp_RevenueCat/app/src/main/java/com/lrms/attendanceapp/iap/PaywallActivity.kt)
* **Layout:** [`activity_paywall.xml`](file:///F:/AttendanceApp_RevenueCat/app/src/main/res/layout/activity_paywall.xml)
* Features:
  * Modern Tailwind/Slate dark-themed paywall matching the app.
  * Highlights Pro features (unlimited logs, cloud sync, biometric verification, report exports).
  * Selectable Annual (Save 40%) vs. Monthly cards with live localized pricing.
  * One-tap purchase CTA button with progress indicators.
  * "Restore Purchases" button.
  * Google Play Store auto-renewable subscription legal disclaimer.

### 4. Main Activity Integration
* **File:** [`MainActivity.kt`](file:///F:/AttendanceApp_RevenueCat/app/src/main/java/com/lrms/attendanceapp/ui/MainActivity.kt)
* **Layout:** [`activity_main.xml`](file:///F:/AttendanceApp_RevenueCat/app/src/main/res/layout/activity_main.xml)
* Automatically checks Pro status in `onResume()` and displays a dynamic banner:
  * **Free User:** ⭐ "Upgrade to Pro Access" banner with button leading to `PaywallActivity`.
  * **Pro User:** 👑 "PRO Member Active" gold badge.

---

## 🚀 How to Connect Your RevenueCat Dashboard

1. **Create an Account:**
   * Go to [app.revenuecat.com](https://app.revenuecat.com/) and create a project.
2. **Add Android App:**
   * In Project Settings > Apps, add an Android app.
   * Package Name: `com.lrms.attendanceapp`
   * Link your Google Play Service Account JSON key (for validating receipt tokens).
3. **Set Up Products & Entitlements in RevenueCat:**
   * **Entitlement:** Create an entitlement with Identifier `pro_access`.
   * **Products:** Add your Google Play subscription product IDs (e.g. `attendance_pro_monthly`, `attendance_pro_annual`).
   * Attach both products to the `pro_access` entitlement.
   * **Offering:** Create an offering named `default` and attach your monthly and annual packages.
4. **Update API Key in App:**
   * In [`AttendanceApplication.kt`](file:///F:/AttendanceApp_RevenueCat/app/src/main/java/com/lrms/attendanceapp/AttendanceApplication.kt#L29), replace:
     ```kotlin
     const val REVENUECAT_GOOGLE_API_KEY = "goog_YOUR_REAL_KEY"
     ```

---

## 🛠 Building & Running

Open `F:\AttendanceApp_RevenueCat` in **Android Studio** or compile via terminal:
```cmd
set JAVA_HOME=C:\Program Files\Java\jdk-17
gradlew.bat assembleDebug
```
The APK will be generated at:
`app\build\outputs\apk\debug\app-debug.apk`
