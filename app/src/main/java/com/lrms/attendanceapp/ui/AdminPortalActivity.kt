package com.lrms.attendanceapp.ui

import android.app.DatePickerDialog
import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AppDatabase
import com.lrms.attendanceapp.data.local.AttendanceEntity
import com.lrms.attendanceapp.databinding.ActivityAdminPortalBinding
import com.lrms.attendanceapp.iap.SubscriptionManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

class AdminPortalActivity : AppCompatActivity() {

    private lateinit var binding: ActivityAdminPortalBinding
    private lateinit var database: AppDatabase
    private lateinit var adapter: AdminAttendanceAdapter

    private var allRecords: List<AttendanceEntity> = emptyList()

    // Filter states
    private var currentAadhaarQuery: String = ""
    private var currentDateFilter: String = ""
    private var currentOccasionFilter: String = "ALL"
    private var currentTypeFilter: String = "ALL"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAdminPortalBinding.inflate(layoutInflater)
        setContentView(binding.root)

        database = AppDatabase.getDatabase(this)

        setupRecyclerView()
        setupListeners()
        observeDatabase()
    }

    private fun setupRecyclerView() {
        adapter = AdminAttendanceAdapter()
        adapter.onItemClickListener = { record ->
            showDeviceRecordDetailsDialog(record)
        }
        binding.rvAdminRecords.layoutManager = LinearLayoutManager(this)
        binding.rvAdminRecords.adapter = adapter
    }

    private fun setupListeners() {
        binding.ibBack.setOnClickListener {
            finish()
        }

        // Disable hardware/system back button while in Admin Portal
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                finish()
            }
        })

        // Admin Logout
        binding.btnAdminLogout.setOnClickListener {
            SubscriptionManager.logOut()
            val intent = Intent(this, OrganizationActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            }
            startActivity(intent)
            finish()
        }

        // Requirement 18: Admin can mark records for particular occasion
        binding.btnAdminMarkOccasion.setOnClickListener {
            showMarkRecordForOccasionDialog()
        }

        // Live text search for Aadhaar No / Name / User ID
        binding.etSearchAadhaar.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                currentAadhaarQuery = s?.toString()?.trim() ?: ""
                applyFilters()
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        // Date Picker Filter
        binding.btnPickDate.setOnClickListener {
            showDatePicker()
        }

        binding.btnClearDate.setOnClickListener {
            currentDateFilter = ""
            binding.btnPickDate.text = "📅 Filter by Date: All Dates"
            binding.btnClearDate.visibility = View.GONE
            applyFilters()
        }

        // Occasion Filter Chips (Requirements 18 & 20)
        binding.btnChipOccAll.setOnClickListener {
            currentOccasionFilter = "ALL"
            updateOccasionChipStyles()
            applyFilters()
        }

        binding.btnChipOccOffice.setOnClickListener {
            currentOccasionFilter = "Office Hours"
            updateOccasionChipStyles()
            applyFilters()
        }

        binding.btnChipOccElection.setOnClickListener {
            currentOccasionFilter = "Committee Election"
            updateOccasionChipStyles()
            applyFilters()
        }

        // Type Filter Chips
        binding.btnChipTypeAll.setOnClickListener {
            currentTypeFilter = "ALL"
            updateTypeChipStyles()
            applyFilters()
        }

        binding.btnChipTypeMorning.setOnClickListener {
            currentTypeFilter = "Morning"
            updateTypeChipStyles()
            applyFilters()
        }

        binding.btnChipTypeEvening.setOnClickListener {
            currentTypeFilter = "Evening"
            updateTypeChipStyles()
            applyFilters()
        }

        // Reset All
        binding.btnResetFilters.setOnClickListener {
            resetAllFilters()
        }

        // Export to CSV Share Intent
        binding.btnAdminExport.setOnClickListener {
            exportFilteredRecordsToCsv()
        }
    }

    private fun showDatePicker() {
        val calendar = Calendar.getInstance()
        val year = calendar.get(Calendar.YEAR)
        val month = calendar.get(Calendar.MONTH)
        val day = calendar.get(Calendar.DAY_OF_MONTH)

        val datePicker = DatePickerDialog(
            this,
            { _, selectedYear, selectedMonth, selectedDay ->
                val formattedDay = String.format("%02d", selectedDay)
                val formattedMonth = String.format("%02d", selectedMonth + 1)
                currentDateFilter = "$formattedDay/$formattedMonth/$selectedYear"

                binding.btnPickDate.text = "📅 Date: $currentDateFilter"
                binding.btnClearDate.visibility = View.VISIBLE
                applyFilters()
            },
            year,
            month,
            day
        )
        datePicker.show()
    }

    private fun observeDatabase() {
        lifecycleScope.launch {
            database.attendanceDao().getAllLogs().collectLatest { logs ->
                allRecords = logs
                updateMetrics(logs)
                applyFilters()
            }
        }
    }

    private fun updateMetrics(logs: List<AttendanceEntity>) {
        binding.tvStatTotal.text = logs.size.toString()
        binding.tvStatMorning.text = logs.count { it.attendanceType.contains("Morning", ignoreCase = true) }.toString()
        binding.tvStatEvening.text = logs.count { it.attendanceType.contains("Evening", ignoreCase = true) }.toString()
        binding.tvStatSynced.text = logs.count { it.blinkVerified }.toString()
    }

    private fun applyFilters() {
        val filtered = allRecords.filter { item ->
            // Aadhaar / Name / ID Filter
            val matchesAadhaar = currentAadhaarQuery.isEmpty() ||
                    item.aadhaarNo.contains(currentAadhaarQuery, ignoreCase = true) ||
                    item.userName.contains(currentAadhaarQuery, ignoreCase = true) ||
                    item.userId.contains(currentAadhaarQuery, ignoreCase = true)

            // Date Filter (timestamp begins with "dd/MM/yyyy")
            val matchesDate = currentDateFilter.isEmpty() ||
                    item.timestamp.contains(currentDateFilter)

            // Occasion Filter (Requirements 18 & 20)
            val matchesOccasion = when (currentOccasionFilter) {
                "Office Hours" -> item.occasion.contains("Office", ignoreCase = true)
                "Committee Election" -> item.occasion.contains("Committee", ignoreCase = true) || item.occasion.contains("Election", ignoreCase = true)
                else -> true
            }

            // Attendance Type Filter
            val matchesType = when (currentTypeFilter) {
                "Morning" -> item.attendanceType.contains("Morning", ignoreCase = true)
                "Evening" -> item.attendanceType.contains("Evening", ignoreCase = true)
                else -> true
            }

            matchesAadhaar && matchesDate && matchesOccasion && matchesType
        }

        adapter.submitList(filtered)
        binding.tvResultsCount.text = "Showing ${filtered.size} of ${allRecords.size} records"

        if (filtered.isEmpty()) {
            binding.layoutEmptyState.visibility = View.VISIBLE
            binding.rvAdminRecords.visibility = View.GONE
        } else {
            binding.layoutEmptyState.visibility = View.GONE
            binding.rvAdminRecords.visibility = View.VISIBLE
        }
    }

    private fun updateOccasionChipStyles() {
        val activeText = ContextCompat.getColor(this, R.color.white)
        val inactiveText = ContextCompat.getColor(this, R.color.slate_400)
        val inactiveColor = ContextCompat.getColor(this, R.color.slate_900)

        binding.btnChipOccAll.setBackgroundColor(if (currentOccasionFilter == "ALL") ContextCompat.getColor(this, R.color.indigo_600) else inactiveColor)
        binding.btnChipOccAll.setTextColor(if (currentOccasionFilter == "ALL") activeText else inactiveText)

        binding.btnChipOccOffice.setBackgroundColor(if (currentOccasionFilter == "Office Hours") ContextCompat.getColor(this, R.color.indigo_600) else inactiveColor)
        binding.btnChipOccOffice.setTextColor(if (currentOccasionFilter == "Office Hours") activeText else inactiveText)

        binding.btnChipOccElection.setBackgroundColor(if (currentOccasionFilter == "Committee Election") ContextCompat.getColor(this, R.color.indigo_600) else inactiveColor)
        binding.btnChipOccElection.setTextColor(if (currentOccasionFilter == "Committee Election") activeText else inactiveText)
    }

    private fun updateTypeChipStyles() {
        val activeText = ContextCompat.getColor(this, R.color.white)
        val inactiveText = ContextCompat.getColor(this, R.color.slate_400)
        val inactiveColor = ContextCompat.getColor(this, R.color.slate_900)

        binding.btnChipTypeAll.setBackgroundColor(if (currentTypeFilter == "ALL") ContextCompat.getColor(this, R.color.indigo_600) else inactiveColor)
        binding.btnChipTypeAll.setTextColor(if (currentTypeFilter == "ALL") activeText else inactiveText)

        binding.btnChipTypeMorning.setBackgroundColor(if (currentTypeFilter == "Morning") ContextCompat.getColor(this, R.color.indigo_600) else inactiveColor)
        binding.btnChipTypeMorning.setTextColor(if (currentTypeFilter == "Morning") activeText else inactiveText)

        binding.btnChipTypeEvening.setBackgroundColor(if (currentTypeFilter == "Evening") ContextCompat.getColor(this, R.color.indigo_600) else inactiveColor)
        binding.btnChipTypeEvening.setTextColor(if (currentTypeFilter == "Evening") activeText else inactiveText)
    }

    private fun resetAllFilters() {
        currentAadhaarQuery = ""
        currentDateFilter = ""
        currentOccasionFilter = "ALL"
        currentTypeFilter = "ALL"

        binding.etSearchAadhaar.setText("")
        binding.btnPickDate.text = "📅 Filter by Date: All Dates"
        binding.btnClearDate.visibility = View.GONE

        updateOccasionChipStyles()
        updateTypeChipStyles()
        applyFilters()

        Toast.makeText(this, "Filters reset to default", Toast.LENGTH_SHORT).show()
    }

    /**
     * Requirement 18, 20, 21, 22:
     * In admin login, all records can be viewed and marked for a particular occasion:
     * 1. Mark Attendance in office hours (Morning/Evening)
     * 2. Caste Vote in Committee Selection System through Election (IETE, IEEE, Courts etc.)
     */
    private fun showMarkRecordForOccasionDialog() {
        val users = arrayOf(
            "Alex Rivera (1234-5678-9021 | ICAR-CIFE Mumbai)",
            "Ramesh Kumar (5555-6666-7777 | ICAR-IASRI New Delhi)"
        )

        AlertDialog.Builder(this)
            .setTitle("Step 1: Select User to Mark Record")
            .setItems(users) { _, userIndex ->
                val (uId, uName, uAadhaar, uInstitute) = if (userIndex == 0) {
                    listOf("EMP-9021", "Alex Rivera", "1234-5678-9021", "ICAR-CIFE Mumbai")
                } else {
                    listOf("EMP-6500", "Ramesh Kumar", "5555-6666-7777", "ICAR-IASRI New Delhi")
                }

                showOccasionSelectionDialog(uId, uName, uAadhaar, uInstitute)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showOccasionSelectionDialog(
        userId: String,
        userName: String,
        aadhaarNo: String,
        institute: String
    ) {
        val occasions = arrayOf(
            "Office Hours: Morning Shift (8:00 AM - 12:00 PM)",
            "Office Hours: Evening Shift (4:00 PM - 6:00 PM)",
            "Committee Vote: IETE Committee Election",
            "Committee Vote: IEEE Advisory Council Election",
            "Committee Vote: Courts and Judicial Selection Panel Election"
        )

        AlertDialog.Builder(this)
            .setTitle("Step 2: Select Occasion for $userName")
            .setItems(occasions) { _, occIndex ->
                val now = SimpleDateFormat("dd/MM/yyyy, hh:mm:ss a", Locale.getDefault()).format(Date())

                val (occasionName, attendanceType, verification) = when (occIndex) {
                    0 -> Triple(
                        AttendanceEntity.OCCASION_OFFICE_HOURS,
                        "Morning-Login",
                        "Admin Verified (Biometric Liveness Match)"
                    )
                    1 -> Triple(
                        AttendanceEntity.OCCASION_OFFICE_HOURS,
                        "Evening-Logout",
                        "Admin Verified (Biometric Liveness Match)"
                    )
                    2 -> Triple(
                        AttendanceEntity.OCCASION_COMMITTEE_ELECTION,
                        "Committee Vote: Dr. Vikram Adityanath (IETE)",
                        "Admin Ballot Authorization (Biometric Confirmed)"
                    )
                    3 -> Triple(
                        AttendanceEntity.OCCASION_COMMITTEE_ELECTION,
                        "Committee Vote: Smt. Meenakshi Sundaram (IEEE)",
                        "Admin Ballot Authorization (Biometric Confirmed)"
                    )
                    else -> Triple(
                        AttendanceEntity.OCCASION_COMMITTEE_ELECTION,
                        "Committee Vote: Adv. Rajeshwar Sharma (Courts)",
                        "Admin Ballot Authorization (Biometric Confirmed)"
                    )
                }

                val record = AttendanceEntity(
                    userId = userId,
                    userName = userName,
                    userEmail = if (userId == "EMP-6500") "ramesh.kumar@example.com" else "alex.rivera@example.com",
                    mobileNo = if (userId == "EMP-6500") "9833344555" else "9811122334",
                    aadhaarNo = aadhaarNo,
                    state = if (userId == "EMP-6500") "Delhi" else "Maharashtra",
                    district = if (userId == "EMP-6500") "South Delhi" else "Mumbai Central",
                    instituteName = institute,
                    latitude = "19.0760 N",
                    longitude = "72.8777 E",
                    address = "Versova, Andheri West, Mumbai, Maharashtra 400061",
                    blinkVerified = true,
                    attendanceType = attendanceType,
                    timestamp = now,
                    verificationMode = verification,
                    confidence = "99.0%",
                    status = "Admin Marked",
                    isSynced = false,
                    occasion = occasionName
                )

                lifecycleScope.launch(Dispatchers.IO) {
                    database.attendanceDao().insertLog(record)
                }

                Toast.makeText(
                    this,
                    "Record marked successfully for $userName on $occasionName!",
                    Toast.LENGTH_LONG
                ).show()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun exportFilteredRecordsToCsv() {
        val filteredList = adapter.currentList
        if (filteredList.isEmpty()) {
            Toast.makeText(this, "No records to export", Toast.LENGTH_SHORT).show()
            return
        }

        val csvBuilder = StringBuilder()
        csvBuilder.append("ID,User ID,Name,Aadhaar No,Occasion,Type,Timestamp,Verification,Location\n")

        for (item in filteredList) {
            csvBuilder.append("${item.id},\"${item.userId}\",\"${item.userName}\",\"${item.aadhaarNo}\",\"${item.occasion}\",\"${item.attendanceType}\",\"${item.timestamp}\",\"${item.verificationMode}\",\"${item.address}\"\n")
        }

        val shareIntent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, "Attendance_Report_${System.currentTimeMillis()}.csv")
            putExtra(Intent.EXTRA_TEXT, csvBuilder.toString())
        }
        startActivity(Intent.createChooser(shareIntent, "Export Attendance CSV Report"))
    }

    private fun showDeviceRecordDetailsDialog(record: AttendanceEntity) {
        val displayType = when {
            record.attendanceType.contains("Morning", ignoreCase = true) -> "Morning Shift"
            record.attendanceType.contains("Evening", ignoreCase = true) -> "Evening Shift"
            else -> record.attendanceType
        }
        val details = """
            🆔 Database ID: ${record.id}
            👤 Employee: ${record.userName}
            💼 User ID: ${record.userId}
            📜 Aadhaar No: ${record.aadhaarNo}
            🏢 Institute: ${record.instituteName}
            📱 Mobile: ${record.mobileNo}
            📧 Email: ${record.userEmail}
            
            🎯 Occasion: ${record.occasion}
            ⏱️ Type / Action: $displayType
            📅 Timestamp: ${record.timestamp}
            👁️ Blink Liveness: ${if (record.blinkVerified) "VERIFIED ✓" else "FAILED"}
            🔍 Verification: ${record.verificationMode} (Confidence: ${record.confidence})
            
            📍 Address: ${record.address}
            🌐 GPS: Lat ${record.latitude}, Long ${record.longitude}
            
            💾 Storage Status: SECURE DEVICE STORAGE (Local Database)
        """.trimIndent()

        AlertDialog.Builder(this)
            .setTitle("📋 Duty Record Details #${record.id}")
            .setMessage(details)
            .setPositiveButton("Close", null)
            .show()
    }
}
