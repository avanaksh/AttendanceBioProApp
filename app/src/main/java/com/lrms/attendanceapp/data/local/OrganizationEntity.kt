package com.lrms.attendanceapp.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "organizations")
data class OrganizationEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val name: String,
    val code: String,
    val category: String, // "SC/HC", "Municipal Corporation", "State/UT", "Housing Society", "Institute Committee", "Election Authority", etc.
    val purpose: String, // e.g., "Cast vote for Selection of Judges/CJM/DJM"
    val iconType: String = "court",
    var morningShiftStart: String = "08:30",
    var morningShiftEnd: String = "12:30",
    var eveningShiftStart: String = "16:00",
    var eveningShiftEnd: String = "18:30"
)
