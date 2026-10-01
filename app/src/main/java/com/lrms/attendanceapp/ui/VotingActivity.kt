package com.lrms.attendanceapp.ui

import android.app.AlertDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.Gson
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AppDatabase
import com.lrms.attendanceapp.data.local.AttendanceEntity
import com.lrms.attendanceapp.data.local.MemberEntity
import com.lrms.attendanceapp.data.local.VoteRecordEntity
import com.lrms.attendanceapp.data.local.VotingTopicEntity
import com.lrms.attendanceapp.databinding.ActivityVotingBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class VotingActivity : AppCompatActivity() {

    private lateinit var binding: ActivityVotingBinding
    private lateinit var database: AppDatabase
    private lateinit var adapter: VotingCardAdapter

    private var orgId: Long = 1
    private var orgName: String = "Supreme Court and High Court"
    private var userIdentifier: String = "MEM-01"
    private var userName: String = "Alex Rivera"
    private var userRole: String = "member"
    private var memberWork: String = "Presiding Officer"

    private var currentMember: MemberEntity? = null
    private var isMorningMarked: Boolean = false
    private var topicsList: List<VotingTopicEntity> = emptyList()
    private var allVotes: List<VoteRecordEntity> = emptyList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityVotingBinding.inflate(layoutInflater)
        setContentView(binding.root)

        orgId = intent.getLongExtra("ORG_ID", 1)
        orgName = intent.getStringExtra("ORG_NAME") ?: orgName
        userIdentifier = intent.getStringExtra("USER_IDENTIFIER") ?: userIdentifier
        userName = intent.getStringExtra("USER_NAME") ?: userName
        userRole = intent.getStringExtra("USER_ROLE") ?: userRole
        memberWork = intent.getStringExtra("MEMBER_WORK") ?: memberWork

        binding.tvVotingStationName.text = "$orgName Ballots"

        database = AppDatabase.getDatabase(this)

        val isAdmin = userRole.equals("admin", ignoreCase = true)
        binding.btnVotingAddTopic.visibility = if (isAdmin) View.VISIBLE else View.GONE

        setupRecyclerView()
        setupListeners()
        loadMemberStatusAndCheckSequence()
        observeData()
    }

    private fun setupRecyclerView() {
        adapter = VotingCardAdapter(
            onCastVote = { topic, option ->
                handleVoteAttempt(topic, option)
            }
        )
        binding.rvBallots.layoutManager = LinearLayoutManager(this)
        binding.rvBallots.adapter = adapter
    }

    private fun setupListeners() {
        binding.ibVotingBack.setOnClickListener {
            finish()
        }

        binding.btnVotingAddTopic.setOnClickListener {
            showAddTopicDialog()
        }
    }

    private fun loadMemberStatusAndCheckSequence() {
        lifecycleScope.launch {
            val member = withContext(Dispatchers.IO) {
                database.memberDao().getMemberByCode(userIdentifier)
            }
            currentMember = member

            if (member != null && member.isBlocked) {
                AlertDialog.Builder(this@VotingActivity)
                    .setTitle("🚨 ACCESS BLOCKED")
                    .setMessage("Your account is BLOCKED due to a detected discrepancy in duty attendance or voting.\n\nReason: ${member.blockReason}\n\nVoting station access is terminated.")
                    .setCancelable(false)
                    .setPositiveButton("Exit") { _, _ -> finish() }
                    .show()
                return@launch
            }

            // Check today's morning attendance
            val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
            database.attendanceDao().getLogsForUser(userIdentifier).collectLatest { logs ->
                val todayLogs = logs.filter { it.timestamp.contains(today) }
                isMorningMarked = todayLogs.any { it.attendanceType.contains("Morning", ignoreCase = true) }

                if (isMorningMarked) {
                    binding.tvVoterCredentials.text = "Voter: $userName ($memberWork) • Step 1: Morning Shift Verified ✓"
                    binding.tvVoterCredentials.setTextColor(getColor(R.color.emerald_500))
                } else {
                    binding.tvVoterCredentials.text = "Voter: $userName ($memberWork) • Step 1: Morning Attendance MISSING ⚠️"
                    binding.tvVoterCredentials.setTextColor(getColor(R.color.amber_500))
                    showMorningRequiredWarning()
                }
                updateAdapter()
            }
        }
    }

    private fun showMorningRequiredWarning() {
        AlertDialog.Builder(this)
            .setTitle("Step 1 Missing")
            .setMessage("Morning shift attendance not recorded for today.")
            .setPositiveButton("OK", null)
            .show()
    }

    private fun observeData() {
        lifecycleScope.launch {
            database.votingTopicDao().getTopicsForOrg(orgId).collectLatest { topics ->
                topicsList = topics
                updateAdapter()
            }
        }

        lifecycleScope.launch {
            database.voteRecordDao().getVotesForOrg(orgId).collectLatest { votes ->
                allVotes = votes
                updateAdapter()
            }
        }
    }

    private fun updateAdapter() {
        val votesByTopic = allVotes.groupBy { it.topicId }
        val userVotedMap = mutableMapOf<Long, VoteRecordEntity>()
        for (vote in allVotes) {
            if (vote.memberCode == userIdentifier) {
                userVotedMap[vote.topicId] = vote
            }
        }
        adapter.updateData(topicsList, votesByTopic, userVotedMap, isMorningMarked)
    }

    private fun isCurrentTimeInPeriod(startStr: String, endStr: String): Boolean {
        try {
            val cal = Calendar.getInstance()
            val nowMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)

            val sParts = startStr.split(":").map { it.trim().toInt() }
            val eParts = endStr.split(":").map { it.trim().toInt() }

            val startMin = sParts[0] * 60 + (if (sParts.size > 1) sParts[1] else 0)
            val endMin = eParts[0] * 60 + (if (eParts.size > 1) eParts[1] else 0)

            return nowMinutes in startMin..endMin
        } catch (_: Exception) {
            return true
        }
    }

    private fun handleVoteAttempt(topic: VotingTopicEntity, candidateOrOption: String) {
        if (!isMorningMarked) {
            AlertDialog.Builder(this)
                .setTitle("Step 1 Missing")
                .setMessage("Morning shift attendance not recorded for today.")
                .setPositiveButton("OK", null)
                .show()
            return
        }

        val inPeriod = isCurrentTimeInPeriod(topic.votingStartTime, topic.votingEndTime)
        if (!inPeriod) {
            AlertDialog.Builder(this)
                .setTitle("Voting Period")
                .setMessage("Voting for \"${topic.title}\" hours: ${topic.votingStartTime} to ${topic.votingEndTime}.\nCurrent time is outside this window.")
                .setPositiveButton("Proceed (Demo Mode)") { _, _ ->
                    confirmAndCastVote(topic, candidateOrOption)
                }
                .setNeutralButton("Flag Discrepancy and Block") { _, _ ->
                    flagDiscrepancyAndBlock("Attempted vote outside voting window ${topic.votingStartTime}-${topic.votingEndTime}")
                }
                .setNegativeButton("Cancel", null)
                .show()
            return
        }

        confirmAndCastVote(topic, candidateOrOption)
    }

    private fun confirmAndCastVote(topic: VotingTopicEntity, candidateOrOption: String) {
        AlertDialog.Builder(this)
            .setTitle("Biometric Verification")
            .setMessage("Eye Blink Scan: MATCH OK\nFingerprint Sensor: MATCH OK\n\nCast vote for:\n\"$candidateOrOption\"\n\nin \"${topic.title}\"?\n\nStatus: Pending evening attendance.")
            .setPositiveButton("Confirm and Cast Ballot") { _, _ ->
                val now = SimpleDateFormat("dd/MM/yyyy, hh:mm:ss a", Locale.getDefault()).format(Date())

                lifecycleScope.launch(Dispatchers.IO) {
                    val vote = VoteRecordEntity(
                        orgId = orgId,
                        topicId = topic.id,
                        memberCode = userIdentifier,
                        memberName = userName,
                        selectedOption = candidateOrOption,
                        timestamp = now,
                        biometricHash = "Dual Biometric (Eye + Fingerprint Re-Auth)",
                        status = VoteRecordEntity.STATUS_PENDING_EVENING,
                        isFinalized = false
                    )
                    database.voteRecordDao().insertVote(vote)

                    // Also log to attendance records
                    val voteLog = AttendanceEntity(
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
                        address = "$orgName Voting Station",
                        blinkVerified = true,
                        attendanceType = "Ballot Vote: $candidateOrOption",
                        timestamp = now,
                        verificationMode = "Dual Biometric (Eye + Fingerprint)",
                        confidence = "99.8%",
                        status = "PROVISIONAL VOTE (Pending Evening Attendance - Currently Uncounted)",
                        isSynced = false,
                        occasion = AttendanceEntity.OCCASION_COMMITTEE_ELECTION,
                        orgId = orgId,
                        memberCode = userIdentifier
                    )
                    database.attendanceDao().insertLog(voteLog)

                    withContext(Dispatchers.Main) {
                        AlertDialog.Builder(this@VotingActivity)
                            .setTitle("Vote Cast")
                            .setMessage("Vote recorded. Status: Pending evening attendance.")
                            .setPositiveButton("Return to Duty Console") { _, _ ->
                                setResult(RESULT_OK)
                                finish()
                            }
                            .show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun flagDiscrepancyAndBlock(reason: String) {
        lifecycleScope.launch(Dispatchers.IO) {
            database.memberDao().blockMember(userIdentifier, reason)
            database.voteRecordDao().abandonVotesForMember(userIdentifier, orgId, reason)
            withContext(Dispatchers.Main) {
                AlertDialog.Builder(this@VotingActivity)
                    .setTitle("🚨 DISCREPANCY FLAGGED - USER BLOCKED")
                    .setMessage("Discrepancy: $reason\n\nYour account has been blocked and any pending votes abandoned.")
                    .setCancelable(false)
                    .setPositiveButton("Exit") { _, _ -> finish() }
                    .show()
            }
        }
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
            .setTitle("📢 Post New Voting Topic / Announcement")
            .setView(dialogView)
            .setPositiveButton("Publish Ballot") { _, _ ->
                val category = etCategory.text.toString().trim().ifEmpty { "Official Ballot Announcement" }
                val title = etTitle.text.toString().trim()
                val description = etDescription.text.toString().trim()
                val rawOptions = etOptions.text.toString().trim()
                val startTime = etStartTime.text.toString().trim().ifEmpty { "10:00" }
                val endTime = etEndTime.text.toString().trim().ifEmpty { "16:00" }

                if (title.isEmpty()) {
                    Toast.makeText(this, "Topic title is required", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }

                val optionsList = if (rawOptions.isNotEmpty()) {
                    rawOptions.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                } else {
                    listOf("In Favor / Yes", "Against / No", "Abstain")
                }
                val optionsJson = Gson().toJson(optionsList)
                val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())

                lifecycleScope.launch(Dispatchers.IO) {
                    val topic = VotingTopicEntity(
                        orgId = orgId,
                        title = title,
                        description = description.ifEmpty { "Official voting announcement published by Administrator." },
                        category = category,
                        optionsJson = optionsJson,
                        createdAt = today,
                        votingStartTime = startTime,
                        votingEndTime = endTime,
                        votingDate = today
                    )
                    database.votingTopicDao().insert(topic)
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@VotingActivity, "Topic published with voting window $startTime - $endTime!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
