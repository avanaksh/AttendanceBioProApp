### How Building in Public Improved BioCheck Pro

1. **Critical Feature Pivot (Offline-First Architecture):**  
   When we shared our initial cloud-based architecture, community feedback from contractors and managers highlighted that frontline workers frequently operate in basements, construction zones, and rural sites with spotty or zero cellular reception. In response, we completely re-engineered the biometric engine to run **100% on-device edge AI facial recognition** with local SQLite storage, eliminating cloud latency and offline failures.

2. **Multi-Store Hardware Realities:**  
   Public discussions around wall-mounted time clocks revealed that many small businesses prefer inexpensive tablets (such as Amazon Fire OS devices) rather than high-end iPads or Galaxy tabs. This prompted us to build a **multi-flavor build architecture** supporting both Google Play and Amazon Appstore with store-specific RevenueCat billing SDK configurations.

3. **Soft-Gating & Paywall UX Optimization:**  
   Fellow builders on Discord and X provided candid feedback about paywall fatigue. Instead of an aggressive hard gate at first launch, we adopted a **product-led soft paywall**: a free tier for up to 5 staff, gating only advanced features (unlimited staff, CSV/PDF payroll exports) at the exact moment managers experience real value.

4. **Accountability & Velocity:**  
   Posting progress under `#Shipaton` provided continuous motivation and prevented scope creep, forcing us to maintain high shipping momentum and deliver a production-hardened app within the hackathon window.
