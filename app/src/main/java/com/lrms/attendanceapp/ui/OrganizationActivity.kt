package com.lrms.attendanceapp.ui

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AppDatabase
import com.lrms.attendanceapp.data.local.MemberEntity
import com.lrms.attendanceapp.data.local.OrganizationEntity
import com.lrms.attendanceapp.data.local.VotingTopicEntity
import com.lrms.attendanceapp.databinding.ActivityOrganizationBinding
import com.lrms.attendanceapp.iap.PaywallActivity
import com.lrms.attendanceapp.iap.SubscriptionManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class OrganizationActivity : AppCompatActivity() {

    private lateinit var binding: ActivityOrganizationBinding
    private lateinit var database: AppDatabase
    private lateinit var adapter: OrganizationAdapter

    private var allOrganizations: List<OrganizationEntity> = emptyList()
    private var searchQuery: String = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOrganizationBinding.inflate(layoutInflater)
        setContentView(binding.root)

        database = AppDatabase.getDatabase(this)

        setupRecyclerView()
        setupListeners()
        observeOrganizations()
    }

    override fun onResume() {
        super.onResume()
        checkProStatus()
    }

    private fun checkProStatus() {
        SubscriptionManager.checkSubscriptionStatus { details ->
            runOnUiThread {
                when {
                    details.isExpired -> {
                        binding.tvProStatusPill.text = "⏳ TRIAL EXPIRED"
                        binding.cardProPill.setCardBackgroundColor(getColor(R.color.indigo_600))
                    }
                    details.isExpiringSoon -> {
                        binding.tvProStatusPill.text = "⚠️ TRIAL (${details.daysRemaining}D)"
                        binding.cardProPill.setCardBackgroundColor(getColor(R.color.amber_500))
                    }
                    details.isTrial -> {
                        binding.tvProStatusPill.text = "⭐ TRIAL (${details.daysRemaining}D)"
                        binding.cardProPill.setCardBackgroundColor(getColor(R.color.amber_500))
                    }
                    details.isPro -> {
                        binding.tvProStatusPill.text = "👑 PRO ACTIVE"
                        binding.cardProPill.setCardBackgroundColor(getColor(R.color.amber_500))
                    }
                    else -> {
                        binding.tvProStatusPill.text = "⭐ PRO ACCESS"
                        binding.cardProPill.setCardBackgroundColor(getColor(R.color.indigo_600))
                    }
                }
            }
        }
    }

    private fun setupRecyclerView() {
        adapter = OrganizationAdapter { organization ->
            val intent = Intent(this, OrganizationDetailActivity::class.java).apply {
                putExtra("EXTRA_ORG_ID", organization.id)
                putExtra("EXTRA_ORG_NAME", organization.name)
                putExtra("EXTRA_ORG_CATEGORY", organization.category)
                putExtra("EXTRA_ORG_PURPOSE", organization.purpose)
            }
            startActivity(intent)
        }
        binding.rvOrganizations.layoutManager = LinearLayoutManager(this)
        binding.rvOrganizations.adapter = adapter
    }

    private fun setupListeners() {
        binding.cardProPill.setOnClickListener {
            val intent = Intent(this, PaywallActivity::class.java).apply {
                putExtra("IS_FROM_INSIDE_APP", true)
            }
            startActivity(intent)
        }

        binding.etSearchOrg.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                searchQuery = s?.toString()?.trim() ?: ""
                filterOrganizations()
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        binding.fabAddOrg.setOnClickListener {
            showAddOrganizationDialog()
        }
    }

    private fun observeOrganizations() {
        lifecycleScope.launch {
            database.organizationDao().getAllOrganizations().collectLatest { orgList ->
                allOrganizations = orgList
                filterOrganizations()
            }
        }
    }

    private fun filterOrganizations() {
        val filtered = if (searchQuery.isEmpty()) {
            allOrganizations
        } else {
            allOrganizations.filter {
                it.name.contains(searchQuery, ignoreCase = true) ||
                it.category.contains(searchQuery, ignoreCase = true) ||
                it.purpose.contains(searchQuery, ignoreCase = true)
            }
        }
        adapter.submitList(filtered)
    }

    private fun showAddOrganizationDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_add_organization, null)
        val etName = dialogView.findViewById<EditText>(R.id.et_dialog_org_name)
        val etCategory = dialogView.findViewById<EditText>(R.id.et_dialog_org_category)
        val etPurpose = dialogView.findViewById<EditText>(R.id.et_dialog_org_purpose)
        val etMorningHours = dialogView.findViewById<EditText>(R.id.et_dialog_morning_hours)
        val etEveningHours = dialogView.findViewById<EditText>(R.id.et_dialog_evening_hours)

        AlertDialog.Builder(this)
            .setTitle("🏢 Register New Organization")
            .setView(dialogView)
            .setPositiveButton("Create and Register") { _, _ ->
                val name = etName.text.toString().trim()
                val category = etCategory.text.toString().trim().ifEmpty { "Apex Subsidiary" }
                val purpose = etPurpose.text.toString().trim().ifEmpty { "Cast vote for leadership and governance" }
                val morning = etMorningHours.text.toString().trim().ifEmpty { "09:00 - 13:00" }
                val evening = etEveningHours.text.toString().trim().ifEmpty { "16:00 - 19:00" }

                if (name.isEmpty()) {
                    Toast.makeText(this, "Organization Name is required", Toast.LENGTH_SHORT).show()
                    return@setPositiveButton
                }

                val mParts = morning.split("-").map { it.trim() }
                val eParts = evening.split("-").map { it.trim() }

                val mStart = if (mParts.isNotEmpty()) mParts[0] else "09:00"
                val mEnd = if (mParts.size > 1) mParts[1] else "13:00"
                val eStart = if (eParts.isNotEmpty()) eParts[0] else "16:00"
                val eEnd = if (eParts.size > 1) eParts[1] else "19:00"

                lifecycleScope.launch(Dispatchers.IO) {
                    val org = OrganizationEntity(
                        name = name,
                        code = "CUSTOM_${System.currentTimeMillis() % 10000}",
                        category = category,
                        purpose = purpose,
                        iconType = "apex",
                        morningShiftStart = mStart,
                        morningShiftEnd = mEnd,
                        eveningShiftStart = eStart,
                        eveningShiftEnd = eEnd
                    )
                    val newOrgId = database.organizationDao().insert(org)

                    // Add 1 Admin and initial members dynamically for the new organization
                    val admin = MemberEntity(
                        orgId = newOrgId,
                        memberCode = "ADM-${System.currentTimeMillis() % 1000}",
                        name = "Admin In-Charge",
                        role = "ADMIN",
                        natureOfWork = "Organization General Administrator",
                        mobile = "9800011220",
                        email = "admin@org.gov.in"
                    )
                    database.memberDao().insert(admin)

                    // Also create an initial topic for voting
                    val today = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())
                    database.votingTopicDao().insert(
                        VotingTopicEntity(
                            orgId = newOrgId,
                            title = "$name Inaugural Governance and Policy Vote",
                            description = "Initial resolution for organizational policies, administrative decisions, and committee selection.",
                            category = "Governance Notification",
                            optionsJson = "[\"Approve Policy Framework\", \"Amend and Resubmit\", \"Abstain\"]",
                            createdAt = today
                        )
                    )

                    withContext(Dispatchers.Main) {
                        Toast.makeText(this@OrganizationActivity, "Organization registered successfully!", Toast.LENGTH_LONG).show()
                    }
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }
}
