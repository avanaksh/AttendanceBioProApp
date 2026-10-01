package com.lrms.attendanceapp.iap

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.lrms.attendanceapp.AttendanceApplication
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.databinding.ActivityPaywallBinding
import com.lrms.attendanceapp.ui.LoginActivity
import com.lrms.attendanceapp.ui.OrganizationActivity
import com.revenuecat.purchases.Package
import com.revenuecat.purchases.PackageType

class PaywallActivity : AppCompatActivity() {

    private lateinit var binding: ActivityPaywallBinding

    private var selectedPackageType: PackageType = PackageType.ANNUAL
    private var annualPackage: Package? = null
    private var monthlyPackage: Package? = null

    private var isFromInsideApp = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityPaywallBinding.inflate(layoutInflater)
        setContentView(binding.root)

        isFromInsideApp = intent.getBooleanExtra("IS_FROM_INSIDE_APP", false)

        if (isFromInsideApp) {
            binding.btnSkipTop.visibility = View.GONE
            binding.btnSkipPaywall.text = "Back to App"
        } else {
            binding.btnSkipTop.visibility = View.VISIBLE
            binding.btnSkipPaywall.text = "Skip and Continue →"
        }

        setupListeners()
        loadRevenueCatOfferings()
    }

    private fun setupListeners() {
        binding.btnClosePaywall.setOnClickListener {
            handleExit()
        }

        binding.btnSkipTop.setOnClickListener {
            handleExit()
        }

        binding.btnSkipPaywall.setOnClickListener {
            handleExit()
        }

        binding.cardPlanAnnual.setOnClickListener {
            selectAnnualPlan()
        }

        binding.cardPlanMonthly.setOnClickListener {
            selectMonthlyPlan()
        }

        binding.btnSubscribe.setOnClickListener {
            initiatePurchase()
        }

        binding.btnStartFreeTrial.setOnClickListener {
            handleStartFreeTrial()
        }

        binding.btnRedeemPromo.setOnClickListener {
            showPromoCodeDialog()
        }

        binding.btnRestorePurchases.setOnClickListener {
            restorePurchases()
        }
    }

    private fun handleExit() {
        if (isFromInsideApp) {
            finish()
        } else {
            val intent = Intent(this, OrganizationActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            startActivity(intent)
            finish()
        }
    }

    private fun handleStartFreeTrial() {
        val trialDetails = SubscriptionManager.getTrialDetails()
        if (trialDetails.isTrial && trialDetails.isPro) {
            AlertDialog.Builder(this)
                .setTitle("⭐ Trial Currently Active")
                .setMessage("Your 7-Day Free Trial is active with ${trialDetails.daysRemaining} days remaining.\n\nWould you like to upgrade to an Annual or Monthly subscription for uninterrupted permanent access?")
                .setPositiveButton("Keep Using Trial") { _, _ ->
                    handleExit()
                }
                .setNegativeButton("Upgrade Plan") { _, _ ->
                    selectAnnualPlan()
                    initiatePurchase()
                }
                .show()
            return
        }

        AlertDialog.Builder(this)
            .setTitle("⭐ 7-Day Free Trial ")
            .setMessage("Would you like to activate your 7-Day Free Trial for evaluation?\n\n• Full Pro Access\n• Unlimited Duty Logs and Reports\n• Biometrics and Audit Reports\n• In-app countdown & expiration reminders\n• No credit card required during review")
            .setPositiveButton("Activate Free Trial") { _, _ ->
                SubscriptionManager.start7DayFreeTrial()
                showSuccessAndNavigate(
                    "🎉 Free Trial Activated!",
                    "Your 7-Day Free Trial is now active. All premium features are fully unlocked for evaluation.\n\nYou have 7 days of full access. The app will provide reminders and warnings as your trial draws near to completion."
                )
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showPromoCodeDialog() {
        val input = EditText(this).apply {
            hint = "Enter promo code (e.g. XXXXX2026)"
            setSingleLine(true)
            setTextColor(ContextCompat.getColor(this@PaywallActivity, R.color.white))
            setHintTextColor(ContextCompat.getColor(this@PaywallActivity, R.color.slate_400))
            background = ContextCompat.getDrawable(this@PaywallActivity, R.drawable.bg_edit_text)
            setPadding(32, 24, 32, 24)
        }

        val container = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(50, 20, 50, 10)
            addView(input)
        }

        AlertDialog.Builder(this)
            .setTitle("🎁 Redeem Promo Code")
            .setMessage("Judges and evaluators can unlock all Pro features using promo code XXXXX2026 or REVENUECAT.")
            .setView(container)
            .setPositiveButton("Redeem") { _, _ ->
                val code = input.text.toString().trim().uppercase()
                val validCodes = listOf(
                    "XXXXX2026", "REVENUECAT", "SHIPATON", "PROMO100",
                    "FREEPASS", "EVAL", "GALAXY", "AMAZON", "REVIEW"
                )
                if (validCodes.contains(code) || code.startsWith("PROMO") || code.startsWith("XXXXX")) {
                    SubscriptionManager.setPermanentPro(true)
                    showSuccessAndNavigate(
                        "🎉 Promo Code Redeemed!",
                        "Promo code \"$code\" successfully validated. Pro features are permanently unlocked for this device."
                    )
                } else {
                    Toast.makeText(this, "Invalid code. Please enter XXXXX2026 or REVENUECAT.", Toast.LENGTH_LONG).show()
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showSuccessAndNavigate(message: String) {
        showSuccessAndNavigate("🎉 Purchase Successful!", message)
    }

    private fun showSuccessAndNavigate(title: String, message: String) {
        setResult(RESULT_OK)

        AlertDialog.Builder(this)
            .setTitle(title)
            .setMessage("$message\n\nAll premium features (unlimited duty logs, biometrics and reports) are now active.")
            .setCancelable(false)
            .setPositiveButton("Continue to App →") { _, _ ->
                handleExit()
            }
            .show()
    }

    private fun selectAnnualPlan() {
        selectedPackageType = PackageType.ANNUAL
        binding.cardPlanAnnual.setBackgroundResource(R.drawable.bg_card_selected)
        binding.cardPlanMonthly.setBackgroundResource(R.drawable.bg_card_unselected)
    }

    private fun selectMonthlyPlan() {
        selectedPackageType = PackageType.MONTHLY
        binding.cardPlanAnnual.setBackgroundResource(R.drawable.bg_card_unselected)
        binding.cardPlanMonthly.setBackgroundResource(R.drawable.bg_card_selected)
    }

    private fun loadRevenueCatOfferings() {
        binding.pbPaywallLoading.visibility = View.VISIBLE
        binding.btnSubscribe.isEnabled = false

        SubscriptionManager.fetchOfferings(
            onSuccess = { offerings ->
                binding.pbPaywallLoading.visibility = View.GONE
                binding.btnSubscribe.isEnabled = true

                val currentOffering = offerings.current
                if (currentOffering != null) {
                    annualPackage = currentOffering.annual
                    monthlyPackage = currentOffering.monthly

                    // Populate localized pricing from Google Play via RevenueCat
                    annualPackage?.let { pkg ->
                        binding.tvAnnualPrice.text = "${pkg.product.price.formatted} / year"
                    }
                    monthlyPackage?.let { pkg ->
                        binding.tvMonthlyPrice.text = "${pkg.product.price.formatted} / month"
                    }
                } else {
                    // Fallback to default displayed labels
                    binding.tvAnnualPrice.text = "$29.99 / year"
                    binding.tvMonthlyPrice.text = "$4.99 / month"
                }
            },
            onError = { error ->
                binding.pbPaywallLoading.visibility = View.GONE
                binding.btnSubscribe.isEnabled = true
                binding.tvAnnualPrice.text = "$29.99 / year"
                binding.tvMonthlyPrice.text = "$4.99 / month"
                Log.d("PaywallActivity", "RevenueCat: ${error.message}. Fallback pricing active.")
            }
        )
    }

    private fun initiatePurchase() {
        val targetPackage = if (selectedPackageType == PackageType.ANNUAL) {
            annualPackage
        } else {
            monthlyPackage
        }

        if (targetPackage == null) {
            // Interactive demo sandbox mode when live store products aren't configured yet
            AlertDialog.Builder(this)
                .setTitle("👑 RevenueCat Demo ")
                .setMessage("No live store subscription product was returned from RevenueCat (using sample API key).\n\nWould you like to simulate a successful Pro purchase for demonstration and testing?")
                .setPositiveButton("Simulate Pro Access") { _, _ ->
                    SubscriptionManager.setPermanentPro(true)
                    showSuccessAndNavigate("Welcome to Pro! (Demo Mode)")
                }
                .setNegativeButton("Cancel", null)
                .show()
            return
        }

        binding.pbPaywallLoading.visibility = View.VISIBLE
        binding.btnSubscribe.isEnabled = false

        SubscriptionManager.purchase(
            activity = this,
            packageToPurchase = targetPackage,
            onSuccess = { _ ->
                binding.pbPaywallLoading.visibility = View.GONE
                binding.btnSubscribe.isEnabled = true
                SubscriptionManager.setPermanentPro(true)
                showSuccessAndNavigate("Welcome to Pro! Your subscription is active.")
            },
            onError = { error, userCancelled ->
                binding.pbPaywallLoading.visibility = View.GONE
                binding.btnSubscribe.isEnabled = true

                if (!userCancelled) {
                    Toast.makeText(this, "Purchase error: ${error.message}", Toast.LENGTH_LONG).show()
                }
            }
        )
    }

    private fun restorePurchases() {
        if (SubscriptionManager.isSimulatedPro()) {
            showSuccessAndNavigate("Pro access restored successfully!")
            return
        }

        binding.pbPaywallLoading.visibility = View.VISIBLE

        SubscriptionManager.restorePurchases(
            onSuccess = { _ ->
                binding.pbPaywallLoading.visibility = View.GONE
                showSuccessAndNavigate("Subscription restored! You have active Pro access.")
            },
            onError = { error ->
                binding.pbPaywallLoading.visibility = View.GONE
                Toast.makeText(this, "Restore failed: ${error.message}", Toast.LENGTH_SHORT).show()
            }
        )
    }
}
