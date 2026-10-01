### Additional Notes & Testing Instructions for Judges

#### 1. Instant Pro Access & Promo Code
To test all premium features without payment, we have provided two built-in evaluation mechanisms directly on the paywall:
* **Promo Code:** Tap **"Redeem Promo Code"** on the paywall screen and enter:
  ```
  JUDGE2026
  ```
  *(or `REVENUECAT` / `SHIPATON`)*. This will permanently unlock all Pro features (`pro_access`) for your session.
* **Instant Free Trial:** You can also tap **"Start 7-Day Free Trial"** to simulate an active trial subscription.

---

#### 2. App Availability & Direct APK Download
The app has been submitted to the Google Play Store under package ID:
```
com.lrms.attendanceapp
```
Because the store listing is rolling out through review, judges can immediately install and test the release APK directly on any Android device or emulator:
* **Direct APK Download:** `[Insert your Google Drive, Dropbox, or GitHub Release link to app-standardAndroid-release.apk]`
* **Demo Video (2 min):** `[Insert your YouTube / Vimeo link]`

---

#### 3. Quick 2-Minute Evaluation Flow
1. **Setup:** Open the app and tap **"Skip and Continue"** to enter the main dashboard.
2. **Face Enrollment:** Tap **Staff Management** $\to$ **Add Staff**, enter a name, and capture 1–2 reference face photos.
3. **Biometric Check-In:** Return to the home screen and tap **Check-In**. Align your face in the biometric scanner ring to observe the real-time AI face match and GPS geofence radar verification.
4. **Paywall & RevenueCat:** Navigate to **Upgrade to Pro** (or attempt to export a payroll CSV/PDF). Enter promo code `JUDGE2026` to observe the instant RevenueCat entitlement unlock.

---

#### 4. Architecture Highlights
* **Zero Cloud Latency:** 100% of facial detection and embedding comparisons execute entirely on-device, preserving frontline worker privacy and ensuring full functionality in zero-connectivity environments.
* **Robust Multi-Store Billing:** The codebase features flavor separation for Google Play Billing and Amazon Appstore, powered cleanly through the RevenueCat Purchases SDK.
