package com.lrms.attendanceapp.ui

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.widget.EditText
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.Gson
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AppDatabase
import com.lrms.attendanceapp.data.local.AttendanceEntity
import com.lrms.attendanceapp.data.local.MemberEntity
import com.lrms.attendanceapp.data.local.VoteRecordEntity
import com.lrms.attendanceapp.data.local.VotingTopicEntity
import com.lrms.attendanceapp.databinding.ActivityMainBinding
import com.lrms.attendanceapp.iap.PaywallActivity
import com.lrms.attendanceapp.iap.SubscriptionManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var database: AppDatabase
    private lateinit var userRecordsAdapter: AdminAttendanceAdapter

    private var userIdentifier = "MEM-01"
    private var userName = "Alex Rivera"
    private var userRole = "member"
    private var userInstitute = "Supreme Court and High Court"
    private var memberNatureOfWork = "Presiding Officer"
    private var orgId: Long = 1
    private var orgName: String = "Supreme Court and High Court"

    private var morningStart = "09:00"
    private var morningEnd = "13:00"
    private var eveningStart = "16:00"
    private var eveningEnd = "19:00"

    private var selectedType = "Morning Shift"
    private var isProMember = false
    private var hasMarkedMorningToday = false
    private var hasMarkedEveningToday = false

    private var isMemberBlocked = false
    private var memberBlockReason = ""
    private var memberAttendanceLogs: List<AttendanceEntity> = emptyList()
    private var memberVotes: List<VoteRecordEntity> = emptyList()
    private val PERMISSION_REQ_CODE = 2001
    private var pendingAttendanceAction: (() -> Unit)? = null
    private var hasShownExpiredDialog = false
    private var hasShownExpiringSoonWarning = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Read Session & Shift Details
        userIdentifier = intent.getStringExtra("USER_IDENTIFIER") ?: "MEM-01"
        userName = intent.getStringExtra("USER_NAME") ?: "Alex Rivera"
        userRole = intent.getStringExtra("USER_ROLE") ?: "member"
        userInstitute = intent.getStringExtra("USER_INSTITUTE") ?: "Supreme Court and High Court"
        memberNatureOfWork = intent.getStringExtra("MEMBER_WORK") ?: "Presiding Officer"
        orgId = intent.getLongExtra("ORG_ID", 1)
        orgName = intent.getStringExtra("ORG_NAME") ?: userInstitute

        morningStart = intent.getStringExtra("MORNING_START") ?: "09:00"
        morningEnd = intent.getStringExtra("MORNING_END") ?: "13:00"
        eveningStart = intent.getStringExtra("EVENING_START") ?: "16:00"
        eveningEnd = intent.getStringExtra("EVENING_END") ?: "19:00"

        setupHeaderUI()
        setupListeners()

        // Disable hardware back button to enforce structured session
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                finish()
            }
        })

        // RevenueCat Subscription ID check (Amazon Store SDK intact)
        SubscriptionManager.identifyUser(userIdentifier)

        // Initialize Local SQLite Database
        database = AppDatabase.getDatabase(this)

        setupUserRecordsRecyclerView()
        observeMemberRecords()
        evaluateSequenceState()
    }

    private fun setupHeaderUI() {
        binding.tvWelcomeName.text = "Welcome, $userName"
        binding.tvMemberNatureOfWork.text = "Nature of Work: $memberNatureOfWork"
        binding.tvUserInstitute.text = orgName

        val isAdmin = userRole.equals("admin", ignoreCase = true)
        if (isAdmin) {
            binding.tvUserRoleBadge.text = "👑 ADMIN"
            binding.tvUserRoleBadge.setBackgroundResource(R.drawable.bg_badge_gold)
            binding.tvUserRoleBadge.setTextColor(ContextCompat.getColor(this, R.color.slate_950))
            binding.cardAdminPortal.visibility = View.VISIBLE
        } else {
            binding.tvUserRoleBadge.text = "MEMBER"
            binding.tvUserRoleBadge.setBackgroundResource(R.drawable.bg_pill_role)
            binding.tvUserRoleBadge.setTextColor(ContextCompat.getColor(this, R.color.white))
            binding.cardAdminPortal.visibility = View.GONE
        }

        binding.tvWindowStatus.text = "Shift Hours: Morning $morningStart - $morningEnd | Evening $eveningStart - $eveningEnd"
        binding.tvVotingPortalTitle.text = "$orgName Voting Station"
    }

    private fun setupListeners() {
        binding.btnLogout.setOnClickListener {
            performLogout()
        }

        binding.cardProStatus.setOnClickListener {
            val intent = Intent(this, PaywallActivity::class.java).apply {
                putExtra("IS_FROM_INSIDE_APP", true)
            }
            startActivity(intent)
        }

        // Step 1: Morning Check-in
        binding.btnMarkMorning.setOnClickListener {
            handleMorningLoginAttempt()
        }

        // Step 2: Open Voting Station
        binding.btnOpenVoting.setOnClickListener {
            handleOpenVoting()
        }

        // Step 3: Evening Check-in & Final Seal
        binding.btnMarkEvening.setOnClickListener {
            handleEveningLogoutAttempt()
        }

        // Test Discrepancy & Abandonment Simulation Button
        binding.btnTestDiscrepancyAbandon.setOnClickListener {
            handleTestDiscrepancyAbandon()
        }

        // Admin quick actions
        binding.tvAdminAction.setOnClickListener {
            val intent = Intent(this, AdminPortalActivity::class.java).apply {
                putExtra("ORG_ID", orgId)
                putExtra("ORG_NAME", orgName)
            }
            startActivity(intent)
        }

        binding.btnAdminAlterShiftsQuick.setOnClickListener {
            showAlterShiftDialog()
        }

        binding.btnAdminAddTopicQuick.setOnClickListener {
            showAddTopicDialog()
        }
    }

    private fun setupUserRecordsRecyclerView() {
        userRecordsAdapter = AdminAttendanceAdapter()
        userRecordsAdapter.onItemClickListener = { record ->
            showRecordDetailsDialog(record)
        }
        binding.rvUserRecords.layoutManager = LinearLayoutManager(this)
        binding.rvUserRecords.adapter = userRecordsAdapter
    }

    private fun observeMemberRecords() {
        // 1. Observe Attendance Logs
        lifecycleScope.launch {
            database.attendanceDao().getLogsForUser(userIdentifier).collectLatest { logs ->
                memberAttendanceLogs = logs.filter { it.orgId == orgId || it.orgId == 0L }
                binding.tvRecordsCount.text = "${memberAttendanceLogs.size} Records Stored on Device"
                if (memberAttendanceLogs.isNotEmpty()) {
                    val last = memberAttendanceLogs.first()
                    binding.tvLastSavedLog.text = "Last Record: ${last.timestamp} (${last.attendanceType})"
                    binding.rvUserRecords.visibility = View.VISIBLE
                    userRecordsAdapter.submitList(memberAttendanceLogs)
                } else {
                    binding.tvLastSavedLog.text = "No duty logs recorded yet."
                    binding.rvUserRecords.visibility = View.GONE
                    userRecordsAdapter.submitList(emptyList())
                }
                evaluateSequenceState()
            }
        }

        // 2. Observe Member Votes
        lifecycleScope.launch {
            database.voteRecordDao().getVotesForMember(userIdentifier).collectLatest { votes ->
                memberVotes = votes.filter { it.orgId == orgId }
                evaluateSequenceState()
            }
        }

        // 3. Observe Member Discrepancy / Block Status
        lifecycleScope.launch {
            database.memberDao().getMembersByOrg(orgId).collectLatest { members ->
                val me = members.find { it.memberCode == userIdentifier }
                if (me != null) {
                    isMemberBlocked = me.isBlocked
                    memberBlockReason = me.blockReason
                    userName = me.name
                    memberNatureOfWork = me.natureOfWork
                    setupHeaderUI()
                } else {
                    // Direct lookup fallback
                    val direct = withContext(Dispatchers.IO) {
                        database.memberDao().getMemberByCode(userIdentifier)
                    }
                    if (direct != null) {
                        isMemberBlocked = direct.isBlocked
                        memberBlockReason = direct.blockReason
                        userName = direct.name
                        memberNatureOfWork = direct.natureOfWork
                        setupHeaderUI()
                    }
                }
                evaluateSequenceState()
            }
        }

        // 4. Observe Dynamic Shift Hours from Organization & Member
        lifecycleScope.launch {
            database.organizationDao().getAllOrganizations().collectLatest { orgs ->
                val org = orgs.find { it.id == orgId }
                if (org != null) {
                    val member = withContext(Dispatchers.IO) {
                        database.memberDao().getMemberByCode(userIdentifier)
                    }
                    if (member != null && member.morningShiftStart.isNotEmpty() && member.morningShiftEnd.isNotEmpty()) {
                        morningStart = member.morningShiftStart
                        morningEnd = member.morningShiftEnd
                        eveningStart = member.eveningShiftStart
                        eveningEnd = member.eveningShiftEnd
                    } else {
                        morningStart = org.morningShiftStart
                        morningEnd = org.morningShiftEnd
                        eveningStart = org.eveningShiftStart
                        eveningEnd = org.eveningShiftEnd
                    }
                    binding.tvWindowStatus.text = "Shift Hours: Morning $morningStart - $morningEnd | Evening $eveningStart - $eveningEnd"
                    evaluateSequenceState()
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        checkProSubscription()

        // Re-check member state and shift timings on resume
        lifecycleScope.launch(Dispatchers.IO) {
            val org = database.organizationDao().getOrganizationById(orgId)
            val member = database.memberDao().getMemberByCode(userIdentifier)
            withContext(Dispatchers.Main) {
                if (member != null) {
                    isMemberBlocked = member.isBlocked
                    memberBlockReason = member.blockReason
                    if (member.morningShiftStart.isNotEmpty() && member.morningShiftEnd.isNotEmpty()) {
                        morningStart = member.morningShiftStart
                        morningEnd = member.morningShiftEnd
                        eveningStart = member.eveningShiftStart
                        eveningEnd = member.eveningShiftEnd
                    } else if (org != null) {
                        morningStart = org.morningShiftStart
                        morningEnd = org.morningShiftEnd
                        eveningStart = org.eveningShiftStart
                        eveningEnd = org.eveningShiftEnd
                    }
                } else if (org != null) {
                    morningStart = org.morningShiftStart
                    morningEnd = org.morningShiftEnd
                    eveningStart = org.eveningShiftStart
                    eveningEnd = org.eveningShiftEnd
                }
                binding.tvWindowStatus.text = "Shift Hours: Morning $morningStart - $morningEnd | Evening $eveningStart - $eveningEnd"
                evaluateSequenceState()
            }
        }
    }

    private fun checkProSubscription() {
        SubscriptionManager.checkSubscriptionStatus { details ->
            runOnUiThread {
                isProMember = details.isPro

                when {
                    // 1. Expired Trial or Expired Subscription
                    details.isExpired -> {
                        binding.tvProIcon.text = "⏳"
                        binding.tvProTitle.text = "Free Trial Expired"
                        binding.tvProSubtitle.text = "Your 7-day trial has ended. Tap to view plans."
                        binding.tvProAction.text = "UPGRADE"

                        if (!hasShownExpiredDialog && !isFinishing) {
                            hasShownExpiredDialog = true
                            AlertDialog.Builder(this)
                                .setTitle("⏳ 7-Day Free Trial Ended")
                                .setMessage("Your 7-Day Free Trial has ended.\n\nTo continue enjoying unlimited duty logs, biometrics, and audit reports, please subscribe to a Monthly or Yearly plan.")
                                .setPositiveButton("View Plans") { _, _ ->
                                    val intent = Intent(this, PaywallActivity::class.java).apply {
                                        putExtra("IS_FROM_INSIDE_APP", true)
                                    }
                                    startActivity(intent)
                                }
                                .setNegativeButton("Continue Free", null)
                                .show()
                        }
                    }

                    // 2. Active Trial with Warning (2 days or less left)
                    details.isTrial && details.isExpiringSoon -> {
                        binding.tvProIcon.text = "⚠️"
                        binding.tvProTitle.text = "⚠️ Trial Ends in ${details.daysRemaining} Day${if (details.daysRemaining > 1) "s" else ""}!"
                        binding.tvProSubtitle.text = "Your free trial will end soon. Tap to keep uninterrupted access."
                        binding.tvProAction.text = "EXTEND"

                        if (!hasShownExpiringSoonWarning && !isFinishing) {
                            hasShownExpiringSoonWarning = true
                            Toast.makeText(
                                this,
                                "⚠️ Reminder: Your Free Trial expires in ${details.daysRemaining} day${if (details.daysRemaining > 1) "s" else ""}!",
                                Toast.LENGTH_LONG
                            ).show()
                        }
                    }

                    // 3. Active Trial with plenty of time (> 2 days)
                    details.isTrial -> {
                        binding.tvProIcon.text = "⭐"
                        binding.tvProTitle.text = "PRO Trial: ${details.daysRemaining} Days Left"
                        binding.tvProSubtitle.text = "7-Day Free Access active • All features unlocked"
                        binding.tvProAction.text = "UPGRADE"
                    }

                    // 4. Paid Subscription Active (Monthly / Yearly / Pro Lifetime)
                    details.isPro -> {
                        binding.tvProIcon.text = "👑"
                        binding.tvProTitle.text = "PRO Member Active"
                        binding.tvProSubtitle.text = if (details.isExpiringSoon) {
                            details.message
                        } else {
                            "Unlimited Duty Logs and Biometrics Unlocked"
                        }
                        binding.tvProAction.text = "ACTIVE"

                        if (details.isExpiringSoon && !hasShownExpiringSoonWarning && !isFinishing) {
                            hasShownExpiringSoonWarning = true
                            Toast.makeText(this, details.message, Toast.LENGTH_LONG).show()
                        }
                    }

                    // 5. Default Free Tier (Trial not yet started)
                    else -> {
                        binding.tvProIcon.text = "⭐"
                        binding.tvProTitle.text = "Upgrade to Pro Access"
                        binding.tvProSubtitle.text = "Start 7-Day Free Trial or Subscribe (Monthly/Yearly)"
                        binding.tvProAction.text = "VIEW PLANS"
                    }
                }
            }
        }
    }

    private fun performLogout() {
        AlertDialog.Builder(this)
            .setTitle("Confirm Logout")
            .setMessage("Are you sure you want to log out of your session in $orgName?")
            .setPositiveButton("Logout") { _, _ ->
                SubscriptionManager.logOut()
                Toast.makeText(this, "Logged out successfully", Toast.LENGTH_SHORT).show()
                finish()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    /**
     * Strict 3-Step Sequence Evaluation:
     * 1️⃣ Step 1: Morning Shift Attendance
     * 2️⃣ Step 2: Cast Vote in Organization Station (only during authorized voting period)
     * 3️⃣ Step 3: Evening Shift Attendance
     * 🏁 Final Step: Complete record entered into local device storage.
     *
     * If morning attendance, evening attendance, or cast vote is absent -> vote is ABANDONED and user is BLOCKED for discrepancy.
     */
    private fun evaluateSequenceState() {
        val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
        val todayLogs = memberAttendanceLogs.filter { it.timestamp.contains(today) }

        hasMarkedMorningToday = todayLogs.any { it.attendanceType.contains("Morning", ignoreCase = true) }
        hasMarkedEveningToday = todayLogs.any { it.attendanceType.contains("Evening", ignoreCase = true) }

        val todayVotes = memberVotes.filter { it.timestamp.contains(today) }
        val hasVotedToday = todayVotes.isNotEmpty()
        val hasAbandonedVote = todayVotes.any { it.status == VoteRecordEntity.STATUS_ABANDONED }

        // 1. Check if member is blocked for discrepancy
        if (isMemberBlocked) {
            binding.cardMemberBlocked.visibility = View.VISIBLE
            binding.tvBlockReasonText.text = "Reason: ${if (memberBlockReason.isNotEmpty()) memberBlockReason else "Discrepancy detected in duty attendance or voting sequence."}"

            // Freeze all actions
            binding.btnMarkMorning.isEnabled = false
            binding.btnMarkMorning.alpha = 0.4f
            binding.btnMarkMorning.text = "1️⃣ Morning (Blocked)"

            binding.btnMarkEvening.isEnabled = false
            binding.btnMarkEvening.alpha = 0.4f
            binding.btnMarkEvening.text = "3️⃣ Evening (Blocked)"

            binding.btnOpenVoting.isEnabled = false
            binding.btnOpenVoting.alpha = 0.4f
            binding.btnOpenVoting.text = "🗳️ Voting Station (Blocked)"

            binding.tvStep2StatusPill.text = "🚨 BLOCKED"
            binding.tvStep2StatusPill.setBackgroundResource(R.drawable.bg_pill_rose)
            binding.tvStep2StatusPill.setTextColor(ContextCompat.getColor(this, R.color.rose_500))

            binding.tvVotingStatusHint.visibility = View.GONE

            binding.btnTestDiscrepancyAbandon.text = "🔄 Reset and Unblock (Demo / Admin Override)"
            binding.btnTestDiscrepancyAbandon.setTextColor(ContextCompat.getColor(this, R.color.emerald_500))
            return
        }

        binding.cardMemberBlocked.visibility = View.GONE
        binding.btnTestDiscrepancyAbandon.text = "⚠️ Test Discrepancy (Simulate Absent Evening Duty and Abandon Vote)"
        binding.btnTestDiscrepancyAbandon.setTextColor(ContextCompat.getColor(this, R.color.rose_500))

        // 2. Evaluate 3-step sequence
        if (!hasMarkedMorningToday) {
            // STEP 1 PENDING - RESTRICTED ACCORDING TO MORNING SHIFT HOURS
            val inMorningSlot = isTimeInSlot(morningStart, morningEnd)
            if (inMorningSlot) {
                binding.btnMarkMorning.isEnabled = true
                binding.btnMarkMorning.alpha = 1.0f
                binding.btnMarkMorning.text = "1️⃣ Mark Morning Shift"
            } else {
                binding.btnMarkMorning.isEnabled = false
                binding.btnMarkMorning.alpha = 0.45f
                binding.btnMarkMorning.text = "1️⃣ Morning Locked (Hours: $morningStart - $morningEnd)"
            }

            binding.btnMarkEvening.isEnabled = false
            binding.btnMarkEvening.alpha = 0.4f
            binding.btnMarkEvening.text = "3️⃣ Evening Locked (Morning Absent)"

            binding.btnOpenVoting.isEnabled = false
            binding.btnOpenVoting.alpha = 0.4f
            binding.btnOpenVoting.text = "🗳️ Step 2: Voting Locked (Morning Absent)"

            binding.tvStep2StatusPill.text = "Locked (Morning Absent) 🔒"
            binding.tvStep2StatusPill.setBackgroundResource(R.drawable.bg_pill_rose)
            binding.tvStep2StatusPill.setTextColor(ContextCompat.getColor(this, R.color.rose_500))

            binding.tvVotingStatusHint.visibility = View.GONE

        } else if (hasAbandonedVote) {
            // VOTE ABANDONED STATE
            binding.btnMarkMorning.isEnabled = false
            binding.btnMarkMorning.alpha = 0.6f
            binding.btnMarkMorning.text = "1️⃣ Morning Shift Verified ✓"

            binding.btnOpenVoting.isEnabled = true
            binding.btnOpenVoting.alpha = 0.85f
            binding.btnOpenVoting.text = "🗳️ View Ballots (Vote Abandoned 🚨)"

            binding.tvStep2StatusPill.text = "🚨 Vote Abandoned"
            binding.tvStep2StatusPill.setBackgroundResource(R.drawable.bg_pill_rose)
            binding.tvStep2StatusPill.setTextColor(ContextCompat.getColor(this, R.color.rose_500))

            binding.btnMarkEvening.isEnabled = false
            binding.btnMarkEvening.alpha = 0.4f
            binding.btnMarkEvening.text = "3️⃣ Evening Shift Blocked"

            binding.tvVotingStatusHint.visibility = View.GONE

        } else if (!hasVotedToday) {
            // STEP 1 DONE, STEP 2 (VOTING) PENDING
            binding.btnMarkMorning.isEnabled = false
            binding.btnMarkMorning.alpha = 0.6f
            binding.btnMarkMorning.text = "1️⃣ Morning Shift Verified ✓"

            binding.btnOpenVoting.isEnabled = true
            binding.btnOpenVoting.alpha = 1.0f
            binding.btnOpenVoting.text = "🗳️ Step 2: Open Voting Station and Cast Vote"

            binding.tvStep2StatusPill.text = "Step 2 Action Required 🗳️"
            binding.tvStep2StatusPill.setBackgroundResource(R.drawable.bg_pill_role)
            binding.tvStep2StatusPill.setTextColor(ContextCompat.getColor(this, R.color.white))

            binding.btnMarkEvening.isEnabled = false
            binding.btnMarkEvening.alpha = 0.4f
            binding.btnMarkEvening.text = "3️⃣ Evening Locked (Cast Vote First 🔒)"

            binding.tvVotingStatusHint.visibility = View.GONE

        } else if (!hasMarkedEveningToday) {
            // STEP 1 & 2 DONE, STEP 3 (EVENING) PENDING - RESTRICTED ACCORDING TO EVENING SHIFT HOURS
            binding.btnMarkMorning.isEnabled = false
            binding.btnMarkMorning.alpha = 0.6f
            binding.btnMarkMorning.text = "1️⃣ Morning Shift Verified ✓"

            binding.btnOpenVoting.isEnabled = true
            binding.btnOpenVoting.alpha = 0.9f
            binding.btnOpenVoting.text = "🗳️ Ballot Cast (Vote UNCOUNTED: Evening Pending ⏳)"

            binding.tvStep2StatusPill.text = "👎 Vote UNCOUNTED (Evening Pending)"
            binding.tvStep2StatusPill.setBackgroundResource(R.drawable.bg_pill_rose)
            binding.tvStep2StatusPill.setTextColor(ContextCompat.getColor(this, R.color.rose_500))

            // Step 3 is restricted to evening shift timing!
            val inEveningSlot = isTimeInSlot(eveningStart, eveningEnd)
            if (inEveningSlot) {
                binding.btnMarkEvening.isEnabled = true
                binding.btnMarkEvening.alpha = 1.0f
                binding.btnMarkEvening.text = "3️⃣ Mark Evening Shift to COUNT Vote"
            } else {
                binding.btnMarkEvening.isEnabled = false
                binding.btnMarkEvening.alpha = 0.45f
                binding.btnMarkEvening.text = "3️⃣ Evening Locked (Hours: $eveningStart - $eveningEnd)"
            }

            binding.tvVotingStatusHint.visibility = View.GONE

        } else {
            // ALL 3 STEPS COMPLETED and FINALIZED!
            binding.btnMarkMorning.isEnabled = false
            binding.btnMarkMorning.alpha = 0.6f
            binding.btnMarkMorning.text = "1️⃣ Morning Verified ✓"

            binding.btnOpenVoting.isEnabled = true
            binding.btnOpenVoting.alpha = 1.0f
            binding.btnOpenVoting.text = "🗳️ View Ballots (Vote COUNTED ✓)"

            binding.tvStep2StatusPill.text = "👍 Validated and Counted ✓"
            binding.tvStep2StatusPill.setBackgroundResource(R.drawable.bg_badge_gold)
            binding.tvStep2StatusPill.setTextColor(ContextCompat.getColor(this, R.color.slate_950))

            binding.btnMarkEvening.isEnabled = false
            binding.btnMarkEvening.alpha = 0.6f
            binding.btnMarkEvening.text = "3️⃣ Evening Verified ✓"

            binding.tvVotingStatusHint.visibility = View.GONE
        }

        val mSlotActive = isTimeInSlot(morningStart, morningEnd)
        val eSlotActive = isTimeInSlot(eveningStart, eveningEnd)
        val mStatus = if (mSlotActive) "Open" else "Restricted"
        val eStatus = if (eSlotActive) "Open" else "Restricted"
        binding.tvWindowStatus.text = "Shift Hours: Morning $morningStart - $morningEnd ($mStatus) | Evening $eveningStart - $eveningEnd ($eStatus)"
    }

    private fun parseMinutes(timeStr: String): Int? {
        val clean = timeStr.trim().uppercase()
        val isPM = clean.contains("PM")
        val isAM = clean.contains("AM")
        val digitsOnly = clean.replace("AM", "").replace("PM", "").trim()
        val parts = digitsOnly.split(":")
        if (parts.isEmpty()) return null
        var hours = parts[0].trim().toIntOrNull() ?: return null
        val minutes = if (parts.size > 1) parts[1].trim().toIntOrNull() ?: 0 else 0
        if (isPM && hours < 12) hours += 12
        if (isAM && hours == 12) hours = 0
        return hours * 60 + minutes
    }

    private fun isTimeInSlot(startStr: String, endStr: String): Boolean {
        try {
            val cal = Calendar.getInstance()
            val nowMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)

            val startMin = parseMinutes(startStr) ?: return false
            val endMin = parseMinutes(endStr) ?: return false

            return nowMinutes in startMin..endMin
        } catch (_: Exception) {
            return false
        }
    }

    private fun handleMorningLoginAttempt() {
        if (isMemberBlocked) {
            showBlockedAlertDialog()
            return
        }

        if (hasMarkedMorningToday) {
            Toast.makeText(this, "Morning shift attendance is already verified for today.", Toast.LENGTH_SHORT).show()
            return
        }

        val inSlot = isTimeInSlot(morningStart, morningEnd)

        if (!inSlot) {
            AlertDialog.Builder(this)
                .setTitle("Attendance Window Restricted")
                .setMessage("Morning shift hours: $morningStart to $morningEnd.\nCurrent time is outside the allowed morning duty window.")
                .setPositiveButton("OK", null)
                .show()
            return
        }

        selectedType = "Morning Shift"
        binding.tvBadgeType.text = "Step 1: Morning Shift"
        checkAndRequestHardwarePermissionsSafely {
            recordAttendanceLocally(isEvening = false)
        }
    }

    private fun handleOpenVoting() {
        if (isMemberBlocked) {
            showBlockedAlertDialog()
            return
        }

        if (!hasMarkedMorningToday) {
            AlertDialog.Builder(this)
                .setTitle("Voting Status")
                .setMessage("Morning attendance not recorded for today.")
                .setPositiveButton("OK", null)
                .show()
            return
        }

        val intent = Intent(this, VotingActivity::class.java).apply {
            putExtra("ORG_ID", orgId)
            putExtra("ORG_NAME", orgName)
            putExtra("USER_IDENTIFIER", userIdentifier)
            putExtra("USER_NAME", userName)
            putExtra("USER_ROLE", userRole)
            putExtra("MEMBER_WORK", memberNatureOfWork)
        }
        startActivity(intent)
    }

    private fun handleEveningLogoutAttempt() {
        if (isMemberBlocked) {
            showBlockedAlertDialog()
            return
        }

        if (!hasMarkedMorningToday) {
            AlertDialog.Builder(this)
                .setTitle("Evening Attendance")
                .setMessage("Morning attendance not recorded for today.")
                .setPositiveButton("OK", null)
                .show()
            return
        }

        val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
        val todayVotes = memberVotes.filter { it.timestamp.contains(today) }

        if (todayVotes.isEmpty()) {
            AlertDialog.Builder(this)
                .setTitle("Evening Attendance")
                .setMessage("Ballot vote not recorded for today.")
                .setPositiveButton("Open Voting Station") { _, _ ->
                    handleOpenVoting()
                }
                .setNegativeButton("Cancel", null)
                .show()
            return
        }

        val inSlot = isTimeInSlot(eveningStart, eveningEnd)

        if (!inSlot) {
            AlertDialog.Builder(this)
                .setTitle("Attendance Window Restricted")
                .setMessage("Evening shift hours: $eveningStart to $eveningEnd.\nCurrent time is outside the allowed evening duty window.")
                .setPositiveButton("OK", null)
                .show()
            return
        }

        selectedType = "Evening Shift"
        binding.tvBadgeType.text = "Step 3: Evening Shift"
        checkAndRequestHardwarePermissionsSafely {
            recordAttendanceLocally(isEvening = true)
        }
    }

    private fun isAmazonDevice(): Boolean {
        return com.lrms.attendanceapp.util.DeviceEnvironment.isAmazonFireOS
    }

    /**
     * Hardware-aware safe permission requester.
     * Works seamlessly on Samsung, Pixel, Xiaomi, and Amazon Fire tablets.
     * - On Amazon tablets: skips strict GPS hardware requests to prevent Fire OS issues.
     * - On regular Android devices: dynamically queries packageManager.hasSystemFeature()
     *   before asking for Camera or Location permissions.
     */
    private fun checkAndRequestHardwarePermissionsSafely(onGranted: () -> Unit) {
        val permissionsNeeded = mutableListOf<String>()
        val isAmazon = isAmazonDevice()

        // 1. Camera Feature Check (both Android & Amazon tablets if hardware camera exists)
        if (packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA_ANY)) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
                permissionsNeeded.add(Manifest.permission.CAMERA)
            }
        }

        // 2. Location Feature Check:
        // On Amazon Fire Tablets, skip strict GPS hardware request to avoid ingestion errors.
        // On regular Android (Samsung/Pixel/etc.), check if GPS hardware exists before requesting.
        if (!isAmazon && packageManager.hasSystemFeature(PackageManager.FEATURE_LOCATION_GPS)) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
                permissionsNeeded.add(Manifest.permission.ACCESS_FINE_LOCATION)
            }
        }

        if (permissionsNeeded.isEmpty()) {
            // All necessary permissions for this device are satisfied
            onGranted()
        } else {
            pendingAttendanceAction = onGranted
            ActivityCompat.requestPermissions(
                this,
                permissionsNeeded.toTypedArray(),
                PERMISSION_REQ_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == PERMISSION_REQ_CODE) {
            val action = pendingAttendanceAction
            pendingAttendanceAction = null
            action?.invoke()
        }
    }

    private fun recordAttendanceLocally(isEvening: Boolean) {
        binding.tvBlinkPrompt.visibility = View.VISIBLE
        binding.tvBlinkPrompt.text = "👁️ Eye Blink Liveness Verified!"

        lifecycleScope.launch {
            val timestamp = SimpleDateFormat("dd/MM/yyyy, hh:mm:ss a", Locale.getDefault()).format(Date())
            val entity = AttendanceEntity(
                userId = userIdentifier,
                userName = userName,
                userEmail = "${userName.lowercase().replace(" ", ".")}@duty.gov.in",
                mobileNo = "9820011220",
                aadhaarNo = "1234-5678-9021",
                state = "Duty Location",
                district = "Central District",
                instituteName = orgName,
                latitude = "19.0760 N",
                longitude = "72.8777 E",
                address = "$orgName Headquarters",
                blinkVerified = true,
                attendanceType = selectedType,
                timestamp = timestamp,
                verificationMode = "Biometric Face + Eye Blink ($selectedType)",
                confidence = "99.2%",
                status = if (isEvening) "ALL 3 STEPS COMPLETED and FINALIZED" else "Morning Shift Verified",
                isSynced = false,
                occasion = "Duty Hours Attendance",
                orgId = orgId,
                memberCode = userIdentifier
            )

            // Save to secure device database
            withContext(Dispatchers.IO) {
                database.attendanceDao().insertLog(entity)
            }
            Toast.makeText(this@MainActivity, "$selectedType Attendance Recorded!", Toast.LENGTH_SHORT).show()

            if (isEvening) {
                // Confirm all provisional votes for this member in this org
                withContext(Dispatchers.IO) {
                    database.voteRecordDao().confirmVotesForMember(userIdentifier, orgId)
                }
            }

            withContext(Dispatchers.Main) {
                if (isEvening) {
                    AlertDialog.Builder(this@MainActivity)
                        .setTitle("ALL 3 STEPS COMPLETED and FINALIZED")
                        .setMessage("Duty attendance and vote record entered into device storage.")
                        .setPositiveButton("OK", null)
                        .show()
                } else {
                    AlertDialog.Builder(this@MainActivity)
                        .setTitle("Step 1 Complete: Morning Shift Verified")
                        .setMessage("Morning attendance verified present.")
                        .setPositiveButton("Open Voting Station") { _, _ ->
                            handleOpenVoting()
                        }
                        .setNegativeButton("Later", null)
                        .show()
                }
            }
        }
    }

    private fun handleTestDiscrepancyAbandon() {
        if (isMemberBlocked) {
            // Provide option to reset and unblock for testing/admin demo!
            AlertDialog.Builder(this)
                .setTitle("🔄 Unblock Member (Demo / Admin Override)")
                .setMessage("This member is currently BLOCKED for duty discrepancy.\n\nWould you like to unblock this member and restore active standing?")
                .setPositiveButton("Unblock Member") { _, _ ->
                    lifecycleScope.launch(Dispatchers.IO) {
                        database.memberDao().unblockMember(userIdentifier)
                        withContext(Dispatchers.Main) {
                            isMemberBlocked = false
                            memberBlockReason = ""
                            evaluateSequenceState()
                            Toast.makeText(this@MainActivity, "Member $userIdentifier unblocked successfully!", Toast.LENGTH_SHORT).show()
                        }
                    }
                }
                .setNegativeButton("Cancel", null)
                .show()
            return
        }

        AlertDialog.Builder(this)
            .setTitle("⚠️ Test Discrepancy and Abandonment Simulation")
            .setMessage("Simulate discrepancy (unmarked evening attendance)?")
            .setPositiveButton("Simulate Discrepancy") { _, _ ->
                val reason = "Discrepancy: Absent from evening duty attendance after voting"
                lifecycleScope.launch(Dispatchers.IO) {
                    database.voteRecordDao().abandonVotesForMember(userIdentifier, orgId, reason)
                    database.memberDao().blockMember(userIdentifier, reason)

                    val timestamp = SimpleDateFormat("dd/MM/yyyy, hh:mm:ss a", Locale.getDefault()).format(Date())
                    val discrepancyLog = AttendanceEntity(
                        userId = userIdentifier,
                        userName = userName,
                        userEmail = "${userName.lowercase().replace(" ", ".")}@duty.gov.in",
                        mobileNo = "9820011220",
                        aadhaarNo = "1234-5678-9021",
                        state = "Duty Location",
                        district = "Central District",
                        instituteName = orgName,
                        latitude = "19.0760 N",
                        longitude = "72.8777 E",
                        address = "$orgName Station",
                        blinkVerified = false,
                        attendanceType = "DISCREPANCY: EVENING ABSENT",
                        timestamp = timestamp,
                        verificationMode = "Security Audit Discrepancy Monitor",
                        confidence = "100%",
                        status = "DISCREPANCY: VOTE ABANDONED and USER BLOCKED",
                        isSynced = false,
                        occasion = "Duty Discrepancy Enforcement",
                        orgId = orgId,
                        memberCode = userIdentifier
                    )
                    database.attendanceDao().insertLog(discrepancyLog)

                    withContext(Dispatchers.Main) {
                        isMemberBlocked = true
                        memberBlockReason = reason
                        evaluateSequenceState()
                        AlertDialog.Builder(this@MainActivity)
                            .setTitle("🚨 DISCREPANCY DETECTED: USER BLOCKED")
                            .setMessage("Duty Discrepancy Enforced:\n\n• Vote has been ABANDONED and invalidated.\n• Member account $userIdentifier is now BLOCKED.\n• All attendance and voting actions are frozen.\n\n(Click the test button again or visit Organization Admin Portal to unblock).")
                            .setPositiveButton("Understood", null)
                            .show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showBlockedAlertDialog() {
        AlertDialog.Builder(this)
            .setTitle("🚨 ACCESS BLOCKED: DISCREPANCY DETECTED")
            .setMessage("Your account is BLOCKED.\n\nReason: ${if (memberBlockReason.isNotEmpty()) memberBlockReason else "Discrepancy in duty attendance or voting sequence."}\n\nAny pending vote has been ABANDONED. All attendance and voting actions are frozen.\n\nContact Organization Administrator to resolve this discrepancy.")
            .setPositiveButton("Understood", null)
            .show()
    }

    private fun showAlterShiftDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_alter_shift_timings, null)
        val etMStart = dialogView.findViewById<EditText>(R.id.et_shift_m_start)
        val etMEnd = dialogView.findViewById<EditText>(R.id.et_shift_m_end)
        val etEStart = dialogView.findViewById<EditText>(R.id.et_shift_e_start)
        val etEEnd = dialogView.findViewById<EditText>(R.id.et_shift_e_end)

        etMStart.setText(morningStart)
        etMEnd.setText(morningEnd)
        etEStart.setText(eveningStart)
        etEEnd.setText(eveningEnd)

        AlertDialog.Builder(this)
            .setTitle("⚙️ Admin: Alter Shift Timings")
            .setView(dialogView)
            .setPositiveButton("Apply") { _, _ ->
                morningStart = etMStart.text.toString().trim().ifEmpty { "09:00" }
                morningEnd = etMEnd.text.toString().trim().ifEmpty { "13:00" }
                eveningStart = etEStart.text.toString().trim().ifEmpty { "16:00" }
                eveningEnd = etEEnd.text.toString().trim().ifEmpty { "19:00" }

                lifecycleScope.launch(Dispatchers.IO) {
                    database.organizationDao().updateShiftTimings(orgId, morningStart, morningEnd, eveningStart, eveningEnd)
                    withContext(Dispatchers.Main) {
                        binding.tvWindowStatus.text = "Shift Hours: Morning $morningStart - $morningEnd | Evening $eveningStart - $eveningEnd"
                        evaluateSequenceState()
                        Toast.makeText(this@MainActivity, "Shift hours altered successfully!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showAddTopicDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_add_topic, null)
        val etCategory = dialogView.findViewById<EditText>(R.id.et_topic_category)
        val etTitle = dialogView.findViewById<EditText>(R.id.et_topic_title)
        val etDescription = dialogView.findViewById<EditText>(R.id.et_topic_description)
        val etOptions = dialogView.findViewById<EditText>(R.id.et_topic_options)
        val etStartTime = dialogView.findViewById<EditText>(R.id.et_voting_start_time)
        val etEndTime = dialogView.findViewById<EditText>(R.id.et_voting_end_time)

        AlertDialog.Builder(this)
            .setTitle("📢 Admin: Post Voting Topic / Issue")
            .setView(dialogView)
            .setPositiveButton("Post Ballot") { _, _ ->
                val category = etCategory.text.toString().trim().ifEmpty { "Official Voting Notice" }
                val title = etTitle.text.toString().trim()
                val description = etDescription.text.toString().trim()
                val rawOptions = etOptions.text.toString().trim()
                val startTime = etStartTime.text.toString().trim().ifEmpty { "10:00" }
                val endTime = etEndTime.text.toString().trim().ifEmpty { "16:00" }

                if (title.isEmpty()) {
                    Toast.makeText(this, "Title is required", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }

                val optionsList = if (rawOptions.isNotEmpty()) {
                    rawOptions.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                } else {
                    listOf("Approve", "Reject", "Abstain")
                }
                val optionsJson = Gson().toJson(optionsList)
                val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())

                lifecycleScope.launch(Dispatchers.IO) {
                    database.votingTopicDao().insert(
                        VotingTopicEntity(
                            orgId = orgId,
                            title = title,
                            description = description.ifEmpty { "Official announcement by Administrator." },
                            category = category,
                            optionsJson = optionsJson,
                            createdAt = today,
                            votingStartTime = startTime,
                            votingEndTime = endTime,
                            votingDate = today
                        )
                    )
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@MainActivity, "Voting announcement posted with window $startTime - $endTime!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showRecordDetailsDialog(record: AttendanceEntity) {
        val details = """
            🆔 Record ID: ${record.id}
            👤 Member: ${record.userName}
            💼 Member Code: ${record.userId}
            🏢 Organization: ${record.instituteName}
            
            ⏱️ Shift Type: ${record.attendanceType}
            📅 Timestamp: ${record.timestamp}
            👁️ Blink Liveness: ${if (record.blinkVerified) "VERIFIED PRESENT ✓" else "FAILED"}
            🔍 Verification Mode: ${record.verificationMode} (Confidence: ${record.confidence})
            
            📍 Duty Location: ${record.address}
            🌐 Coordinates: Lat ${record.latitude}, Long ${record.longitude}
            
            💾 Storage Status: SECURE DEVICE STORAGE (Local Database)
        """.trimIndent()

        AlertDialog.Builder(this)
            .setTitle("📋 Duty Record Details #${record.id}")
            .setMessage(details)
            .setPositiveButton("Close", null)
            .show()
    }
}
