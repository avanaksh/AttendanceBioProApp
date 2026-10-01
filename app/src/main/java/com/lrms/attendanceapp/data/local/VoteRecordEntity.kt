package com.lrms.attendanceapp.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "vote_records")
data class VoteRecordEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val orgId: Long,
    val topicId: Long,
    val memberCode: String,
    val memberName: String,
    val selectedOption: String,
    val timestamp: String,
    val biometricHash: String = "Biometric Re-Authentication Verified",
    var status: String = STATUS_PENDING_EVENING,
    var isFinalized: Boolean = false,
    var abandonReason: String = ""
) {
    fun isCounted(): Boolean = status == STATUS_CONFIRMED && isFinalized

    companion object {
        const val STATUS_PENDING_EVENING = "PENDING_EVENING_ATTENDANCE"
        const val STATUS_CONFIRMED = "CONFIRMED_FINAL"
        const val STATUS_UNCOUNTED_EVENING_ABSENT = "UNCOUNTED_EVENING_ABSENT"
        const val STATUS_ABANDONED = "ABANDONED_INVALID"
    }
}
