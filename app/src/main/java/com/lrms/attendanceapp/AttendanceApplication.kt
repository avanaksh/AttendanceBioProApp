package com.lrms.attendanceapp

import android.app.Application
import android.util.Log
import com.lrms.attendanceapp.util.DeviceEnvironment
import com.revenuecat.purchases.LogLevel
import com.revenuecat.purchases.Purchases
import com.revenuecat.purchases.PurchasesConfiguration
import com.revenuecat.purchases.Store

class AttendanceApplication : Application() {

    override fun onCreate() {
        super.onCreate()
        instance = this

        // 1. Silent Hardware & OS Detection at Startup (no UI / user disturbance)
        DeviceEnvironment.detectAtStartup(this)

        // Enable debug logs for RevenueCat during development
        Purchases.logLevel = LogLevel.DEBUG

        // Configure RevenueCat Purchases SDK safely
        try {
            val key = REVENUECAT_API_KEY
            val isAmazonStore = key.startsWith("amzn_") || DeviceEnvironment.isAmazonFireOS
            val configBuilder = PurchasesConfiguration.Builder(this, key)
            if (isAmazonStore) {
                configBuilder.store(Store.AMAZON)
            }
            Purchases.configure(configBuilder.build())
            Log.d(
                TAG,
                "AttendanceApplication initialized with RevenueCat SDK (Store: ${if (isAmazonStore) "Amazon" else "Google Play"}, KeyPrefix: ${key.take(5)}...)"
            )
        } catch (t: Throwable) {
            Log.e(TAG, "Failed to initialize RevenueCat Purchases SDK: ${t.message}", t)
        }
    }

    companion object {
        private const val TAG = "AttendanceApplication"

        lateinit var instance: AttendanceApplication
            private set

        // Dedicated RevenueCat Public API Keys:
        const val AMAZON_API_KEY = "amzn_gBlQlarricNvAfzyHewgmbWKDye"
        const val GOOGLE_PLAY_API_KEY = "goog_imIbmlRuTysfzLQkdfZwAIOrvoJ"

        // Automatically resolves key based on build flavor & device environment
        val REVENUECAT_API_KEY: String
            get() = if (DeviceEnvironment.isAmazonFireOS) AMAZON_API_KEY else BuildConfig.REVENUECAT_API_KEY

        // Entitlement ID configured in RevenueCat dashboard (e.g., 'pro_access')
        const val ENTITLEMENT_ID = "pro_access"
    }
}
