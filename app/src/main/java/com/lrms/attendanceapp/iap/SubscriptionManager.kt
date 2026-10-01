package com.lrms.attendanceapp.iap

import android.app.Activity
import android.util.Log
import com.lrms.attendanceapp.AttendanceApplication
import com.revenuecat.purchases.CustomerInfo
import com.revenuecat.purchases.Offerings
import com.revenuecat.purchases.Package
import com.revenuecat.purchases.PurchaseParams
import com.revenuecat.purchases.Purchases
import com.revenuecat.purchases.PurchasesError
import com.revenuecat.purchases.interfaces.PurchaseCallback
import com.revenuecat.purchases.interfaces.ReceiveCustomerInfoCallback
import com.revenuecat.purchases.interfaces.ReceiveOfferingsCallback
import com.revenuecat.purchases.interfaces.LogInCallback
import com.revenuecat.purchases.models.StoreTransaction

/**
 * Singleton manager to interface cleanly with RevenueCat Purchases SDK
 */
data class SubscriptionDetails(
    val isPro: Boolean,
    val isTrial: Boolean,
    val daysRemaining: Int,
    val isExpiringSoon: Boolean,
    val isExpired: Boolean,
    val planName: String,
    val message: String
)

object SubscriptionManager {

    private const val TAG = "SubscriptionManager"
    private const val PREFS_NAME = "revenuecat_demo_prefs"
    private const val KEY_TRIAL_ACTIVE = "key_trial_active"
    private const val KEY_TRIAL_START_TIME = "key_trial_start_time"
    private const val TRIAL_DURATION_DAYS = 7
    private const val TRIAL_DURATION_MS = TRIAL_DURATION_DAYS * 24 * 60 * 60 * 1000L

    fun start7DayFreeTrial() {
        try {
            val prefs = AttendanceApplication.instance.getSharedPreferences(PREFS_NAME, android.content.Context.MODE_PRIVATE)
            prefs.edit()
                .putBoolean(KEY_TRIAL_ACTIVE, true)
                .putLong(KEY_TRIAL_START_TIME, System.currentTimeMillis())
                .putBoolean("is_simulated_pro", true)
                .apply()
        } catch (e: Exception) {
            Log.w(TAG, "Failed to start free trial: ${e.message}")
        }
    }

    fun getTrialDetails(): SubscriptionDetails {
        val prefs = AttendanceApplication.instance.getSharedPreferences(PREFS_NAME, android.content.Context.MODE_PRIVATE)
        val isTrialActive = prefs.getBoolean(KEY_TRIAL_ACTIVE, false)
        val startTime = prefs.getLong(KEY_TRIAL_START_TIME, 0L)

        if (!isTrialActive || startTime == 0L) {
            val isSimPro = prefs.getBoolean("is_simulated_pro", false)
            return if (isSimPro) {
                SubscriptionDetails(
                    isPro = true,
                    isTrial = false,
                    daysRemaining = 365,
                    isExpiringSoon = false,
                    isExpired = false,
                    planName = "Pro Lifetime Pass",
                    message = "Active Pro Access"
                )
            } else {
                SubscriptionDetails(
                    isPro = false,
                    isTrial = false,
                    daysRemaining = 0,
                    isExpiringSoon = false,
                    isExpired = false,
                    planName = "Free Plan",
                    message = "Basic Access"
                )
            }
        }

        val elapsed = System.currentTimeMillis() - startTime
        val remainingMs = TRIAL_DURATION_MS - elapsed

        return if (remainingMs <= 0) {
            prefs.edit()
                .putBoolean(KEY_TRIAL_ACTIVE, false)
                .putBoolean("is_simulated_pro", false)
                .apply()
            SubscriptionDetails(
                isPro = false,
                isTrial = true,
                daysRemaining = 0,
                isExpiringSoon = false,
                isExpired = true,
                planName = "7-Day Free Trial",
                message = "Your 7-Day Free Trial has expired. Upgrade to Monthly or Yearly to restore Pro access."
            )
        } else {
            val daysRemaining = Math.max(1, Math.ceil(remainingMs / (24.0 * 60 * 60 * 1000)).toInt())
            val isExpiringSoon = daysRemaining <= 2
            SubscriptionDetails(
                isPro = true,
                isTrial = true,
                daysRemaining = daysRemaining,
                isExpiringSoon = isExpiringSoon,
                isExpired = false,
                planName = "7-Day Free Trial",
                message = if (isExpiringSoon)
                    "⚠️ Warning: Free Trial expires in $daysRemaining day${if (daysRemaining > 1) "s" else ""}!"
                else
                    "7-Day Free Trial: $daysRemaining days left"
            )
        }
    }

    fun setPermanentPro(active: Boolean) {
        try {
            val prefs = AttendanceApplication.instance.getSharedPreferences(PREFS_NAME, android.content.Context.MODE_PRIVATE)
            prefs.edit()
                .putBoolean("is_simulated_pro", active)
                .putBoolean(KEY_TRIAL_ACTIVE, false)
                .putLong(KEY_TRIAL_START_TIME, 0L)
                .apply()
        } catch (e: Exception) {
            Log.w(TAG, "Failed to persist permanent pro: ${e.message}")
        }
    }

    fun setSimulatedPro(active: Boolean) {
        setPermanentPro(active)
    }

    fun isSimulatedPro(): Boolean {
        return try {
            val prefs = AttendanceApplication.instance.getSharedPreferences(PREFS_NAME, android.content.Context.MODE_PRIVATE)
            val isTrialActive = prefs.getBoolean(KEY_TRIAL_ACTIVE, false)
            if (isTrialActive) {
                val startTime = prefs.getLong(KEY_TRIAL_START_TIME, 0L)
                if (startTime != 0L) {
                    val elapsed = System.currentTimeMillis() - startTime
                    if (elapsed >= TRIAL_DURATION_MS) {
                        return false
                    }
                }
            }
            prefs.getBoolean("is_simulated_pro", false)
        } catch (e: Exception) {
            false
        }
    }

    /**
     * Checks subscription status and returns full countdown & expiration warning details
     */
    fun checkSubscriptionStatus(onResult: (SubscriptionDetails) -> Unit) {
        val trialDetails = getTrialDetails()
        if (trialDetails.isPro) {
            onResult(trialDetails)
            return
        }

        if (!Purchases.isConfigured) {
            onResult(trialDetails)
            return
        }

        Purchases.sharedInstance.getCustomerInfo(object : ReceiveCustomerInfoCallback {
            override fun onReceived(customerInfo: CustomerInfo) {
                val entitlement = customerInfo.entitlements[AttendanceApplication.ENTITLEMENT_ID]
                val isPro = entitlement?.isActive == true
                if (isPro && entitlement != null) {
                    val expDate = entitlement.expirationDate
                    val willRenew = entitlement.willRenew
                    var days = 30
                    var expiringSoon = false
                    if (expDate != null) {
                        val remMs = expDate.time - System.currentTimeMillis()
                        if (remMs > 0) {
                            days = Math.max(1, Math.ceil(remMs / (24.0 * 60 * 60 * 1000)).toInt())
                            if (!willRenew && days <= 3) {
                                expiringSoon = true
                            }
                        }
                    }
                    onResult(
                        SubscriptionDetails(
                            isPro = true,
                            isTrial = false,
                            daysRemaining = days,
                            isExpiringSoon = expiringSoon,
                            isExpired = false,
                            planName = entitlement.productIdentifier,
                            message = if (expiringSoon) "⚠️ Subscription ends in $days days (Auto-renew OFF)" else "Active Pro Subscription"
                        )
                    )
                } else {
                    onResult(trialDetails)
                }
            }

            override fun onError(error: PurchasesError) {
                onResult(trialDetails)
            }
        })
    }

    /**
     * Checks whether the user has the active Pro entitlement
     */
    fun checkProAccess(onResult: (isPro: Boolean) -> Unit) {
        checkSubscriptionStatus { details ->
            onResult(details.isPro)
        }
    }

    /**
     * Fetches the current active paywall offerings configured in RevenueCat dashboard
     */
    fun fetchOfferings(
        onSuccess: (Offerings) -> Unit,
        onError: (PurchasesError) -> Unit
    ) {
        Purchases.sharedInstance.getOfferings(object : ReceiveOfferingsCallback {
            override fun onReceived(offerings: Offerings) {
                onSuccess(offerings)
            }

            override fun onError(error: PurchasesError) {
                Log.e(TAG, "Error fetching offerings: ${error.message}")
                onError(error)
            }
        })
    }

    /**
     * Initiates Amazon Appstore purchase flow for a selected package
     */
    fun purchase(
        activity: Activity,
        packageToPurchase: Package,
        onSuccess: (CustomerInfo) -> Unit,
        onError: (error: PurchasesError, userCancelled: Boolean) -> Unit
    ) {
        val params = PurchaseParams.Builder(activity, packageToPurchase).build()
        Purchases.sharedInstance.purchase(params, object : PurchaseCallback {
            override fun onCompleted(storeTransaction: StoreTransaction, customerInfo: CustomerInfo) {
                Log.d(TAG, "Purchase completed successfully: ${storeTransaction.orderId}")
                onSuccess(customerInfo)
            }

            override fun onError(error: PurchasesError, userCancelled: Boolean) {
                Log.e(TAG, "Purchase failed: ${error.message}, userCancelled: $userCancelled")
                onError(error, userCancelled)
            }
        })
    }

    /**
     * Restores previous purchases (e.g., if user reinstalled the app or switched devices)
     */
    fun restorePurchases(
        onSuccess: (CustomerInfo) -> Unit,
        onError: (PurchasesError) -> Unit
    ) {
        Purchases.sharedInstance.restorePurchases(object : ReceiveCustomerInfoCallback {
            override fun onReceived(customerInfo: CustomerInfo) {
                Log.d(TAG, "Purchases restored successfully")
                onSuccess(customerInfo)
            }

            override fun onError(error: PurchasesError) {
                Log.e(TAG, "Error restoring purchases: ${error.message}")
                onError(error)
            }
        })
    }

    /**
     * Associate RevenueCat with your backend user identifier (e.g. employee/student ID)
     */
    fun identifyUser(userId: String, onComplete: ((CustomerInfo?) -> Unit)? = null) {
        if (!Purchases.isConfigured) return
        Purchases.sharedInstance.logIn(userId, object : LogInCallback {
            override fun onReceived(customerInfo: CustomerInfo, created: Boolean) {
                Log.d(TAG, "Logged into RevenueCat with user ID: $userId (created: $created)")
                onComplete?.invoke(customerInfo)
            }

            override fun onError(error: PurchasesError) {
                Log.e(TAG, "Error logging in user to RevenueCat: ${error.message}")
                onComplete?.invoke(null)
            }
        })
    }

    /**
     * Reset RevenueCat user back to anonymous on logout
     */
    fun logOut(onComplete: (() -> Unit)? = null) {
        if (!Purchases.isConfigured) return
        Purchases.sharedInstance.logOut(object : ReceiveCustomerInfoCallback {
            override fun onReceived(customerInfo: CustomerInfo) {
                Log.d(TAG, "Logged out of RevenueCat")
                onComplete?.invoke()
            }

            override fun onError(error: PurchasesError) {
                Log.e(TAG, "Error logging out from RevenueCat: ${error.message}")
                onComplete?.invoke()
            }
        })
    }
}
