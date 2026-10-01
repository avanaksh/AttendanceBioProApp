package com.lrms.attendanceapp.ui

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.widget.EditText
import android.widget.RadioButton
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AppDatabase
import com.lrms.attendanceapp.data.local.MemberEntity
import com.lrms.attendanceapp.data.local.OrganizationEntity
import com.lrms.attendanceapp.data.local.VotingTopicEntity
import com.lrms.attendanceapp.data.local.VoteRecordEntity
import com.lrms.attendanceapp.databinding.ActivityOrganizationDetailBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class OrganizationDetailActivity : AppCompatActivity() {

    private lateinit var binding: ActivityOrganizationDetailBinding
    private lateinit var database: AppDatabase

    private var orgId: Long = 1
    private var orgName: String = "Supreme Court and High Court"
    private var orgCategory: String = "SC/HC"
    private var orgPurpose: String = "Cast vote for Selection of Judges/CJM/DJM"

    private var currentOrg: OrganizationEntity? = null
    private var allMembers: List<MemberEntity> = emptyList()
    private var searchMemberQuery: String = ""

    private lateinit var memberAdapter: MemberAdapter
    private lateinit var topicAdapter: VotingTopicAdapter

    private var attendanceMap: MutableMap<String, Pair<Boolean, Boolean>> = mutableMapOf()
    private var allOrgVotes: List<VoteRecordEntity> = emptyList()
    private var allOrgTopics: List<VotingTopicEntity> = emptyList()
    private var memberVoteMap: MutableMap<String, VoteRecordEntity> = mutableMapOf()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOrganizationDetailBinding.inflate(layoutInflater)
        setContentView(binding.root)

        orgId = intent.getLongExtra("EXTRA_ORG_ID", 1)
        orgName = (intent.getStringExtra("EXTRA_ORG_NAME") ?: orgName).replace("&", "and")
        orgCategory = (intent.getStringExtra("EXTRA_ORG_CATEGORY") ?: orgCategory).replace("&", "and")
        orgPurpose = (intent.getStringExtra("EXTRA_ORG_PURPOSE") ?: orgPurpose).replace("&", "and")

        binding.tvDetailOrgName.text = orgName
        binding.tvDetailOrgCategory.text = orgCategory
        binding.tvDetailOrgPurpose.text = "🎯 Purpose: $orgPurpose"

        database = AppDatabase.getDatabase(this)

        setupRecyclerViews()
        setupListeners()
        loadOrganizationDetails()
        observeData()
    }

    private fun setupRecyclerViews() {
        // Members list with direct Login button for each member (Admin or User)
        memberAdapter = MemberAdapter(
            onLoginClick = { member ->
                if (member.isBlocked) {
                    showMemberActionDialog(member)
                } else {
                    openMainActivityAsMember(member)
                }
            },
            onOptionsClick = { member ->
                showMemberActionDialog(member)
            }
        )
        binding.rvMembers.layoutManager = LinearLayoutManager(this)
        binding.rvMembers.adapter = memberAdapter

        // Voting topics list with Admin Add, Edit, Delete capabilities
        topicAdapter = VotingTopicAdapter(
            isAdmin = true,
            onTopicClick = { topic ->
                val intent = Intent(this, VotingActivity::class.java).apply {
                    putExtra("ORG_ID", orgId)
                    putExtra("ORG_NAME", orgName)
                    putExtra("TOPIC_ID", topic.id)
                    putExtra("TOPIC_TITLE", topic.title)
                }
                startActivity(intent)
            },
            onEditClick = { topic ->
                showEditTopicDialog(topic)
            },
            onDeleteClick = { topic ->
                confirmDeleteTopic(topic)
            }
        )
        binding.rvVotingTopics.layoutManager = LinearLayoutManager(this)
        binding.rvVotingTopics.adapter = topicAdapter
    }

    private fun setupListeners() {
        binding.ibDetailBack.setOnClickListener {
            finish()
        }

        binding.btnOrgMasterRecords.setOnClickListener {
            val intent = Intent(this, AdminPortalActivity::class.java).apply {
                putExtra("ORG_ID", orgId)
                putExtra("ORG_NAME", orgName)
            }
            startActivity(intent)
        }

        binding.btnAlterShiftTimings.setOnClickListener {
            showAlterShiftTimingsDialog()
        }

        binding.btnAddTopic.setOnClickListener {
            showAddTopicDialog()
        }

        binding.btnAddMember.setOnClickListener {
            showAddMemberDialog()
        }

        binding.etSearchMember.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                searchMemberQuery = s?.toString()?.trim() ?: ""
                filterMembers()
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        binding.btnViewFullVoteAudit.setOnClickListener {
            showAuthorityVoteAuditDialog()
        }
    }

    private fun loadOrganizationDetails() {
        lifecycleScope.launch {
            val org = withContext(Dispatchers.IO) {
                database.organizationDao().getOrganizationById(orgId)
            }
            if (org != null) {
                currentOrg = org
                binding.tvDetailMorningTiming.text = "${org.morningShiftStart} - ${org.morningShiftEnd}"
                binding.tvDetailEveningTiming.text = "${org.eveningShiftStart} - ${org.eveningShiftEnd}"
            }
        }
    }

    private fun observeData() {
        // Observe Members
        lifecycleScope.launch {
            database.memberDao().getMembersByOrg(orgId).collectLatest { members ->
                allMembers = members
                val blockedCount = members.count { it.isBlocked }
                val headerText = if (blockedCount > 0) {
                    "👥 Members (${members.size}) • 🚨 $blockedCount Blocked"
                } else {
                    "👥 Organization Members (${members.size})"
                }
                binding.tvMembersHeader.text = headerText
                updateAuditMetricsAndMembers()
            }
        }

        // Observe Voting Topics
        lifecycleScope.launch {
            database.votingTopicDao().getTopicsForOrg(orgId).collectLatest { topics ->
                allOrgTopics = topics
                topicAdapter.submitList(topics, adminMode = true)
            }
        }

        // Observe Attendance logs to compute today's status for each member
        lifecycleScope.launch {
            database.attendanceDao().getLogsForOrg(orgId).collectLatest { logs ->
                val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
                val todayLogs = logs.filter { it.timestamp.contains(today) }

                attendanceMap.clear()
                for (member in allMembers) {
                    val mLogs = todayLogs.filter { it.memberCode == member.memberCode || it.userId == member.memberCode }
                    val hasMorning = mLogs.any { it.attendanceType.contains("Morning", ignoreCase = true) }
                    val hasEvening = mLogs.any { it.attendanceType.contains("Evening", ignoreCase = true) }
                    attendanceMap[member.memberCode] = Pair(hasMorning, hasEvening)
                }
                updateAuditMetricsAndMembers()
            }
        }

        // Observe Votes for this Organization (Authority)
        lifecycleScope.launch {
            database.voteRecordDao().getVotesForOrg(orgId).collectLatest { votes ->
                allOrgVotes = votes
                updateAuditMetricsAndMembers()
            }
        }
    }

    private fun updateAuditMetricsAndMembers() {
        val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
        val todayVotes = allOrgVotes.filter { it.timestamp.contains(today) }

        memberVoteMap.clear()
        for (vote in todayVotes) {
            memberVoteMap[vote.memberCode] = vote
        }

        val totalCast = todayVotes.size
        // Counted votes require Evening Shift Attendance to be marked on the same day!
        val countedVotes = todayVotes.count { vote ->
            vote.status == VoteRecordEntity.STATUS_CONFIRMED || (attendanceMap[vote.memberCode]?.second == true)
        }
        val uncountedVotes = totalCast - countedVotes

        binding.tvAuditTotalCast.text = totalCast.toString()
        binding.tvAuditCountedVotes.text = countedVotes.toString()
        binding.tvAuditUncountedVotes.text = uncountedVotes.toString()

        if (uncountedVotes > 0) {
            binding.tvAuditUncountedBanner.visibility = View.VISIBLE
            binding.tvAuditUncountedBanner.text = "⚠️ Discrepancy Alert: $uncountedVotes vote(s) UNCOUNTED because Evening Shift attendance was not marked on the same day. Tap 'Audit Details' to review."
        } else {
            binding.tvAuditUncountedBanner.visibility = View.GONE
        }

        filterMembers()
    }

    private fun filterMembers() {
        val filtered = if (searchMemberQuery.isEmpty()) {
            allMembers
        } else {
            allMembers.filter {
                it.name.contains(searchMemberQuery, ignoreCase = true) ||
                it.natureOfWork.contains(searchMemberQuery, ignoreCase = true) ||
                it.role.contains(searchMemberQuery, ignoreCase = true) ||
                it.memberCode.contains(searchMemberQuery, ignoreCase = true)
            }
        }

        val defaultShifts = currentOrg?.let {
            "${it.morningShiftStart} - ${it.morningShiftEnd} | ${it.eveningShiftStart} - ${it.eveningShiftEnd}"
        } ?: "09:00 - 13:00 | 16:00 - 19:00"

        memberAdapter.updateData(filtered, defaultShifts, attendanceMap, memberVoteMap)
    }

    private fun showAuthorityVoteAuditDialog() {
        val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
        val todayVotes = allOrgVotes.filter { it.timestamp.contains(today) }

        if (todayVotes.isEmpty()) {
            AlertDialog.Builder(this)
                .setTitle("🗳️ Authority Ballot Audit — $orgName")
                .setMessage("No ballots have been cast in this organization today ($today).")
                .setPositiveButton("Close", null)
                .show()
            return
        }

        val sb = StringBuilder()
        sb.append("🏢 Respective Authority: $orgName\n")
        sb.append("📅 Audit Date: $today\n\n")

        val uncounted = todayVotes.filter { vote ->
            vote.status != VoteRecordEntity.STATUS_CONFIRMED && (attendanceMap[vote.memberCode]?.second != true)
        }
        val counted = todayVotes.filter { vote ->
            vote.status == VoteRecordEntity.STATUS_CONFIRMED || (attendanceMap[vote.memberCode]?.second == true)
        }

        sb.append("📊 AUTHORITY BALLOT and DUTY SUMMARY:\n")
        sb.append("• Total Ballots Cast: ${todayVotes.size}\n")
        sb.append("• 👍 Validated and Counted: ${counted.size}\n")
        sb.append("• 👎 Uncounted / Incomplete: ${uncounted.size}\n\n")

        if (uncounted.isNotEmpty()) {
            sb.append("🚨 👎 THUMBS DOWN — UNCOUNTED ENTRIES (EVENING ABSENT):\n")
            sb.append("----------------------------------------------------\n")
            for (v in uncounted) {
                val member = allMembers.find { it.memberCode == v.memberCode }
                val topic = allOrgTopics.find { it.id == v.topicId }
                val topicTitle = topic?.title ?: "Ballot #${v.topicId}"
                sb.append("👤 Voter: ${v.memberName} (${v.memberCode})\n")
                sb.append("💼 Role: ${member?.natureOfWork ?: "Staff"}\n")
                sb.append("📢 Ballot Topic: $topicTitle\n")
                sb.append("🗳️ Choice Cast: \"${v.selectedOption}\"\n")
                sb.append("⏱️ Cast Time: ${v.timestamp}\n")
                sb.append("🌅 Morning Shift: VERIFIED PRESENT ✓\n")
                sb.append("🌆 Evening Shift: ❌ NOT MARKED ON SAME DAY\n")
                sb.append("⚖️ Official Verdict: 👎 THUMBS DOWN — VOTE NOT COUNTED\n")
                if (member?.isBlocked == true) {
                    sb.append("🚨 Standing: ACCOUNT BLOCKED FOR DISCREPANCY\n")
                }
                sb.append("\n")
            }
        }

        if (counted.isNotEmpty()) {
            sb.append("🎉 👍 THUMBS UP — VALIDATED and COUNTED BALLOTS:\n")
            sb.append("----------------------------------------------------\n")
            for (v in counted) {
                val topic = allOrgTopics.find { it.id == v.topicId }
                val topicTitle = topic?.title ?: "Ballot #${v.topicId}"
                sb.append("👤 ${v.memberName} (${v.memberCode}) ➔ \"${v.selectedOption}\"\n")
                sb.append("📢 Topic: $topicTitle\n")
                sb.append("🌅 Morning: Verified ✓ | 🌆 Evening: Verified ✓\n")
                sb.append("⚖️ Official Verdict: 👍 THUMBS UP — VALIDATED and SEALED ✓\n\n")
            }
        }

        AlertDialog.Builder(this)
            .setTitle("🗳️ Authority Ballot and Attendance Audit")
            .setMessage(sb.toString().trimEnd())
            .setPositiveButton("Done", null)
            .setNeutralButton("Export Audit Report") { _, _ ->
                val intent = Intent(Intent.ACTION_SEND).apply {
                    type = "text/plain"
                    putExtra(Intent.EXTRA_SUBJECT, "$orgName - Voting and Attendance Audit Report ($today)")
                    putExtra(Intent.EXTRA_TEXT, sb.toString())
                }
                startActivity(Intent.createChooser(intent, "Share Authority Audit Report"))
            }
            .show()
    }

    private fun showMemberActionDialog(member: MemberEntity) {
        if (member.isBlocked) {
            val options = arrayOf(
                "🟢 Unblock Member (Resolve Discrepancy)",
                "📋 View Duty Records for ${member.name}",
                "⏱️ Alter Shift Timings for this Member"
            )

            AlertDialog.Builder(this)
                .setTitle("🚨 ${member.name} (BLOCKED)")
                .setMessage("Reason: ${member.blockReason.ifEmpty { "Discrepancy found in duty attendance or voting sequence." }}")
                .setItems(options) { _, which ->
                    when (which) {
                        0 -> unblockMember(member)
                        1 -> {
                            val intent = Intent(this, AdminPortalActivity::class.java).apply {
                                putExtra("ORG_ID", orgId)
                                putExtra("ORG_NAME", orgName)
                                putExtra("FILTER_MEMBER_CODE", member.memberCode)
                            }
                            startActivity(intent)
                        }
                        2 -> showAlterMemberShiftDialog(member)
                    }
                }
                .setNegativeButton("Close", null)
                .show()
            return
        }

        val status = attendanceMap[member.memberCode] ?: Pair(false, false)
        val vote = memberVoteMap[member.memberCode]
        val isVoteUncounted = vote != null && !status.second && (vote.status != VoteRecordEntity.STATUS_CONFIRMED)

        val options = if (isVoteUncounted) {
            arrayOf(
                "🚀 Log In and Open Duty Console as ${member.name}",
                "🚨 Block Member (Enforce Discrepancy for Missing Evening Duty)",
                "⏱️ Alter Shift Timings for this Member",
                "📋 View Duty Records for ${member.name}"
            )
        } else {
            arrayOf(
                "🚀 Log In and Open Duty Console as ${member.name}",
                "⏱️ Alter Shift Timings for this Member",
                "📋 View Duty Records for ${member.name}",
                "🚨 Block Member (Flag Discrepancy)"
            )
        }

        val message = if (isVoteUncounted) {
            "⚠️ ATTENDANCE DISCREPANCY DETECTED:\n\nThis member cast a ballot today for \"${vote?.selectedOption}\" but Evening Shift attendance was NOT marked on the same day.\n\nOfficial Verdict: VOTE NOT COUNTED."
        } else {
            "Member Code: ${member.memberCode}\nNature of Work: ${member.natureOfWork}"
        }

        AlertDialog.Builder(this)
            .setTitle("${member.name} (${member.role})")
            .setMessage(message)
            .setItems(options) { _, which ->
                if (isVoteUncounted) {
                    when (which) {
                        0 -> openMainActivityAsMember(member)
                        1 -> showBlockDiscrepancyDialog(member)
                        2 -> showAlterMemberShiftDialog(member)
                        3 -> {
                            val intent = Intent(this, AdminPortalActivity::class.java).apply {
                                putExtra("ORG_ID", orgId)
                                putExtra("ORG_NAME", orgName)
                                putExtra("FILTER_MEMBER_CODE", member.memberCode)
                            }
                            startActivity(intent)
                        }
                    }
                } else {
                    when (which) {
                        0 -> openMainActivityAsMember(member)
                        1 -> showAlterMemberShiftDialog(member)
                        2 -> {
                            val intent = Intent(this, AdminPortalActivity::class.java).apply {
                                putExtra("ORG_ID", orgId)
                                putExtra("ORG_NAME", orgName)
                                putExtra("FILTER_MEMBER_CODE", member.memberCode)
                            }
                            startActivity(intent)
                        }
                        3 -> showBlockDiscrepancyDialog(member)
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showBlockDiscrepancyDialog(member: MemberEntity) {
        val reasons = arrayOf(
            "Absent from Evening Duty Shift after casting vote",
            "Attempted to vote outside authorized voting period",
            "Morning shift attendance check skipped or absent",
            "Biometric / Identity mismatch discrepancy",
            "Duty absence reported by supervising officer"
        )

        AlertDialog.Builder(this)
            .setTitle("🚨 Block Member: Discrepancy Found")
            .setItems(reasons) { _, which ->
                val reason = reasons[which]
                lifecycleScope.launch(Dispatchers.IO) {
                    database.memberDao().blockMember(member.memberCode, reason)
                    database.voteRecordDao().abandonVotesForMember(member.memberCode, orgId, reason)
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@OrganizationDetailActivity, "${member.name} has been BLOCKED. Votes abandoned.", Toast.LENGTH_LONG).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun unblockMember(member: MemberEntity) {
        lifecycleScope.launch(Dispatchers.IO) {
            database.memberDao().unblockMember(member.memberCode)
            withContext(Dispatchers.Main) {
                Toast.makeText(this@OrganizationDetailActivity, "${member.name} unblocked successfully.", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun openMainActivityAsMember(member: MemberEntity) {
        val org = currentOrg
        val mStart = if (member.morningShiftStart.isNotEmpty()) member.morningShiftStart else (org?.morningShiftStart ?: "09:00")
        val mEnd = if (member.morningShiftEnd.isNotEmpty()) member.morningShiftEnd else (org?.morningShiftEnd ?: "13:00")
        val eStart = if (member.eveningShiftStart.isNotEmpty()) member.eveningShiftStart else (org?.eveningShiftStart ?: "16:00")
        val eEnd = if (member.eveningShiftEnd.isNotEmpty()) member.eveningShiftEnd else (org?.eveningShiftEnd ?: "19:00")

        val intent = Intent(this, MainActivity::class.java).apply {
            putExtra("USER_IDENTIFIER", member.memberCode)
            putExtra("USER_NAME", member.name)
            putExtra("USER_ROLE", member.role.lowercase())
            putExtra("USER_INSTITUTE", orgName)
            putExtra("MEMBER_WORK", member.natureOfWork)
            putExtra("MEMBER_CODE", member.memberCode)
            putExtra("ORG_ID", orgId)
            putExtra("ORG_NAME", orgName)
            putExtra("MORNING_START", mStart)
            putExtra("MORNING_END", mEnd)
            putExtra("EVENING_START", eStart)
            putExtra("EVENING_END", eEnd)
            putExtra("IS_BLOCKED", member.isBlocked)
            putExtra("BLOCK_REASON", member.blockReason)
        }
        startActivity(intent)
    }

    private fun showAlterShiftTimingsDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_alter_shift_timings, null)
        val etMStart = dialogView.findViewById<EditText>(R.id.et_shift_m_start)
        val etMEnd = dialogView.findViewById<EditText>(R.id.et_shift_m_end)
        val etEStart = dialogView.findViewById<EditText>(R.id.et_shift_e_start)
        val etEEnd = dialogView.findViewById<EditText>(R.id.et_shift_e_end)

        currentOrg?.let {
            etMStart.setText(it.morningShiftStart)
            etMEnd.setText(it.morningShiftEnd)
            etEStart.setText(it.eveningShiftStart)
            etEEnd.setText(it.eveningShiftEnd)
        }

        AlertDialog.Builder(this)
            .setTitle("⚙️ Admin: Alter Organization Shifts")
            .setView(dialogView)
            .setPositiveButton("Save Shift Regulations") { _, _ ->
                val mStart = etMStart.text.toString().trim().ifEmpty { "09:00" }
                val mEnd = etMEnd.text.toString().trim().ifEmpty { "13:00" }
                val eStart = etEStart.text.toString().trim().ifEmpty { "16:00" }
                val eEnd = etEEnd.text.toString().trim().ifEmpty { "19:00" }

                lifecycleScope.launch(Dispatchers.IO) {
                    database.organizationDao().updateShiftTimings(orgId, mStart, mEnd, eStart, eEnd)
                    withContext(Dispatchers.Main) {
                        currentOrg?.let {
                            it.morningShiftStart = mStart
                            it.morningShiftEnd = mEnd
                            it.eveningShiftStart = eStart
                            it.eveningShiftEnd = eEnd
                        }
                        binding.tvDetailMorningTiming.text = "$mStart - $mEnd"
                        binding.tvDetailEveningTiming.text = "$eStart - $eEnd"
                        filterMembers()
                        Toast.makeText(this@OrganizationDetailActivity, "Shift timing regulations updated for $orgName!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showAlterMemberShiftDialog(member: MemberEntity) {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_alter_shift_timings, null)
        val etMStart = dialogView.findViewById<EditText>(R.id.et_shift_m_start)
        val etMEnd = dialogView.findViewById<EditText>(R.id.et_shift_m_end)
        val etEStart = dialogView.findViewById<EditText>(R.id.et_shift_e_start)
        val etEEnd = dialogView.findViewById<EditText>(R.id.et_shift_e_end)

        val org = currentOrg
        etMStart.setText(member.morningShiftStart.ifEmpty { org?.morningShiftStart ?: "09:00" })
        etMEnd.setText(member.morningShiftEnd.ifEmpty { org?.morningShiftEnd ?: "13:00" })
        etEStart.setText(member.eveningShiftStart.ifEmpty { org?.eveningShiftStart ?: "16:00" })
        etEEnd.setText(member.eveningShiftEnd.ifEmpty { org?.eveningShiftEnd ?: "19:00" })

        AlertDialog.Builder(this)
            .setTitle("⚙️ Shift Timings for ${member.name}")
            .setMessage("Set custom shift hours based on nature of work: ${member.natureOfWork}")
            .setView(dialogView)
            .setPositiveButton("Apply Hours") { _, _ ->
                val mStart = etMStart.text.toString().trim()
                val mEnd = etMEnd.text.toString().trim()
                val eStart = etEStart.text.toString().trim()
                val eEnd = etEEnd.text.toString().trim()

                lifecycleScope.launch(Dispatchers.IO) {
                    database.memberDao().updateMemberShiftTimings(member.id, mStart, mEnd, eStart, eEnd)
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@OrganizationDetailActivity, "Custom shift hours saved for ${member.name}!", Toast.LENGTH_SHORT).show()
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
                        Toast.makeText(this@OrganizationDetailActivity, "Topic published with voting window $startTime - $endTime!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showEditTopicDialog(topic: VotingTopicEntity) {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_add_topic, null)
        val etCategory = dialogView.findViewById<EditText>(R.id.et_topic_category)
        val etTitle = dialogView.findViewById<EditText>(R.id.et_topic_title)
        val etDescription = dialogView.findViewById<EditText>(R.id.et_topic_description)
        val etOptions = dialogView.findViewById<EditText>(R.id.et_topic_options)
        val etStartTime = dialogView.findViewById<EditText>(R.id.et_voting_start_time)
        val etEndTime = dialogView.findViewById<EditText>(R.id.et_voting_end_time)

        etCategory.setText(topic.category)
        etTitle.setText(topic.title)
        etDescription.setText(topic.description)
        etStartTime.setText(topic.votingStartTime)
        etEndTime.setText(topic.votingEndTime)

        try {
            val listType = object : TypeToken<List<String>>() {}.type
            val opts: List<String> = Gson().fromJson(topic.optionsJson, listType)
            etOptions.setText(opts.joinToString(", "))
        } catch (_: Exception) {}

        AlertDialog.Builder(this)
            .setTitle("✏️ Edit Voting Topic and Period")
            .setView(dialogView)
            .setPositiveButton("Save Changes") { _, _ ->
                val category = etCategory.text.toString().trim().ifEmpty { topic.category }
                val title = etTitle.text.toString().trim().ifEmpty { topic.title }
                val description = etDescription.text.toString().trim().ifEmpty { topic.description }
                val rawOptions = etOptions.text.toString().trim()
                val startTime = etStartTime.text.toString().trim().ifEmpty { topic.votingStartTime }
                val endTime = etEndTime.text.toString().trim().ifEmpty { topic.votingEndTime }

                val optionsList = if (rawOptions.isNotEmpty()) {
                    rawOptions.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                } else {
                    listOf("In Favor / Yes", "Against / No", "Abstain")
                }
                val optionsJson = Gson().toJson(optionsList)

                lifecycleScope.launch(Dispatchers.IO) {
                    database.votingTopicDao().updateTopicDetails(
                        id = topic.id,
                        title = title,
                        description = description,
                        category = category,
                        optionsJson = optionsJson,
                        startTime = startTime,
                        endTime = endTime
                    )
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@OrganizationDetailActivity, "Topic and voting period updated!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun confirmDeleteTopic(topic: VotingTopicEntity) {
        AlertDialog.Builder(this)
            .setTitle("🗑️ Delete Voting Ballot?")
            .setMessage("Are you sure you want to delete \"${topic.title}\"?\n\nThis will remove the topic from active ballots.")
            .setPositiveButton("Delete") { _, _ ->
                lifecycleScope.launch(Dispatchers.IO) {
                    database.votingTopicDao().deleteById(topic.id)
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@OrganizationDetailActivity, "Topic deleted.", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showAddMemberDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_add_member, null)
        val etName = dialogView.findViewById<EditText>(R.id.et_member_name)
        val etWork = dialogView.findViewById<EditText>(R.id.et_member_work)
        val etMobile = dialogView.findViewById<EditText>(R.id.et_member_mobile)

        val cleanOrgName = orgName.replace("&", "and")

        AlertDialog.Builder(this)
            .setTitle("➕ Add Member to $cleanOrgName")
            .setView(dialogView)
            .setPositiveButton("Add Member") { _, _ ->
                val name = etName.text.toString().trim().replace("&", "and")
                val work = etWork.text.toString().trim().replace("&", "and").ifEmpty { "General Staff" }
                val mobile = etMobile.text.toString().trim().ifEmpty { "9800011220" }
                val role = "MEMBER"

                if (name.isEmpty()) {
                    Toast.makeText(this, "Member Name is required", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }

                val code = "MEM-${System.currentTimeMillis() % 10000}"

                lifecycleScope.launch(Dispatchers.IO) {
                    val member = MemberEntity(
                        orgId = orgId,
                        memberCode = code,
                        name = name,
                        role = role,
                        natureOfWork = work,
                        mobile = mobile,
                        email = "${name.lowercase().replace(" ", ".")}@org.gov.in"
                    )
                    database.memberDao().insert(member)
                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@OrganizationDetailActivity, "$name added successfully!", Toast.LENGTH_SHORT).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
