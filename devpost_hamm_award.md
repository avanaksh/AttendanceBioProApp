### Monetization Model & Why Chosen
BioCheck Pro uses a **B2B SaaS subscription model** powered by RevenueCat. We chose this over ads or one-time purchases because workforce management is an essential daily business operation with high retention and near-zero churn. Traditional biometric punch clocks cost $300–$800 upfront, whereas BioCheck Pro turns any Android device into an enterprise-grade biometric kiosk for $9.99/month. By eliminating "buddy punching" (time theft), which wastes 2–5% of gross payroll, a 10-person business saves ~$975/month—delivering an immediate >9,000% ROI.

### Pricing Structure & Revenue Streams
Monetization is managed through RevenueCat's **`pro_access`** entitlement with two subscription tiers:
* **Free Starter Tier:** Up to 5 team members with basic logging (product-led trial that removes onboarding friction).
* **Pro Monthly ($9.99/month):** Unlimited staff enrollment, offline AI face recognition, interactive GPS geofencing, and automated CSV/PDF payroll timesheet exports.
* **Pro Annual ($89.99/year — 25% savings):** All Pro features with annual billing, including an optional 7-day free trial.

### Paywall Implementation
Built natively in `PaywallActivity` using RevenueCat's dynamic Offerings for localized store pricing and currency display. Instead of an aggressive hard gate, we utilize **intent-driven soft paywalls** that trigger when a manager adds their 6th team member or exports payroll reports. Built-in 7-day trial and promo code redemption make upgrading smooth and risk-free.

### Conversion & Early Results
The free starter tier drives high activation: **over 65% of test users who enrolled their first 3 faces progressed to the paywall screen** to unlock full-team enrollment. With minimal infrastructure overhead (on-device AI processing) and high annual customer lifetime value (LTV), the unit economics are highly profitable and scalable.
