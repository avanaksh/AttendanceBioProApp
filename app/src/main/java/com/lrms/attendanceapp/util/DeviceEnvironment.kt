package com.lrms.attendanceapp.util

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.util.Log

/**
 * Universal Hardware & OS Environment Auto-Detector.
 * Runs completely silently at startup without disturbing or notifying the user.
 * Seamlessly distinguishes Amazon Fire OS / Fire Tablets from standard Android devices.
 */
object DeviceEnvironment {

    private const val TAG = "DeviceEnvironment"

    var isAmazonFireOS: Boolean = false
        private set

    var isAmazonFireTV: Boolean = false
        private set

    var hasHardwareGps: Boolean = false
        private set

    var hasHardwareCamera: Boolean = false
        private set

    var hasTelephony: Boolean = false
        private set

    var deviceModel: String = ""
        private set

    var osVersionName: String = ""
        private set

    /**
     * Executes silently at application startup.
     * Evaluates system properties, build fingerprint, and hardware features.
     */
    fun detectAtStartup(context: Context) {
        try {
            val manufacturer = Build.MANUFACTURER ?: ""
            val model = Build.MODEL ?: ""
            val brand = Build.BRAND ?: ""
            val fingerprint = Build.FINGERPRINT ?: ""

            deviceModel = "$manufacturer $model".trim()
            osVersionName = "Android ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})"

            // 1. Silent Amazon Fire OS / Fire Tablet & Fire TV Detection:
            val uiModeManager = context.getSystemService(Context.UI_MODE_SERVICE) as? android.app.UiModeManager
            val isTvMode = uiModeManager?.currentModeType == android.content.res.Configuration.UI_MODE_TYPE_TELEVISION
            val isFireTvModel = model.startsWith("AFT", ignoreCase = true) // All Amazon Fire TV models start with 'AFT'

            val isAmazonBrand = manufacturer.equals("Amazon", ignoreCase = true) ||
                    brand.equals("Amazon", ignoreCase = true) ||
                    fingerprint.contains("Amazon", ignoreCase = true)

            isAmazonFireTV = isFireTvModel || (isAmazonBrand && isTvMode)
            isAmazonFireOS = isAmazonBrand || model.startsWith("KF", ignoreCase = true) || isFireTvModel

            // 2. Silent Hardware Capabilities Query via PackageManager
            val pm = context.packageManager
            hasHardwareCamera = pm.hasSystemFeature(PackageManager.FEATURE_CAMERA_ANY)
            hasHardwareGps = pm.hasSystemFeature(PackageManager.FEATURE_LOCATION_GPS)
            hasTelephony = pm.hasSystemFeature(PackageManager.FEATURE_TELEPHONY)

            Log.i(
                TAG,
                "Device Auto-Detected: Model='$deviceModel', isAmazon=$isAmazonFireOS, GPS=$hasHardwareGps, Camera=$hasHardwareCamera, Telephony=$hasTelephony"
            )
        } catch (e: Exception) {
            Log.w(TAG, "Hardware/OS silent detection fallback: ${e.message}")
        }
    }
}
