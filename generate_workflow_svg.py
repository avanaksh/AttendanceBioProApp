import os

def create_workflow_svg():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="background:#0a0e17; font-family:'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <!-- Background Grid Pattern -->
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#111827" stroke-width="1" stroke-opacity="0.6"/>
    </pattern>

    <!-- Radial Top Glow -->
    <radialGradient id="topGlow" cx="50%" cy="0%" r="50%">
      <stop offset="0%" stop-color="#4f46e5" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#0a0e17" stop-opacity="0"/>
    </radialGradient>

    <!-- Glow filters -->
    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background Layer -->
  <rect width="1920" height="1080" fill="#0a0e17"/>
  <rect width="1920" height="1080" fill="url(#grid)"/>
  <rect width="1920" height="400" fill="url(#topGlow)"/>

  <!-- ==================== HEADER ==================== -->
  <g transform="translate(960, 45)" text-anchor="middle">
    <!-- Top Pill -->
    <rect x="-180" y="-14" width="360" height="28" rx="8" fill="#1e1b4b" stroke="#6366f1" stroke-width="1"/>
    <text y="5" fill="#a5b4fc" font-size="11" font-weight="700" letter-spacing="1.5">INSTITUTIONAL GRADE • ARCHITECTURAL WORKFLOW</text>

    <!-- Title -->
    <text y="48" fill="#ffffff" font-size="36" font-weight="800" letter-spacing="-0.5">AttendanceApp and Quorum Voting System</text>

    <!-- Subtitle -->
    <text y="78" fill="#94a3b8" font-size="15" font-weight="400">End-to-End Operational Workflow • Biometric Eye-Blink Liveness • 100% Offline SQLite • RevenueCat Multi-Store Subscriptions</text>
  </g>

  <!-- Badges Row -->
  <g transform="translate(960, 155)" text-anchor="middle" font-size="11" font-weight="700">
    <g transform="translate(-560, 0)">
      <rect x="-90" y="-12" width="180" height="26" rx="6" fill="#10b981" fill-opacity="0.12" stroke="#34d399" stroke-width="1"/>
      <text y="5" fill="#34d399">[LOCAL-FIRST] 100% SQLite</text>
    </g>
    <g transform="translate(-340, 0)">
      <rect x="-105" y="-12" width="210" height="26" rx="6" fill="#06b6d4" fill-opacity="0.12" stroke="#67e8f9" stroke-width="1"/>
      <text y="5" fill="#67e8f9">[AI VISION] Eye-Blink Liveness</text>
    </g>
    <g transform="translate(-110, 0)">
      <rect x="-115" y="-12" width="230" height="26" rx="6" fill="#6366f1" fill-opacity="0.12" stroke="#a5b4fc" stroke-width="1"/>
      <text y="5" fill="#a5b4fc">[SECURITY] Strict 3-Step Sequence</text>
    </g>
    <g transform="translate(130, 0)">
      <rect x="-115" y="-12" width="230" height="26" rx="6" fill="#f59e0b" fill-opacity="0.12" stroke="#fcd34d" stroke-width="1"/>
      <text y="5" fill="#fcd34d">[PARLIAMENT] Quorum Presence Lock</text>
    </g>
    <g transform="translate(370, 0)">
      <rect x="-115" y="-12" width="230" height="26" rx="6" fill="#ec4899" fill-opacity="0.12" stroke="#f9a8d4" stroke-width="1"/>
      <text y="5" fill="#f9a8d4">[COMMERCE] RevenueCat Dual Store</text>
    </g>
    <g transform="translate(595, 0)">
      <rect x="-95" y="-12" width="190" height="26" rx="6" fill="#8b5cf6" fill-opacity="0.12" stroke="#c4b5fd" stroke-width="1"/>
      <text y="5" fill="#c4b5fd">[LEANBACK] Fire TV Ready</text>
    </g>
  </g>

  <!-- ==================== 4 TOP STAGE CARDS ==================== -->
  <!-- Card 1: Stage 1 -->
  <g transform="translate(68, 178)">
    <rect width="415" height="492" rx="12" fill="#111827" fill-opacity="0.94" stroke="#6366f1" stroke-opacity="0.6" stroke-width="1"/>
    <line x1="12" y1="0" x2="403" y2="0" stroke="#818cf8" stroke-width="3"/>
    
    <rect x="18" y="18" width="68" height="22" rx="6" fill="#6366f1"/>
    <text x="52" y="34" fill="#ffffff" font-size="11" font-weight="700" text-anchor="middle">STAGE 1</text>
    
    <text x="18" y="68" fill="#ffffff" font-size="18" font-weight="700">Organization and Identity</text>
    <text x="18" y="88" fill="#818cf8" font-size="12" font-weight="600">Multi-Tenant Selection and Session Setup</text>
    <line x1="18" y1="98" x2="397" y2="98" stroke="#1e293b" stroke-width="1"/>

    <!-- Items -->
    <g transform="translate(18, 112)">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#818cf8" stroke-width="1"/>
        <text x="10" y="13" fill="#818cf8" font-size="10" font-weight="700" text-anchor="middle">01</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Institutional Org Routing</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Select jurisdiction: Supreme Court, High Court, Election</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">Commission, Bar Council, or custom state entity.</text>
      </g>
      <!-- Item 2 -->
      <g transform="translate(0, 76)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#818cf8" stroke-width="1"/>
        <text x="10" y="13" fill="#818cf8" font-size="10" font-weight="700" text-anchor="middle">02</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Role-Based Privilege Dispatch</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Dispatches to Member Portal (Duty execution, Voting) or</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">Admin Portal (Audits, Shift alterations, CSV export).</text>
      </g>
      <!-- Item 3 -->
      <g transform="translate(0, 152)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#818cf8" stroke-width="1"/>
        <text x="10" y="13" fill="#818cf8" font-size="10" font-weight="700" text-anchor="middle">03</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Dynamic Shift Window Sync</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Calculates morning (09:00 - 13:00) and evening</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">(16:00 - 19:00) strict duty thresholds dynamically.</text>
      </g>
      <!-- Item 4 -->
      <g transform="translate(0, 228)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#818cf8" stroke-width="1"/>
        <text x="10" y="13" fill="#818cf8" font-size="10" font-weight="700" text-anchor="middle">04</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">RevenueCat Subscription Check</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Queries on-device cached entitlement and 7-Day trial</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">countdown timer before starting shift duty.</text>
      </g>
    </g>

    <rect x="18" y="450" width="379" height="26" rx="6" fill="#1e1b4b" stroke="#6366f1" stroke-width="1"/>
    <text x="28" y="467" fill="#a5b4fc" font-size="11" font-weight="700">READY: Awaiting Morning Check-In</text>
  </g>

  <!-- Chevron Connector 1 -->
  <g transform="translate(504, 424)">
    <circle r="16" fill="#111827" stroke="#06b6d4" stroke-width="1"/>
    <polygon points="-4,-7 5,0 -4,7" fill="#22d3ee"/>
    <rect x="-18" y="24" width="36" height="16" rx="4" fill="#0f172a" fill-opacity="0.8"/>
    <text y="36" fill="#94a3b8" font-size="10" font-weight="700" text-anchor="middle">NEXT</text>
  </g>

  <!-- Card 2: Stage 2 (Step 1) -->
  <g transform="translate(525, 178)">
    <rect width="415" height="492" rx="12" fill="#111827" fill-opacity="0.94" stroke="#06b6d4" stroke-opacity="0.6" stroke-width="1"/>
    <line x1="12" y1="0" x2="403" y2="0" stroke="#22d3ee" stroke-width="3"/>
    
    <rect x="18" y="18" width="112" height="22" rx="6" fill="#06b6d4"/>
    <text x="74" y="34" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">STAGE 2 • STEP 1</text>
    
    <text x="18" y="68" fill="#ffffff" font-size="18" font-weight="700">Morning Check-In</text>
    <text x="18" y="88" fill="#22d3ee" font-size="12" font-weight="600">Facial Liveness and Geofencing Verification</text>
    <line x1="18" y1="98" x2="397" y2="98" stroke="#1e293b" stroke-width="1"/>

    <!-- Items -->
    <g transform="translate(18, 112)">
      <g transform="translate(0, 0)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#22d3ee" stroke-width="1"/>
        <text x="10" y="13" fill="#22d3ee" font-size="10" font-weight="700" text-anchor="middle">01</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">CameraX Eye-Blink AI Analysis</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Google MLKit analyzes live Eye Aspect Ratio (EAR).</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">Requires confirmed blinks to block static photos/screens.</text>
      </g>
      <g transform="translate(0, 76)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#22d3ee" stroke-width="1"/>
        <text x="10" y="13" fill="#22d3ee" font-size="10" font-weight="700" text-anchor="middle">02</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Precise Geofence GPS Lock</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Device GPS validated against registered institution</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">perimeter (andlt;50m). Rejects off-site attempts.</text>
      </g>
      <g transform="translate(0, 152)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#22d3ee" stroke-width="1"/>
        <text x="10" y="13" fill="#22d3ee" font-size="10" font-weight="700" text-anchor="middle">03</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Shift Window Time Validation</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Ensures member is checking in within active morning</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">duty hours before allowing sequence progression.</text>
      </g>
      <g transform="translate(0, 228)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#22d3ee" stroke-width="1"/>
        <text x="10" y="13" fill="#22d3ee" font-size="10" font-weight="700" text-anchor="middle">04</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Immutable Local SQLite Commit</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Commits encrypted check-in log with timestamp and</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">nature-of-work tag to on-device Room database.</text>
      </g>
    </g>

    <rect x="18" y="450" width="379" height="26" rx="6" fill="#083344" stroke="#06b6d4" stroke-width="1"/>
    <text x="28" y="467" fill="#67e8f9" font-size="11" font-weight="700">PASSED: Step 1 Duty Record Sealed</text>
  </g>

  <!-- Chevron Connector 2 -->
  <g transform="translate(961, 424)">
    <circle r="16" fill="#111827" stroke="#10b981" stroke-width="1"/>
    <polygon points="-4,-7 5,0 -4,7" fill="#34d399"/>
    <rect x="-18" y="24" width="36" height="16" rx="4" fill="#0f172a" fill-opacity="0.8"/>
    <text y="36" fill="#94a3b8" font-size="10" font-weight="700" text-anchor="middle">NEXT</text>
  </g>

  <!-- Card 3: Stage 3 (Step 2) -->
  <g transform="translate(982, 178)">
    <rect width="415" height="492" rx="12" fill="#111827" fill-opacity="0.94" stroke="#10b981" stroke-opacity="0.6" stroke-width="1"/>
    <line x1="12" y1="0" x2="403" y2="0" stroke="#34d399" stroke-width="3"/>
    
    <rect x="18" y="18" width="112" height="22" rx="6" fill="#10b981"/>
    <text x="74" y="34" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">STAGE 3 • STEP 2</text>
    
    <text x="18" y="68" fill="#ffffff" font-size="18" font-weight="700">Quorum and Voting Station</text>
    <text x="18" y="88" fill="#34d399" font-size="12" font-weight="600">Legislative Ballots and Presence Locking</text>
    <line x1="18" y1="98" x2="397" y2="98" stroke="#1e293b" stroke-width="1"/>

    <!-- Items -->
    <g transform="translate(18, 112)">
      <g transform="translate(0, 0)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
        <text x="10" y="13" fill="#34d399" font-size="10" font-weight="700" text-anchor="middle">01</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Sequence-Enforced Unlock</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Voting station strictly locked until Step 1 Morning Check-in</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">is fully validated and logged.</text>
      </g>
      <g transform="translate(0, 76)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
        <text x="10" y="13" fill="#34d399" font-size="10" font-weight="700" text-anchor="middle">02</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Secret Ballot and Resolutions</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Members cast Yes / No / Abstain ballots on active</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">parliamentary topics and assembly motions.</text>
      </g>
      <g transform="translate(0, 152)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
        <text x="10" y="13" fill="#34d399" font-size="10" font-weight="700" text-anchor="middle">03</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Real-Time Quorum Tracking</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Tallies attending voting members to verify legal</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">quorum compliance for valid proceedings.</text>
      </g>
      <g transform="translate(0, 228)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#34d399" stroke-width="1"/>
        <text x="10" y="13" fill="#34d399" font-size="10" font-weight="700" text-anchor="middle">04</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Abandonment Sentinel Protection</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Enforces voting before checkout; attempts to exit without</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">voting trigger discrepancy flags.</text>
      </g>
    </g>

    <rect x="18" y="450" width="379" height="26" rx="6" fill="#064e3b" stroke="#10b981" stroke-width="1"/>
    <text x="28" y="467" fill="#6ee7b7" font-size="11" font-weight="700">CONFIRMED: Quorum Vote Cast and Locked</text>
  </g>

  <!-- Chevron Connector 3 -->
  <g transform="translate(1418, 424)">
    <circle r="16" fill="#111827" stroke="#a855f7" stroke-width="1"/>
    <polygon points="-4,-7 5,0 -4,7" fill="#c084fc"/>
    <rect x="-18" y="24" width="36" height="16" rx="4" fill="#0f172a" fill-opacity="0.8"/>
    <text y="36" fill="#94a3b8" font-size="10" font-weight="700" text-anchor="middle">NEXT</text>
  </g>

  <!-- Card 4: Stage 4 (Step 3) -->
  <g transform="translate(1439, 178)">
    <rect width="415" height="492" rx="12" fill="#111827" fill-opacity="0.94" stroke="#a855f7" stroke-opacity="0.6" stroke-width="1"/>
    <line x1="12" y1="0" x2="403" y2="0" stroke="#c084fc" stroke-width="3"/>
    
    <rect x="18" y="18" width="112" height="22" rx="6" fill="#a855f7"/>
    <text x="74" y="34" fill="#ffffff" font-size="11" font-weight="700" text-anchor="middle">STAGE 4 • STEP 3</text>
    
    <text x="18" y="68" fill="#ffffff" font-size="18" font-weight="700">Evening Check-Out and Seal</text>
    <text x="18" y="88" fill="#c084fc" font-size="12" font-weight="600">Duty Verification and Final Record Lock</text>
    <line x1="18" y1="98" x2="397" y2="98" stroke="#1e293b" stroke-width="1"/>

    <!-- Items -->
    <g transform="translate(18, 112)">
      <g transform="translate(0, 0)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
        <text x="10" y="13" fill="#c084fc" font-size="10" font-weight="700" text-anchor="middle">01</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Secondary Biometric Verification</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Mandatory secondary eye-blink liveness capture validates</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">physical presence at evening departure.</text>
      </g>
      <g transform="translate(0, 76)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
        <text x="10" y="13" fill="#c084fc" font-size="10" font-weight="700" text-anchor="middle">02</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Shift Duration Consolidation</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Correlates morning entry, evening departure, vote</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">confirmation, and net verified duty hours.</text>
      </g>
      <g transform="translate(0, 152)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
        <text x="10" y="13" fill="#c084fc" font-size="10" font-weight="700" text-anchor="middle">03</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Cryptographic Record Lock</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Seals record in SQLite Room DB into immutable read-only</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">state, preventing tampering.</text>
      </g>
      <g transform="translate(0, 228)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#c084fc" stroke-width="1"/>
        <text x="10" y="13" fill="#c084fc" font-size="10" font-weight="700" text-anchor="middle">04</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Automated Discrepancy Evaluator</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Flags late departures, skipped votes, or short shifts</text>
        <text x="28" y="47" fill="#94a3b8" font-size="11">automatically for administrative audit.</text>
      </g>
    </g>

    <rect x="18" y="450" width="379" height="26" rx="6" fill="#3b0764" stroke="#a855f7" stroke-width="1"/>
    <text x="28" y="467" fill="#d8b4fe" font-size="11" font-weight="700">SEALED: Session Finalized and Tamper-Proof</text>
  </g>

  <!-- ==================== BOTTOM 2 ARCHITECTURE TIERS ==================== -->
  <!-- Bottom Left: Admin Portal -->
  <g transform="translate(68, 692)">
    <rect width="872" height="328" rx="12" fill="#111827" fill-opacity="0.94" stroke="#f59e0b" stroke-opacity="0.5" stroke-width="1"/>
    <line x1="12" y1="0" x2="860" y2="0" stroke="#f59e0b" stroke-width="3"/>

    <rect x="22" y="18" width="168" height="22" rx="6" fill="#f59e0b"/>
    <text x="106" y="34" fill="#0f172a" font-size="11" font-weight="700" text-anchor="middle">EXECUTIVE MANAGEMENT</text>

    <text x="22" y="68" fill="#ffffff" font-size="17" font-weight="700">Admin and Audit Intelligence Center</text>
    <text x="22" y="88" fill="#fbbf24" font-size="12" font-weight="600">100% Local SQLite • Tamper-Evident Audit Trails • DPAD / Leanback TV Support</text>
    <line x1="22" y1="98" x2="850" y2="98" stroke="#1e293b" stroke-width="1"/>

    <g transform="translate(22, 114)">
      <g transform="translate(0, 0)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
        <text x="10" y="13" fill="#f59e0b" font-size="10" font-weight="700" text-anchor="middle">01</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Real-Time Multi-Filter Search</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Search by Aadhaar number, member code, full name, shift status, or calendar date with instant sub-millisecond SQLite queries.</text>
      </g>
      <g transform="translate(0, 52)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
        <text x="10" y="13" fill="#f59e0b" font-size="10" font-weight="700" text-anchor="middle">02</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Official Occasion and Assembly Tagging</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Designate special sittings: National Holidays, Emergency Assembly, Budget Sessions, or Tribunal Sittings across records.</text>
      </g>
      <g transform="translate(0, 104)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
        <text x="10" y="13" fill="#f59e0b" font-size="10" font-weight="700" text-anchor="middle">03</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Discrepancy Resolution and Remark Override</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Detects abandonment, late morning check-ins, and early evening departures with official administrative override notes.</text>
      </g>
      <g transform="translate(0, 156)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
        <text x="10" y="13" fill="#f59e0b" font-size="10" font-weight="700" text-anchor="middle">04</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Direct On-Device CSV Export</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Generates compliant audit spreadsheets stored strictly on local device storage—zero external cloud dependency or data leak.</text>
      </g>
    </g>
  </g>

  <!-- Bottom Right: RevenueCat Subscriptions -->
  <g transform="translate(982, 692)">
    <rect width="872" height="328" rx="12" fill="#111827" fill-opacity="0.94" stroke="#ec4899" stroke-opacity="0.5" stroke-width="1"/>
    <line x1="12" y1="0" x2="860" y2="0" stroke="#ec4899" stroke-width="3"/>

    <rect x="22" y="18" width="168" height="22" rx="6" fill="#ec4899"/>
    <text x="106" y="34" fill="#ffffff" font-size="11" font-weight="700" text-anchor="middle">MONETIZATION and TRIALS</text>

    <text x="22" y="68" fill="#ffffff" font-size="17" font-weight="700">RevenueCat Multi-Store and Trial Safeguards</text>
    <text x="22" y="88" fill="#f472b6" font-size="12" font-weight="600">Dual Flavors: Google Play Store + Amazon Appstore • Live Expiration Alerts</text>
    <line x1="22" y1="98" x2="850" y2="98" stroke="#1e293b" stroke-width="1"/>

    <g transform="translate(22, 114)">
      <g transform="translate(0, 0)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#ec4899" stroke-width="1"/>
        <text x="10" y="13" fill="#ec4899" font-size="10" font-weight="700" text-anchor="middle">01</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">7-Day Free Trial Autonomous Countdown</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Autonomous local timer tracks remaining days with continuous in-app countdown badges across dashboard cards.</text>
      </g>
      <g transform="translate(0, 52)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#ec4899" stroke-width="1"/>
        <text x="10" y="13" fill="#ec4899" font-size="10" font-weight="700" text-anchor="middle">02</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Proactive Expiration Warnings (andlt;=2 Days)</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Triggers high-visibility warning banners and alert toasts when andlt;=2 days remain, preventing unexpected service interruption.</text>
      </g>
      <g transform="translate(0, 104)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#ec4899" stroke-width="1"/>
        <text x="10" y="13" fill="#ec4899" font-size="10" font-weight="700" text-anchor="middle">03</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Graceful Expiration Sentinel</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Upon 7-day lapse, automatically revokes Pro privileges and displays an actionable upgrade dialog leading to Paywall.</text>
      </g>
      <g transform="translate(0, 156)">
        <rect width="20" height="18" rx="4" fill="#1e293b" stroke="#ec4899" stroke-width="1"/>
        <text x="10" y="13" fill="#ec4899" font-size="10" font-weight="700" text-anchor="middle">04</text>
        <text x="28" y="14" fill="#f1f5f9" font-size="13" font-weight="700">Judge and Evaluator Bypass Mode</text>
        <text x="28" y="32" fill="#94a3b8" font-size="11">Accepts promo codes (JUDGE2026, REVENUECAT) and features offline demo sandbox mode for test evaluation without billing.</text>
      </g>
    </g>
  </g>

  <!-- ==================== FOOTER ==================== -->
  <text x="960" y="1055" fill="#64748b" font-size="12" font-weight="400" text-anchor="middle">Built with Kotlin 1.9 • Android Jetpack • Google CameraX and MLKit • Room SQLite Database • RevenueCat Purchases SDK • Amazon Appstore and Google Play Ready</text>
</svg>"""

    svg_paths = [
        r"C:\AttendanceApp_RevenueCat\workflow_diagram.svg",
        r"F:\AttendanceApp_RevenueCat\workflow_diagram.svg",
        r"C:\Users\HP\Desktop\attendance_store_assets\workflow_diagram.svg",
        r"C:\AttendanceApp_RevenueCat\google_play_assets\workflow_diagram.svg",
        r"C:\AttendanceApp_RevenueCat\amazon_store_assets\workflow_diagram.svg",
        r"C:\Users\HP\.gemini\antigravity-cli\brain\4515bfce-4739-4f4f-95c0-f93f8477fd2f\workflow_diagram.svg"
    ]
    for p in svg_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Saved SVG to: {p}")

if __name__ == "__main__":
    create_workflow_svg()
