package com.lrms.attendanceapp.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AppDatabase
import com.lrms.attendanceapp.data.local.DatabaseInitializer
import com.lrms.attendanceapp.data.local.MemberEntity
import com.lrms.attendanceapp.data.local.OrganizationEntity
import com.lrms.attendanceapp.databinding.ActivityLoginBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private lateinit var database: AppDatabase

    private var organizations: List<OrganizationEntity> = emptyList()
    private var currentMembers: List<MemberEntity> = emptyList()
    private var selectedOrg: OrganizationEntity? = null
    private var selectedMember: MemberEntity? = null

    private var isAdminMode: Boolean = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        database = AppDatabase.getDatabase(this)

        setupRoleToggle()
        setupListeners()
        loadData()
    }

    private fun setupRoleToggle() {
        binding.rgRole.setOnCheckedChangeListener { _, checkedId ->
            if (checkedId == R.id.rb_role_admin) {
                isAdminMode = true
                binding.tvRoleBanner.text = "👑 Administrator Mode: Access Authority Voting Audit, Add/Edit/Delete Topics, Alter Shift Timings, and Member Blocking for discrepancies."
                binding.tvRoleBanner.setBackgroundResource(R.drawable.bg_badge_gold)
                binding.tvRoleBanner.setTextColor(ContextCompat.getColor(this, R.color.slate_950))
                binding.btnQuickProfileLogin.text = "⚡ Sign In as Selected Administrator"
                binding.etIdentifier.hint = "e.g. JUD-ADM-01, MC-ADM-01, PR-ADM-01 or 'admin'"
                binding.etPassword.setText("admin123")
            } else {
                isAdminMode = false
                binding.tvRoleBanner.text = "👤 Member Mode: Access personal duty check-in (Step 1: Morning ➔ Step 2: Cast Ballot ➔ Step 3: Evening Check-in and Seal)."
                binding.tvRoleBanner.setBackgroundResource(R.drawable.bg_pill_role)
                binding.tvRoleBanner.setTextColor(ContextCompat.getColor(this, R.color.white))
                binding.btnQuickProfileLogin.text = "⚡ Sign In as Selected Member"
                binding.etIdentifier.hint = "e.g. JUD-MEM-01, MC-MEM-01, PR-MEM-01, Mobile, or Aadhaar"
                binding.etPassword.setText("user123")
            }
            refreshMemberSpinner()
        }
    }

    private fun setupListeners() {
        binding.btnQuickProfileLogin.setOnClickListener {
            val member = selectedMember
            val org = selectedOrg
            if (member == null || org == null) {
                Toast.makeText(this, "Select an organization and member profile", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            launchDutyConsole(member, org)
        }

        binding.btnLogin.setOnClickListener {
            val identifier = binding.etIdentifier.text.toString().trim()
            val password = binding.etPassword.text.toString().trim()

            if (identifier.isEmpty()) {
                Toast.makeText(this, "Enter your Member Code, Mobile, Email, or Aadhaar", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            performManualLogin(identifier, password)
        }

        // Demo Shortcut Buttons
        binding.btnDemoScAdmin.setOnClickListener { loginByMemberCode("JUD-ADM-01") }
        binding.btnDemoScMember.setOnClickListener { loginByMemberCode("JUD-MEM-01") }
        binding.btnDemoMcAdmin.setOnClickListener { loginByMemberCode("MC-ADM-01") }
        binding.btnDemoMcMember.setOnClickListener { loginByMemberCode("MC-MEM-01") }
        binding.btnDemoPrAdmin.setOnClickListener { loginByMemberCode("PR-ADM-01") }
        binding.btnDemoPrMember.setOnClickListener { loginByMemberCode("PR-MEM-01") }

        binding.btnBrowseOrganizations.setOnClickListener {
            val intent = Intent(this, OrganizationActivity::class.java)
            startActivity(intent)
        }
    }

    private fun loadData() {
        val targetOrgId = intent.getLongExtra("EXTRA_ORG_ID", -1L)

        lifecycleScope.launch(Dispatchers.IO) {
            DatabaseInitializer.populateInitialDataIfNeeded(database)
            var orgs = database.organizationDao().getAllOrganizationsList()
            if (orgs.isEmpty()) {
                for (i in 1..10) {
                    kotlinx.coroutines.delay(200)
                    orgs = database.organizationDao().getAllOrganizationsList()
                    if (orgs.isNotEmpty()) break
                }
            }
            organizations = orgs

            withContext(Dispatchers.Main) {
                if (organizations.isEmpty()) return@withContext

                val orgNames = organizations.map { "${it.name} (${it.category})" }
                val orgAdapter = ArrayAdapter(this@LoginActivity, R.layout.item_spinner_selected, orgNames)
                orgAdapter.setDropDownViewResource(R.layout.item_spinner_dropdown)
                binding.spOrganization.adapter = orgAdapter

                // Set initial selection
                val initialIndex = if (targetOrgId > 0) {
                    val idx = organizations.indexOfFirst { it.id == targetOrgId }
                    if (idx >= 0) idx else 0
                } else {
                    0
                }
                binding.spOrganization.setSelection(initialIndex)
                selectedOrg = organizations[initialIndex]

                binding.spOrganization.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                    override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                        selectedOrg = organizations[position]
                        loadMembersForOrg(selectedOrg!!.id)
                    }

                    override fun onNothingSelected(parent: AdapterView<*>?) {}
                }

                loadMembersForOrg(selectedOrg!!.id)
            }
        }
    }

    private fun loadMembersForOrg(orgId: Long) {
        lifecycleScope.launch(Dispatchers.IO) {
            currentMembers = database.memberDao().getMembersListByOrg(orgId)
            withContext(Dispatchers.Main) {
                refreshMemberSpinner()
            }
        }
    }

    private fun refreshMemberSpinner() {
        val filtered = if (isAdminMode) {
            val admins = currentMembers.filter { it.role.equals("ADMIN", ignoreCase = true) }
            if (admins.isNotEmpty()) admins else currentMembers
        } else {
            val members = currentMembers.filter { !it.role.equals("ADMIN", ignoreCase = true) }
            if (members.isNotEmpty()) members else currentMembers
        }

        if (filtered.isEmpty()) {
            val emptyList = listOf("No members registered in this category")
            val emptyAdapter = ArrayAdapter(this, R.layout.item_spinner_selected, emptyList)
            emptyAdapter.setDropDownViewResource(R.layout.item_spinner_dropdown)
            binding.spMember.adapter = emptyAdapter
            selectedMember = null
            return
        }

        val memberLabels = filtered.map {
            val roleIcon = if (it.role.equals("ADMIN", ignoreCase = true)) "👑 [ADMIN]" else "👤 [MEMBER]"
            "${it.name} $roleIcon • ${it.natureOfWork}"
        }

        val memberAdapter = ArrayAdapter(this, R.layout.item_spinner_selected, memberLabels)
        memberAdapter.setDropDownViewResource(R.layout.item_spinner_dropdown)
        binding.spMember.adapter = memberAdapter

        selectedMember = filtered.firstOrNull()

        binding.spMember.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                if (position in filtered.indices) {
                    selectedMember = filtered[position]
                    binding.etIdentifier.setText(selectedMember!!.memberCode)
                }
            }

            override fun onNothingSelected(parent: AdapterView<*>?) {}
        }

        selectedMember?.let {
            binding.etIdentifier.setText(it.memberCode)
        }
    }

    private fun performManualLogin(identifier: String, pass: String) {
        lifecycleScope.launch(Dispatchers.IO) {
            var member: MemberEntity? = null
            var org: OrganizationEntity? = null

            // 1. Direct identifier query (Code, Mobile, Email, Aadhaar)
            member = database.memberDao().getMemberByIdentifier(identifier)

            // 2. Generic "admin" keyword shortcut
            if (member == null && (identifier.equals("admin", ignoreCase = true) || pass.equals("admin123", ignoreCase = true))) {
                val orgTarget = selectedOrg ?: organizations.firstOrNull()
                if (orgTarget != null) {
                    member = database.memberDao().getAdminForOrg(orgTarget.id)
                }
            }

            // 3. Generic "user" or "member" keyword shortcut
            if (member == null && (identifier.equals("user", ignoreCase = true) || identifier.equals("member", ignoreCase = true))) {
                val orgTarget = selectedOrg ?: organizations.firstOrNull()
                if (orgTarget != null) {
                    val members = database.memberDao().getMembersListByOrg(orgTarget.id)
                    member = members.firstOrNull { !it.role.equals("ADMIN", ignoreCase = true) } ?: members.firstOrNull()
                }
            }

            if (member != null) {
                org = database.organizationDao().getOrganizationById(member.orgId)
            }

            withContext(Dispatchers.Main) {
                if (member != null && org != null) {
                    launchDutyConsole(member, org)
                } else {
                    AlertDialog.Builder(this@LoginActivity)
                        .setTitle("⚠️ Credential Not Found")
                        .setMessage("No member account matched \"$identifier\".\n\nYou can use:\n• Member Code (e.g. JUD-ADM-01, JUD-MEM-01)\n• Mobile Number (e.g. 9820011221)\n• Email address\n• Aadhaar Number\n• Or tap any profile in the Fast Profile Selector or Quick-Test presets.")
                        .setPositiveButton("OK", null)
                        .show()
                }
            }
        }
    }

    private fun loginByMemberCode(code: String) {
        lifecycleScope.launch(Dispatchers.IO) {
            val member = database.memberDao().getMemberByCode(code)
            val org = if (member != null) database.organizationDao().getOrganizationById(member.orgId) else null
            withContext(Dispatchers.Main) {
                if (member != null && org != null) {
                    launchDutyConsole(member, org)
                } else {
                    Toast.makeText(this@LoginActivity, "Member code $code not found", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun launchDutyConsole(member: MemberEntity, org: OrganizationEntity) {
        val mStart = if (member.morningShiftStart.isNotEmpty()) member.morningShiftStart else org.morningShiftStart
        val mEnd = if (member.morningShiftEnd.isNotEmpty()) member.morningShiftEnd else org.morningShiftEnd
        val eStart = if (member.eveningShiftStart.isNotEmpty()) member.eveningShiftStart else org.eveningShiftStart
        val eEnd = if (member.eveningShiftEnd.isNotEmpty()) member.eveningShiftEnd else org.eveningShiftEnd

        val roleStr = member.role.lowercase()
        val roleIcon = if (roleStr == "admin") "👑 Administrator" else "👤 Member"

        Toast.makeText(this, "Logged in as ${member.name} ($roleIcon)", Toast.LENGTH_SHORT).show()

        val intent = Intent(this, MainActivity::class.java).apply {
            putExtra("USER_IDENTIFIER", member.memberCode)
            putExtra("USER_NAME", member.name)
            putExtra("USER_ROLE", roleStr)
            putExtra("USER_INSTITUTE", org.name)
            putExtra("MEMBER_WORK", member.natureOfWork)
            putExtra("MEMBER_CODE", member.memberCode)
            putExtra("ORG_ID", org.id)
            putExtra("ORG_NAME", org.name)
            putExtra("MORNING_START", mStart)
            putExtra("MORNING_END", mEnd)
            putExtra("EVENING_START", eStart)
            putExtra("EVENING_END", eEnd)
            putExtra("IS_BLOCKED", member.isBlocked)
            putExtra("BLOCK_REASON", member.blockReason)
        }
        startActivity(intent)
    }
}
