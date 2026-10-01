package com.lrms.attendanceapp.data.local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "local_attendance_logs")
data class AttendanceEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val userId: String,
    val userName: String,
    val userEmail: String,
    val mobileNo: String,
    val aadhaarNo: String,
    val state: String,
    val district: String,
    val instituteName: String,
    val latitude: String,
    val longitude: String,
    val address: String,
    val blinkVerified: Boolean,
    val attendanceType: String, // "Morning Shift", "Evening Shift", or "Committee Vote"
    val timestamp: String,
    val verificationMode: String,
    val confidence: String,
    val status: String,
    var isSynced: Boolean = false,
    @ColumnInfo(name = "occasion", defaultValue = "Duty Hours Attendance")
    val occasion: String = OCCASION_DUTY_HOURS,
    @ColumnInfo(name = "orgId", defaultValue = "0")
    val orgId: Long = 0,
    @ColumnInfo(name = "memberCode", defaultValue = "''")
    val memberCode: String = ""
) {
    companion object {
        const val OCCASION_OFFICE_HOURS = "Duty Hours Attendance"
        const val OCCASION_DUTY_HOURS = "Duty Hours Attendance"
        const val OCCASION_COMMITTEE_ELECTION = "Organization Ballots and Voting"
    }
}
